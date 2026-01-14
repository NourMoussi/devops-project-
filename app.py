import logging
import datetime
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv
from marshmallow import ValidationError

# Import du modèle et du gestionnaire de données
from models.task import db_manager, TaskSchema

# Charger les variables d'environnement
load_dotenv()

# Configuration du Logging Structuré (JSON)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

# Initialisation de l'application
app = Flask(__name__)
CORS(app)

# Métadonnées
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')

# Initialisation des schémas de validation
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# -------------------------------------------------------------------
# Endpoints API
# -------------------------------------------------------------------

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de Health Check."""
    logger.info("Health check requested")
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'version': APP_VERSION,
        'environment': os.getenv('FLASK_ENV', 'development')
    }), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Récupérer toutes les tâches."""
    logger.info("Fetching all tasks")
    tasks = db_manager.get_all()
    # Sérialisation des objets Task en JSON via Marshmallow
    result = tasks_schema.dump(tasks)
    return jsonify(result), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    """Créer une nouvelle tâche."""
    json_data = request.get_json()
    if not json_data:
        logger.warning("Create task attempt with no data")
        return jsonify({"message": "No input data provided"}), 400
    
    try:
        # Validation et création de l'objet Task
        task = task_schema.load(json_data)
        created_task = db_manager.create(task)
        logger.info(f"Task created: {created_task.id}")
        return jsonify(task_schema.dump(created_task)), 201
    except ValidationError as err:
        logger.warning(f"Validation error: {err.messages}")
        return jsonify(err.messages), 422

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    """Récupérer une tâche par son ID."""
    task = db_manager.get_by_id(task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        return jsonify({"message": "Task not found"}), 404
    
    return jsonify(task_schema.dump(task)), 200

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    """Mettre à jour une tâche."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    # Vérifier l'existence AVANT de valider pour éviter des logs inutiles
    existing_task = db_manager.get_by_id(task_id)
    if not existing_task:
        logger.warning(f"Update attempt on non-existent task: {task_id}")
        return jsonify({"message": "Task not found"}), 404

    try:
        # On valide partiel=True car on peut ne mettre à jour que le statut par exemple
        errors = task_schema.validate(json_data, partial=True)
        if errors:
            raise ValidationError(errors)
            
        updated_task = db_manager.update(task_id, json_data)
        logger.info(f"Task updated: {task_id}")
        return jsonify(task_schema.dump(updated_task)), 200
    except ValidationError as err:
        logger.warning(f"Validation error: {err.messages}")
        return jsonify(err.messages), 422

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Supprimer une tâche."""
    success = db_manager.delete(task_id)
    if not success:
        logger.warning(f"Delete attempt on non-existent task: {task_id}")
        return jsonify({"message": "Task not found"}), 404
    
    logger.info(f"Task deleted: {task_id}")
    return jsonify({"message": "Task deleted successfully"}), 200


if __name__ == '__main__':
    # Configuration du port et de l'hôte
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
