# Issue #14 - Déploiement GitOps avec ArgoCD 🐙

## 📋 Résumé
L'Issue #14 a mis en place le déploiement continu (GitOps) via ArgoCD. Deux artefacts principaux ont été créés : le manifest de l'application ArgoCD et un script d'installation automatisé.

## ✅ Livrables

### 1. Manifeste ArgoCD (`k8s/argocd/application.yaml`)
Ce fichier configure ArgoCD pour surveiller le dossier `charts/task-manager-api` du dépôt GitHub et synchroniser automatiquement l'état du cluster.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: task-manager
  namespace: argocd
# ... (voir fichier pour détails)
```

### 2. Script d'Installation (`setup_argocd.ps1`)
Un script PowerShell a été créé pour :
- Créer le namespace `argocd`.
- Installer ArgoCD depuis les manifestes officiels.
- Déployer l'application Task Manager dans ArgoCD.

## 🚀 Guide de Déploiement

Puisque l'environnement Minikube local n'était pas actif lors de la configuration, voici la procédure à suivre pour valider le déploiement :

### 1. Démarrer Minikube
```powershell
minikube start
```

### 2. Exécuter l'installation
```powershell
.\setup_argocd.ps1
```

### 3. Accéder à l'interface ArgoCD
Exécutez la commande suivante pour accéder à l'UI :
```powershell
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
- **URL** : https://localhost:8080
- **Username** : `admin`
- **Password** : (Récupérer via la commande ci-dessous)
```powershell
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($input))
```

### 4. Vérifier la Synchronisation
Dans l'interface ArgoCD, l'application `task-manager` doit apparaître. Cliquez sur "Sync" si nécessaire, ou attendez la synchronisation automatique (configurée en auto-sync).

### 5. Test GitOps (Mise à jour)
Pour tester le mécanisme GitOps :
1. Modifiez `charts/task-manager-api/values.yaml` (ex: changez `replicaCount: 1` à `2`).
2. Commitez et pushez les changements (`git push`).
3. Observez ArgoCD : il détectera le changement et mettra à jour le déploiement automatiquement.

## ⚠️ Notes Importantes
- Le `repoURL` dans `application.yaml` pointe vers `https://github.com/NourMoussi/devops-project-.git`. Assurez-vous que ce dépôt est public ou que ArgoCD a les accès nécessaires.
- La synchronisation automatique est activée (`prune: true`, `selfHeal: true`).

---
**Status** : ✅ PRÊT (En attente de démarrage cluster)
**Date** : 2026-01-16
