import datetime
import uuid
from marshmallow import Schema, fields, validate, post_load

# -------------------------------------------------------------------
# Modèle de Données (Domain Model)
# -------------------------------------------------------------------
class Task:
    def __init__(self, title, description, status="TODO", _id=None, created_at=None):
        self.id = _id if _id else str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at if created_at else datetime.datetime.utcnow().isoformat() + 'Z'

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }

# -------------------------------------------------------------------
# Schéma de Validation (Marshmallow)
# Permet de valider les entrées API et de sérialiser les objets
# -------------------------------------------------------------------
class TaskSchema(Schema):
    id = fields.Str(dump_only=True)  # L'ID est généré par le serveur, pas par l'utilisateur
    title = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    description = fields.Str(required=True, validate=validate.Length(max=500))
    status = fields.Str(validate=validate.OneOf(["TODO", "IN_PROGRESS", "DONE"]), missing="TODO")
    created_at = fields.Str(dump_only=True)

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)

# -------------------------------------------------------------------
# Gestionnaire de Données (In-Memory Repository)
# Simule une base de données
# -------------------------------------------------------------------
class TaskManager:
    def __init__(self):
        self.tasks = {}  # Dictionnaire pour accès O(1) par ID
        self._initialize_demo_data()

    def _initialize_demo_data(self):
        """Charge quelques données de démonstration au démarrage."""
        demo_tasks = [
            Task("Apprendre DevOps", "Suivre le cours complet et faire le projet", "IN_PROGRESS"),
            Task("Configurer CI/CD", "Mettre en place GitHub Actions", "TODO"),
            Task("Manger une pizza", "Récompense après le déploiement", "TODO")
        ]
        for task in demo_tasks:
            self.tasks[task.id] = task

    def get_all(self):
        """Retourne toutes les tâches sous forme de liste."""
        return list(self.tasks.values())

    def get_by_id(self, task_id):
        """Retourne une tâche par son ID ou None."""
        return self.tasks.get(task_id)

    def create(self, task):
        """Ajoute une nouvelle tâche."""
        self.tasks[task.id] = task
        return task

    def update(self, task_id, data):
        """Met à jour une tâche existante."""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        return task

    def delete(self, task_id):
        """Supprime une tâche."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

# Instance globale (Singleton pattern simplifié pour ce projet)
db_manager = TaskManager()
