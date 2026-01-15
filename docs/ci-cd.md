# Documentation CI/CD Pipeline 🚀

## 📋 Vue d'Ensemble

Ce document décrit le pipeline CI/CD complet mis en place avec **GitHub Actions** pour automatiser le développement, les tests et le déploiement de l'application Task Manager API.

## 🏗️ Architecture du Pipeline

Le pipeline est organisé en **3 jobs** principaux qui s'exécutent séquentiellement :

```
┌─────────────────────────────────────────────────────────┐
│         Trigger : Push/PR sur main ou Release           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│        Job 1: Linting & Tests (Python 3.11)             │
│  ✅ Checkout du code                                    │
│  ✅ Installation de Python                              │
│  ✅ Mise en cache des dépendances pip                   │
│  ✅ Installation des dépendances                        │
│  ✅ Linting avec flake8                                 │
│  ✅ Tests unitaires avec pytest                         │
│  ✅ Rapport de couverture de code                       │
└────────────────────┬────────────────────────────────────┘
                     │ (depends_on: test)
                     ▼
┌─────────────────────────────────────────────────────────┐
│      Job 2: Build & Push Docker Image                   │
│  ✅ Checkout du code                                    │
│  ✅ Login Docker Hub (secrets)                          │
│  ✅ Extraction des métadonnées (tags)                   │
│  ✅ Build de l'image Docker                             │
│  ✅ Tag: latest + SHA commit                            │
│  ✅ Push vers Docker Hub                                │
└────────────────────┬────────────────────────────────────┘
                     │ (optionnel, commenté)
                     ▼
┌─────────────────────────────────────────────────────────┐
│       Job 3: Deploy to Kubernetes (Optionnel)           │
│  ⚠️  Setup kubectl                                      │
│  ⚠️  Configuration kubeconfig                           │
│  ⚠️  Déploiement sur cluster K8s                        │
│  ⚠️  Vérification du rollout                            │
└─────────────────────────────────────────────────────────┘
```

## 🔔 Déclencheurs (Triggers)

Le pipeline se déclenche automatiquement dans les cas suivants :

### 1. Push sur la branche `main`
```yaml
on:
  push:
    branches:
      - main
```
- Exécute **tous les jobs** (test, build, push)
- L'image Docker est construite et poussée vers Docker Hub

### 2. Pull Request vers `main`
```yaml
on:
  pull_request:
    branches:
      - main
```
- Exécute **uniquement le job de test**
- Vérifie que les tests passent avant merge
- N'effectue pas de build/push Docker

### 3. Publication d'une Release
```yaml
on:
  release:
    types: [published]
```
- Exécute tous les jobs
- Tag l'image avec la version de la release

## 📦 Jobs Détaillés

### Job 1 : Linting & Tests 🧪

**Objectif** : Vérifier la qualité du code et s'assurer que tous les tests passent.

**Étapes :**

1. **Checkout du code** (`actions/checkout@v4`)
   - Récupère le code source du repository

2. **Setup Python 3.11** (`actions/setup-python@v5`)
   - Installation de Python 3.11
   - Configuration de la mise en cache pip pour accélérer les builds

3. **Installation des dépendances**
   ```bash
   pip install -r requirements.txt
   pip install flake8 pytest pytest-cov
   ```

4. **Linting avec flake8**
   - Détection des erreurs de syntaxe Python
   - Vérification de la complexité du code
   - Respect des conventions PEP 8
   
   **Règles appliquées :**
   - `E9` : Erreurs de syntaxe
   - `F63, F7, F82` : Noms non définis

5. **Tests unitaires avec pytest**
   ```bash
   pytest test_api.py -v --cov=. --cov-report=term-missing --cov-report=xml
   ```
   - Exécution de tous les tests
   - Génération d'un rapport de couverture

6. **Upload du rapport de couverture** (optionnel)
   - Envoi vers Codecov pour suivi de la couverture

**Sortie attendue :**
```
✅ All tests passed (10/10)
✅ Code coverage: 85%
✅ No linting errors
```

---

### Job 2 : Build & Push Docker Image 🐳

**Objectif** : Construire l'image Docker et la pousser vers Docker Hub.

**Conditions d'exécution :**
- ✅ Job `test` réussi (`needs: test`)
- ✅ Push sur la branche `main`
- ✅ N'est **PAS** déclenché sur les Pull Requests

**Étapes :**

1. **Checkout du code**

2. **Login Docker Hub** (`docker/login-action@v3`)
   ```yaml
   with:
     username: ${{ secrets.DOCKER_USERNAME }}
     password: ${{ secrets.DOCKER_PASSWORD }}
   ```
   - Utilise les secrets GitHub configurés
   - Token sécurisé (jamais affiché dans les logs)

3. **Extraction des métadonnées** (`docker/metadata-action@v5`)
   - Génère automatiquement les tags :
     - `latest` : Dernière version stable
     - `main-<sha>` : Hash du commit (traçabilité)
     - `<branch-name>` : Nom de la branche

4. **Build et Push** (`docker/build-push-action@v5`)
   ```yaml
   with:
     context: .
     file: ./Dockerfile
     push: true
     tags: ${{ steps.meta.outputs.tags }}
   ```
   - Build multi-stage optimisé
   - Push automatique vers Docker Hub

**Sortie attendue :**
```
✅ Image built successfully
✅ Image size: ~150MB
✅ Pushed to: username/devops-project-api:latest
✅ Pushed to: username/devops-project-api:main-abc1234
```

