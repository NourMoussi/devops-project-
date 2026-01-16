# 🚀 Guide de Déploiement

Ce guide détaille les différentes méthodes pour déployer l'API Task Manager.

## 1. Local (Développement)
Pour exécuter l'application localement sans conteneurs :

```bash
# Windows
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## 2. Docker Compose
Pour lancer la stack complète (App + Prometheus) :

```bash
docker-compose up -d --build
```
L'API sera accessible sur `http://localhost:5000`.

## 3. Kubernetes avec Helm
Pour déployer manuellement sur un cluster Kubernetes :

```bash
helm install task-manager charts/task-manager-api
```

## 4. GitOps avec ArgoCD (Recommandé pour la Prod)
Nous utilisons ArgoCD pour la synchronisation automatique.

### Prérequis
- Cluster Kubernetes (Minikube, Kind, ou Cloud)
- CLI `kubectl` configuré

### Installation Automatique
Utilisez le script fourni à la racine du projet :

```powershell
.\setup_argocd.ps1
```

### Installation Manuelle
1. **Installer ArgoCD** :
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

2. **Déployer l'Application** :
   ```bash
   kubectl apply -f k8s/argocd/application.yaml
   ```

### Accès Interface ArgoCD
```bash
# Port-forwarding
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
Accédez à `https://localhost:8080`.
- **User**: `admin`
- **Password**:
  ```bash
  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
  ```

### Vérification
Une fois déployée, l'application devrait être en statut `Synced` et `Healthy` dans ArgoCD.
Toute modification sur la branche `main` du dépôt Git sera automatiquement déployée.
