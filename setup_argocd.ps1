# Vérifier si Minikube est en cours d'exécution
$minikubeStatus = minikube status
if ($minikubeStatus -match "Stopped") {
    Write-Host "Minikube is stopped. Please start it using 'minikube start'."
    exit 1
}

# 1. Créer le namespace argocd
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

# 2. Installer ArgoCD
Write-Host "Installing ArgoCD..."
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 3. Attendre que le serveur ArgoCD soit prêt (optionnel, simple pause ici)
Write-Host "Waiting for ArgoCD components to start..."
# On pourrait utiliser kubectl wait, mais une pause simple pour l'exemple suffit ou on laisse l'utilisateur vérifier.

# 4. Appliquer l'application Task Manager
Write-Host "Deploying Task Manager Application..."
kubectl apply -f k8s/argocd/application.yaml

Write-Host "Setup complete!"
Write-Host "To access ArgoCD UI:"
Write-Host "1. Port-forward: kubectl port-forward svc/argocd-server -n argocd 8080:443"
Write-Host "2. Get Password: kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($input))"
Write-Host "3. Open https://localhost:8080 (Username: admin)"
