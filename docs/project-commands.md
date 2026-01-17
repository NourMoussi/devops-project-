# 📘 Gestionnaire de Tâches - Guide des Commandes du Projet

Ce document regroupe toutes les commandes essentielles pour configurer, développer, tester et déployer le projet **Task Manager API**.

## 1. 🛠️ Configuration de l'environnement (Local)

### Prérequis
Assurez-vous d'avoir installé : Python 3.9+, Docker, Minikube, et kubectl.

### Création et activation de l'environnement virtuel
```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### Installation des dépendances
```powershell
# Installer les dépendances du projet
pip install -r requirements.txt

# Installer les outils de développement/test
pip install pytest pytest-cov flake8 black
```

---

## 2. 💻 Développement & Tests

### Lancer l'application localement (Python)
```powershell
# Lancer l'API sur http://localhost:5000
python app.py
```

### Exécuter les tests unitaires et le linting
```powershell
# Lancer tous les tests avec Pytest
pytest

# Lancer les tests avec un rapport de couverture
pytest --cov=. --cov-report=term-missing

# Vérifier la qualité du code (Linting)
flake8 .
```

---

## 3. 🐳 Docker

### Construire l'image Docker
```powershell
# Construire l'image (tag: latest)
docker build -t task-manager-api .

# Construire avec un tag spécifique
docker build -t moussinour/todo:tagname .
```

### Lancer le conteneur localement
```powershell
# Lancer le conteneur sur le port 5000
docker run -p 5000:5000 --name task-manager task-manager-api
```

### Pousser sur Docker Hub
```powershell
# Se connecter à Docker Hub
docker login

# Pousser l'image
docker push moussinour/todo:latest
```

---

## 4. ☸️ Kubernetes (Minikube)

### Démarrer le cluster
```powershell
# Démarrer Minikube
minikube start

# Vérifier le statut
minikube status
```

### Déploiement
```powershell
# Charger l'image locale dans Minikube (si nécessaire pour tester sans push)
minikube image load moussinour/todo:latest

# Appliquer les configurations Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Vérification et Accès
```powershell
# Voir les Pods
kubectl get pods

# Voir les Services
kubectl get svc

# Accéder au service (Méthode Recommandée - Plus stable)
# Cela redirige le port 80 du service vers le port 9090 de votre machine (8080 est souvent occupé)
kubectl port-forward service/task-manager-api-service 9090:80

# Ensuite, accédez à : http://localhost:9090/health

# Méthode alternative (Minikube Tunnel)
# Attention : Cette commande doit rester ouverte dans un terminal séparé pour fonctionner
minikube service task-manager-api-service --url
```

### Logs et Debug
```powershell
# Voir les logs d'un pod spécifique
kubectl logs <nom-du-pod>

# Suivre les logs en direct
kubectl logs -f <nom-du-pod>

# Debug : Décrire le déploiement pour voir les erreurs
kubectl describe deployment task-manager-api
```

---

## 5. 🛡️ Qualité & Sécurité (DevSecOps)

### Scan de vulnérabilités (Trivy)
```powershell
# Scanner l'image Docker
trivy image moussinour/todo:latest
```

### Analyse Statique (SAST - Bandit)
```powershell
# Analyser le code Python
bandit -r . -x ./venv
```

### Audit des dépendances
```powershell
# Vérifier les vulnérabilités des paquets pip
pip-audit
```

---

## 6. 🚀 CI/CD (GitHub Actions)

Le pipeline CI/CD est automatisé dans `.github/workflows/ci-cd.yml`.

### Déclencher le pipeline
```powershell
# Ajouter, commiter et pousser les changements
git add .
git commit -m "Message du commit"
git push origin main
```
