import logging, datetime, os, time, uuid
from flask import Flask, jsonify, request, g, has_request_context
from flask_cors import CORS
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv
from marshmallow import ValidationError
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask_swagger_ui import get_swaggerui_blueprint
from models.task import db_manager, TaskSchema

load_dotenv()
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(g, 'request_id', 'unknown') if has_request_context() else 'system'
        return True

logHandler = logging.StreamHandler()
logHandler.setFormatter(jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(request_id)s %(message)s'))
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.addFilter(RequestIdFilter())
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

app = Flask(__name__)
CORS(app)
SWAGGER_URL, API_URL = '/swagger', '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Task Manager API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

APP_VERSION, task_schema, tasks_schema = os.getenv('APP_VERSION', '1.0.0'), TaskSchema(), TaskSchema(many=True)
HTTP_REQUESTS_TOTAL = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
HTTP_REQUEST_DURATION_SECONDS = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'endpoint'])
APP_TASKS_TOTAL = Gauge('app_tasks_total', 'Total number of tasks in memory')

@app.before_request
def before_request():
    g.start_time, request_id = time.time(), request.headers.get('X-Request-ID', str(uuid.uuid4()))
    g.request_id = request_id

@app.after_request
def after_request(response):
    response.headers['X-Request-ID'] = g.request_id
    if request.endpoint != 'metrics':
        duration, endpoint = time.time() - g.start_time, request.endpoint or 'unknown'
        HTTP_REQUEST_DURATION_SECONDS.labels(method=request.method, endpoint=endpoint).observe(duration)
        HTTP_REQUESTS_TOTAL.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
    return response

@app.route('/metrics')
def metrics():
    APP_TASKS_TOTAL.set(len(db_manager.get_all()))
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.utcnow().isoformat() + 'Z', 'version': APP_VERSION}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    logger.info("Fetching all tasks")
    return jsonify(tasks_schema.dump(db_manager.get_all())), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    json_data = request.get_json()
    if not json_data: return jsonify({"message": "No input data provided"}), 400
    try:
        task = db_manager.create(task_schema.load(json_data))
        logger.info(f"Task created: {task.id}")
        return jsonify(task_schema.dump(task)), 201
    except ValidationError as err:
        logger.warning(f"Validation error: {err.messages}")
        return jsonify(err.messages), 422

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = db_manager.get_by_id(task_id)
    if not task: return jsonify({"message": "Task not found"}), 404
    return jsonify(task_schema.dump(task)), 200

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    json_data = request.get_json()
    if not json_data: return jsonify({"message": "No input data provided"}), 400
    if not db_manager.get_by_id(task_id): return jsonify({"message": "Task not found"}), 404
    try:
        errors = task_schema.validate(json_data, partial=True)
        if errors: raise ValidationError(errors)
        updated_task = db_manager.update(task_id, json_data)
        logger.info(f"Task updated: {task_id}")
        return jsonify(task_schema.dump(updated_task)), 200
    except ValidationError as err: return jsonify(err.messages), 422

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not db_manager.delete(task_id): return jsonify({"message": "Task not found"}), 404
    logger.info(f"Task deleted: {task_id}")
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == '__main__':
    port, debug = int(os.getenv('PORT', 5000)), os.getenv('FLASK_DEBUG', '0') == '1'
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) # nosec
