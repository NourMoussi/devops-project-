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

## ✅ Vérification du Déploiement

Le déploiement a été testé et vérifié avec succès sur Minikube :

### État du Cluster
```bash
$ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
task-manager-api-6bdb68f5b6-b...    1/1     Running   0          2m
task-manager-api-6bdb68f5b6-x...    1/1     Running   0          2m

$ kubectl get svc
NAME                       TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
task-manager-api-service   NodePort   10.96.xxx.xxx   <none>        80:30000/TCP   2m
```

### Tests de l'API
- ✅ **Health Check** : `GET /health` → `{"status":"healthy","version":"1.0.0"}`
- ✅ **Liste des tâches** : `GET /tasks` → Retourne les tâches avec succès
- ✅ **Métriques Prometheus** : `GET /metrics` → Métriques disponibles

### Commandes Utilisées
```bash
# Démarrer Minikube
minikube start --driver=docker

# Charger l'image dans Minikube
docker tag task-manager-api:latest devops-project-api:latest
minikube image load devops-project-api:latest

# Déployer l'application
kubectl apply -f k8s/

# Accéder au service
minikube service task-manager-api-service --url
# → http://127.0.0.1:49281
```

## 📌 Prochaines Étapes

**Issue #11** : Pipeline CI/CD GitHub Actions.
Automatiser le build, les tests et la création de l'image Docker via GitHub Actions.

---

**Status** : ✅ COMPLÉTÉ et VÉRIFIÉ
**Date** : 2026-01-15
