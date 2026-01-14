import logging
import datetime
import os
from flask import Flask, jsonify
from flask_cors import CORS
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du Logging Structuré (JSON)
# C'est une bonne pratique DevOps pour faciliter le parsing des logs
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

# Configuration CORS (Cross-Origin Resource Sharing)
# Permet à des applications frontend situées sur d'autres domaines d'appeler l'API
CORS(app)

# Métadonnées de l'application
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')

@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de Health Check simple.
    Utilisé par Kubernetes et les load balancers pour vérifier si le service est en vie.
    """
    logger.info("Health check requested")
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'version': APP_VERSION,
        'environment': os.getenv('FLASK_ENV', 'development')
    }), 200

if __name__ == '__main__':
    # Configuration du port et de l'hôte
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
