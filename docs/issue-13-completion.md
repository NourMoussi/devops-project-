# Issue #13 - Packaging Helm pour Kubernetes ☸️

## 📋 Résumé
L'Issue #13 a été complétée. Nous avons créé un **Chart Helm** complet pour l'API Task Manager, permettant son déploiement rapide et configurable sur n'importe quel cluster Kubernetes.

## ✅ Livrables

### 📦 Structure du Chart
Le chart a été créé dans le répertoire `charts/task-manager-api` avec la structure standard :

```
charts/task-manager-api/
├── Chart.yaml          # Métadonnées du chart (Version 0.1.0)
├── values.yaml         # Configuration par défaut
└── templates/          # Modèles Kubernetes
    ├── deployment.yaml # Définition des Pods/Replicas
    ├── service.yaml    # Exposition réseau (Service)
    ├── _helpers.tpl    # Fonctions utilitaires
    └── serviceaccount.yaml # Compte de service
```

### ⚙️ Configuration Par Défaut (`values.yaml`)
- **Image** : `nourmoussi/devops-project-api:latest`
- **Port** : 5000 (ClusterIP)
- **Répliques** : 1 (configurable)
- **Ressources** : Limites CPU (250m) et Mémoire (256Mi) définies.
- **Probes** : Health checks configurés sur le endpoint `/health`.
- **Environnement** : `FLASK_DEBUG=0` par défaut.

## 🚀 Utilisation

### Installation
Pour installer le chart sur un cluster :
```bash
helm install task-manager charts/task-manager-api
```

### Validation
Le chart a été validé syntaxiquement :
```bash
helm lint charts/task-manager-api
# ==> Linting charts/task-manager-api
# 1 chart(s) linted, 0 chart(s) failed
```

### Rendu (Dry-Run)
Pour visualiser les manifestes générés sans installer :
```bash
helm template debug-release charts/task-manager-api
```

---
**Status** : ✅ COMPLÉTÉ
**Date** : 2026-01-16
