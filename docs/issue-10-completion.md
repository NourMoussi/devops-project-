# Issue #10 - Déploiement Kubernetes (Manifests) ✅

## 📋 Résumé

L'Issue #10 a été complétée. Les manifestes Kubernetes nécessaires au déploiement de l'application sur un cluster ont été créés.

## ✅ Checklist Complétée

- [x] Créer le répertoire `k8s/`
- [x] Rédiger le manifeste `Deployment` (`k8s/deployment.yaml`)
  - Configuration de 2 réplicas pour la haute disponibilité
  - Limitation des ressources (CPU/Memory)
  - Configuration des sondes de santé (Liveness & Readiness)
- [x] Rédiger le manifeste `Service` (`k8s/service.yaml`)
  - Exposition via NodePort (Port 30000)

## ☸️ Instructions de Déploiement

### Prérequis

- Un cluster Kubernetes (Minikube ou Kind)
- `kubectl` configuré

### 1. Charger l'image (Si local - Minikube)

Si vous utilisez Minikube et n'avez pas poussé l'image sur un registre (Docker Hub), vous devez charger l'image locale dans Minikube :

```bash
minikube image load devops-project-api:latest
```

### 2. Appliquer les manifestes

```bash
# Appliquer le déploiement et le service
kubectl apply -f k8s/
```

### 3. Vérifier le statut

```bash
# Voir les pods
kubectl get pods

# Voir le service
kubectl get svc task-manager-api-service
```

### 4. Accéder à l'application

Si vous utilisez Minikube :

```bash
minikube service task-manager-api-service
```

Ou accédez directement via `http://<MINIKUBE-IP>:30000`.

## 📦 Détails de Configuration

- **Replicas** : 2
- **Strategy** : RollingUpdate
- **Resources** :
  - Requests : 100m CPU / 64Mi RAM
  - Limits : 500m CPU / 256Mi RAM
- **Probes** : HTTP GET sur `/health`

## 📌 Prochaines Étapes

**Issue #11** : Pipeline CI/CD GitHub Actions.
Automatiser le build, les tests et la création de l'image Docker via GitHub Actions.

---

**Status** : ✅ COMPLÉTÉ
**Date** : 2026-01-15
