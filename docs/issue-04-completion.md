# Issue #4 - Modèle Task et Stockage ✅

## 📋 Résumé

L'Issue #4 a été complétée. Nous avons mis en place la couche de données de l'application.

## ✅ Checklist Complétée

- [x] Créer la structure `models/`
- [x] Créer la classe `Task` (attributs id, title, description, status, created_at)
- [x] Implémenter le stockage en mémoire (`TaskManager`)
- [x] Implémenter la validation avec Marshmallow (`TaskSchema`)
- [x] Ajouter des données de démo

## 💻 Détails Techniques

### Architecture des Données
- **Modèle Anémique/Riche** : La classe `Task` contient à la fois les données et une logique de sérialisation simple.
- **Repository Pattern** : La classe `TaskManager` agit comme une abstraction de la base de données. Si demain nous voulons passer à PostgreSQL, il suffira de modifier cette classe sans toucher aux contrôleurs.
- **Validation Layer** : Marshmallow garantit que seules des données valides entrent dans notre système (titre entre 3 et 100 caractères, statut valide, etc.).

### Structure du Code (`models/task.py`)
```python
class Task: ...        # Entité métier
class TaskSchema: ...  # Validation et Sérialisation
class TaskManager: ... # Accès aux données (In-Memory pour l'instant)
```

## 📌 Prochaines Étapes

**Issue #5** : Implémentation des endpoints CRUD.
Nous allons maintenant connecter `app.py` à ce modèle pour exposer les routes `/tasks`.

---

**Status** : ✅ COMPLÉTÉ
**Date** : 2026-01-14
