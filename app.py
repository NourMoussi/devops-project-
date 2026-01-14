import logging
import datetime
import os
import time
import uuid
from flask import Flask, jsonify, request, g, has_request_context
from flask_cors import CORS
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv
from marshmallow import ValidationError
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask_swagger_ui import get_swaggerui_blueprint

# Import du modèle et du gestionnaire de données
from models.task import db_manager, TaskSchema

# Charger les variables d'environnement
load_dotenv()

# -------------------------------------------------------------------
# Configuration du Logging avec REQUEST ID
# -------------------------------------------------------------------
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if has_request_context():
            record.request_id = getattr(g, 'request_id', 'unknown')
        else:
            record.request_id = 'system'
        return True

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt='%(asctime)s %(levelname)s %(name)s %(request_id)s %(message)s'
)
logHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(logHandler)
logger.addFilter(RequestIdFilter())
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

# Initialisation de l'application
app = Flask(__name__)
CORS(app)

# Configuration Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Task Manager API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


APP_VERSION = os.getenv('APP_VERSION', '1.0.0')

# Schémas Marshmallow
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# -------------------------------------------------------------------
# M É T R I Q U E S   P R O M E T H E U S
# -------------------------------------------------------------------
# ... (Métriques inchangées)
HTTP_REQUESTS_TOTAL = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
HTTP_REQUEST_DURATION_SECONDS = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'endpoint'])
APP_TASKS_TOTAL = Gauge('app_tasks_total', 'Total number of tasks in memory')

# -------------------------------------------------------------------
# Middlewares (Tracing & Metrics)
# -------------------------------------------------------------------
@app.before_request
def before_request():
    # 1. Start Timer pour métriques
    g.start_time = time.time()
    # 2. Generate Request ID pour tracing
    # On accepte X-Request-ID entrant (pour tracing distribué) ou on en génère un
    request_id = request.headers.get('X-Request-ID')
    if not request_id:
        request_id = str(uuid.uuid4())
    g.request_id = request_id

@app.after_request
def after_request(response):
    # Ajout du Request ID dans les headers de réponse
    response.headers['X-Request-ID'] = g.request_id
    
    if request.endpoint == 'metrics':
        return response
        
    duration = time.time() - g.start_time
    endpoint = request.endpoint if request.endpoint else 'unknown'
    
    HTTP_REQUEST_DURATION_SECONDS.labels(method=request.method, endpoint=endpoint).observe(duration)
    HTTP_REQUESTS_TOTAL.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
    
    return response

# -------------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------------

@app.route('/metrics')
def metrics():
    """Endpoint exposé pour le scraping Prometheus."""
    # Mise à jour de la jauge métier juste avant le scraping
    count = len(db_manager.get_all())
    APP_TASKS_TOTAL.set(count)
    
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de Health Check."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'version': APP_VERSION
    }), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    logger.info("Fetching all tasks")
    tasks = db_manager.get_all()
    return jsonify(tasks_schema.dump(tasks)), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    
    try:
        task = task_schema.load(json_data)
        created_task = db_manager.create(task)
        logger.info(f"Task created: {created_task.id}")
        return jsonify(task_schema.dump(created_task)), 201
    except ValidationError as err:
        logger.warning(f"Validation error: {err.messages}")
        return jsonify(err.messages), 422

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = db_manager.get_by_id(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    return jsonify(task_schema.dump(task)), 200

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    existing_task = db_manager.get_by_id(task_id)
    if not existing_task:
        return jsonify({"message": "Task not found"}), 404

    try:
        errors = task_schema.validate(json_data, partial=True)
        if errors:
            raise ValidationError(errors)
            
        updated_task = db_manager.update(task_id, json_data)
        logger.info(f"Task updated: {task_id}")
        return jsonify(task_schema.dump(updated_task)), 200
    except ValidationError as err:
        return jsonify(err.messages), 422

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    success = db_manager.delete(task_id)
    if not success:
        return jsonify({"message": "Task not found"}), 404
    
    logger.info(f"Task deleted: {task_id}")
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

