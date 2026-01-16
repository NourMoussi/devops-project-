# Issue #14 - Déploiement GitOps avec ArgoCD 🐙

## 📋 Objectif
Automatiser le déploiement de l'application sur le cluster Kubernetes en utilisant une approche GitOps avec ArgoCD.

## 📝 Tâches

- [ ] **Installation d'ArgoCD** : Installer ArgoCD sur le cluster Minikube (namespace `argocd`).
- [ ] **Configuration de l'Application** : Créer le manifeste `k8s/argocd/application.yaml` pointant vers le dossier `charts/task-manager-api`.
- [ ] **Déploiement** : Appliquer la configuration sur le cluster.
- [ ] **Vérification** : S'assurer que l'application est "Healthy" et "Synced".
- [ ] **Documentation** : Documenter l'accès à l'UI ArgoCD et le workflow.

## 🛠️ Détails Techniques

### Manifeste ArgoCD (`k8s/argocd/application.yaml`)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: task-manager
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/NourMoussi/devops-project-.git'
    targetRevision: HEAD
    path: charts/task-manager-api
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## 🚀 Critères d'Acceptation
1. ArgoCD est installé et accessible.
2. L'application `task-manager` apparaît dans ArgoCD.
3. Les pods de l'application sont déployés avec succès par ArgoCD.