---

### Job 3 : Deploy to Kubernetes (Optionnel) ☸️

**Status** : Actuellement **commenté** dans le workflow.

**Objectif** : Déployer automatiquement sur un cluster Kubernetes.

**Étapes (si activé) :**

1. Setup kubectl
2. Configuration du kubeconfig (via secret)
3. Déploiement : `kubectl apply -f k8s/`
4. Vérification : `kubectl rollout status deployment/task-manager-api`

**Pour activer ce job :**
1. Créer le secret `KUBECONFIG` (base64 du fichier kubeconfig)
2. Décommenter les lignes dans `.github/workflows/ci-cd.yml`

## 🔐 Secrets GitHub Requis

Les secrets suivants doivent être configurés dans `Settings → Secrets and variables → Actions` :

| Secret | Description | Requis | Comment l'obtenir |
|--------|-------------|--------|-------------------|
| `DOCKER_USERNAME` | Nom d'utilisateur Docker Hub | ✅ Oui | Votre username Docker Hub |
| `DOCKER_PASSWORD` | Token d'accès Docker Hub | ✅ Oui | [hub.docker.com/settings/security](https://hub.docker.com/settings/security) |
| `KUBECONFIG` | Configuration Kubernetes (base64) | ⚠️ Optionnel | `cat ~/.kube/config \| base64` |

### Comment créer un token Docker Hub

1. Se connecter sur [hub.docker.com](https://hub.docker.com)
2. Aller dans **Account Settings → Security**
3. Cliquer sur **New Access Token**
4. Nommer le token : `github-actions-devops-project`
5. Sélectionner les permissions : **Read & Write**
6. Copier le token (ne sera affiché qu'une fois !)
7. L'ajouter dans GitHub : `Settings → Secrets → New repository secret`

## 📊 Monitoring et Logs

### Visualiser les Workflows

1. Aller dans l'onglet **Actions** du repository GitHub
2. Sélectionner un workflow pour voir les détails
3. Cliquer sur un job pour voir les logs détaillés

### Badge de Statut

Le badge dans le README affiche le statut en temps réel :

```markdown
![CI/CD](https://github.com/NourMoussi/devops-project-/workflows/CI/CD%20Pipeline/badge.svg)
```

- 🟢 **Vert** : Tous les jobs réussis
- 🔴 **Rouge** : Au moins un job a échoué
- 🟡 **Jaune** : Workflow en cours d'exécution

## 🔧 Configuration Avancée

### Mise en Cache des Dépendances

Le workflow utilise automatiquement la mise en cache pip :

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'  # ← Mise en cache automatique
```

**Avantages :**
- Réduction du temps de build (~30-50%)
- Moins de consommation de bande passante

### Variables d'Environnement

Définies au niveau du workflow :

```yaml
env:
  PYTHON_VERSION: '3.11'
  DOCKER_IMAGE: devops-project-api
```

## 🐛 Guide de Dépannage

### Erreur : "Authentication failed" (Docker)

**Cause** : Secrets Docker Hub incorrects ou expirés

**Solution :**
1. Vérifier que `DOCKER_USERNAME` et `DOCKER_PASSWORD` sont bien configurés
2. Régénérer un nouveau token Docker Hub
3. Mettre à jour les secrets dans GitHub

---

### Erreur : "Tests failed"

**Cause** : Un ou plusieurs tests unitaires échouent

**Solution :**
1. Consulter les logs du job `test`
2. Reproduire l'erreur en local :
   ```bash
   pytest test_api.py -v
   ```
3. Corriger le code
4. Commiter et pusher la correction

---

### Erreur : "flake8 linting errors"

**Cause** : Le code ne respecte pas les conventions PEP 8

**Solution :**
1. Exécuter flake8 en local :
   ```bash
   flake8 . --show-source --statistics
   ```
2. Corriger les erreurs signalées
3. Optionnel : Utiliser `black` pour formater automatiquement :
   ```bash
   pip install black
   black .
   ```

---

### Workflow ne se déclenche pas

**Causes possibles :**
1. GitHub Actions désactivé dans le repository
2. Fichier `.github/workflows/ci-cd.yml` mal formaté
3. Branch protégée

**Solution :**
1. Vérifier `Settings → Actions → General` : "Allow all actions"
2. Valider le YAML : https://www.yamllint.com/
3. Vérifier les règles de protection de branche

## 📈 Métriques et Performances

### Temps d'Exécution Typique

| Job | Durée Moyenne | Cache Hit | Cache Miss |
|-----|---------------|-----------|------------|
| Test | ~1-2 min | ~45s | ~1m30s |
| Build & Push | ~2-3 min | ~2min | ~3min |
| **Total** | **~3-5 min** | **~2m45s** | **~4m30s** |

### Optimisations Futures

- [ ] Parallélisation des tests
- [ ] Utilisation de Docker layer caching
- [ ] Matrix build pour plusieurs versions Python
- [ ] Tests d'intégration automatisés

## 🔗 Ressources Utiles

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Setup Python Action](https://github.com/actions/setup-python)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Pytest Documentation](https://docs.pytest.org/)

## 📝 Changelog

| Version | Date | Modifications |
|---------|------|---------------|
| 1.0.0 | 2026-01-15 | Pipeline initial (test, build, push) |
| 1.1.0 | TBD | Ajout du déploiement K8s automatique |

---

**Auteur** : Nour Moussi  
**Dernière mise à jour** : 2026-01-15  
**Status** : ✅ Production Ready
