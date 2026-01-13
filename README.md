# 📋 Task Manager API - DevOps Project

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

## 📖 Description

**Task Manager API** est un projet DevOps académique complet démontrant les meilleures pratiques de développement, déploiement et observabilité d'une application moderne.

Ce projet implémente une API REST simple de gestion de tâches (TODO list) avec un focus sur :
- 🚀 **CI/CD automatisé** avec GitHub Actions
- 🐳 **Containerisation** Docker optimisée
- ☸️ **Orchestration** Kubernetes (minikube/kind)
- 📊 **Observabilité** complète (métriques, logs, tracing)
- 🔒 **Sécurité** avec scans SAST et DAST
- 📚 **Documentation** professionnelle

## 🎯 Objectifs du Projet

Ce projet a été conçu pour démontrer :

1. **Développement Backend** : API REST en Python/Flask (< 150 lignes)
2. **Workflow Git** : Issues, Pull Requests, Code Reviews
3. **Pipeline CI/CD** : Tests, Build, Scan, Deploy automatisés
4. **Containerisation** : Docker multi-stage, optimisation d'images
5. **Kubernetes** : Déploiement, scaling, health checks
6. **Observabilité** : Métriques Prometheus, logs structurés JSON
7. **Sécurité** : Analyse statique (SAST) et dynamique (DAST)

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│   Task Manager API (Flask)  │
│  ┌─────────────────────────┐│
│  │  REST Endpoints         ││
│  │  - GET/POST/PUT/DELETE  ││
│  └─────────────────────────┘│
│  ┌─────────────────────────┐│
│  │  Observability          ││
│  │  - Metrics (/metrics)   ││
│  │  - Structured Logs      ││
│  │  - Request Tracing      ││
│  └─────────────────────────┘│
│  ┌─────────────────────────┐│
│  │  In-Memory Storage      ││
│  └─────────────────────────┘│
└─────────────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│   Monitoring Stack          │
│   - Prometheus              │
│   - Grafana (optionnel)     │
└─────────────────────────────┘
```

## 🚀 Quick Start

### Prérequis

- Python 3.9+
- Docker & Docker Compose
- Git
- kubectl (pour Kubernetes)
- minikube ou kind (pour déploiement local K8s)

### Installation Locale

```bash
# Cloner le repository
git clone https://github.com/NourMoussi/devops-project-.git
cd devops-project-

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

L'API sera accessible sur `http://localhost:5000`

## 📚 Documentation

- [Guide de Contribution](CONTRIBUTING.md)
- [Documentation API](docs/api.md) *(à venir)*
- [Guide de Déploiement](docs/deployment.md) *(à venir)*
- [Rapport de Sécurité](docs/security-report.md) *(à venir)*

## 🛠️ Stack Technique

- **Backend** : Python 3.9+, Flask 3.0+
- **Observabilité** : prometheus-client, structlog
- **Containerisation** : Docker, Docker Compose
- **Orchestration** : Kubernetes (minikube/kind)
- **CI/CD** : GitHub Actions
- **Sécurité** : Bandit (SAST), OWASP ZAP (DAST), Trivy (scan Docker)
- **Tests** : pytest, coverage

## 📝 API Endpoints

*(Documentation complète à venir)*

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | Health check de l'application |
| GET | `/metrics` | Métriques Prometheus |
| GET | `/tasks` | Liste toutes les tâches |
| POST | `/tasks` | Créer une nouvelle tâche |
| GET | `/tasks/<id>` | Récupérer une tâche spécifique |
| PUT | `/tasks/<id>` | Mettre à jour une tâche |
| DELETE | `/tasks/<id>` | Supprimer une tâche |

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez consulter [CONTRIBUTING.md](CONTRIBUTING.md) pour les détails.

### Workflow de Contribution

1. Créer une issue décrivant la fonctionnalité/bug
2. Créer une branche depuis `main` : `git checkout -b feature/ma-fonctionnalite`
3. Commiter les changements : `git commit -m "feat: ajout de ma fonctionnalité"`
4. Pousser la branche : `git push origin feature/ma-fonctionnalite`
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Nour Moussi**
- GitHub: [@NourMoussi](https://github.com/NourMoussi)
- Projet: [devops-project-](https://github.com/NourMoussi/devops-project-)

## 🙏 Remerciements

Projet réalisé dans le cadre d'un cours DevOps académique démontrant les meilleures pratiques de l'industrie.

---

⭐ **N'hésitez pas à mettre une étoile si ce projet vous a été utile !**
