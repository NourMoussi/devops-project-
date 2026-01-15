# Issue #11 - Pipeline CI/CD GitHub Actions 🚀

## 🎯 Objectif

Mettre en place un pipeline CI/CD complet avec GitHub Actions pour automatiser le processus de développement, de test et de déploiement de l'application Task Manager.

## 📋 Tâches à Réaliser

### 1. ✅ Créer le Workflow Principal (`.github/workflows/ci-cd.yml`)

Le pipeline doit inclure les étapes suivantes :

#### **Stage 1 : Linting et Tests**
- [ ] Checkout du code source
- [ ] Configuration de Python 3.11
- [ ] Installation des dépendances (`pip install -r requirements.txt`)
- [ ] Linting avec `flake8` (vérification de la qualité du code)
- [ ] Exécution des tests unitaires avec `pytest`
- [ ] Génération d'un rapport de couverture de code

#### **Stage 2 : Build et Push Docker**
- [ ] Login vers Docker Hub (utilisation des secrets GitHub)
- [ ] Construction de l'image Docker avec tag versionnée
- [ ] Tag automatique avec `latest` et version
- [ ] Push de l'image vers Docker Hub
- [ ] Vérification de la taille de l'image

#### **Stage 3 : Déploiement (Optionnel - Phase 2)**
- [ ] Configuration de `kubectl` avec secrets
- [ ] Déploiement sur cluster Kubernetes
- [ ] Vérification du statut du déploiement
- [ ] Tests de fumée (smoke tests)

### 2. 🔐 Configuration des Secrets GitHub

Ajouter les secrets suivants dans les paramètres du repository GitHub :

| Secret | Description | Requis |
|--------|-------------|--------|
| `DOCKER_USERNAME` | Nom d'utilisateur Docker Hub | ✅ Oui |
| `DOCKER_PASSWORD` | Token d'accès Docker Hub | ✅ Oui |
| `KUBECONFIG` | Configuration Kubernetes base64 | ⚠️ Optionnel |

**Instructions pour créer un token Docker Hub :**
1. Aller sur https://hub.docker.com/settings/security
2. Cliquer sur "New Access Token"
3. Nommer le token (ex: "github-actions")
4. Copier le token et l'ajouter aux secrets GitHub

### 3. 🔔 Configuration des Déclencheurs (Triggers)

Le pipeline doit se déclencher sur :

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  release:
    types: [published]
```

### 4. 📊 Badges et Documentation

- [ ] Ajouter un badge de statut CI dans le `README.md`
- [ ] Ajouter un badge de couverture de code
- [ ] Documenter le processus CI/CD dans `docs/ci-cd.md`
- [ ] Créer un diagramme du pipeline

## 📦 Livrables Attendus

1. **Fichier de workflow** : `.github/workflows/ci-cd.yml`
   - Configuration complète du pipeline
   - Jobs séparés pour linting, tests, build et push

2. **Documentation CI/CD** : `docs/ci-cd.md`
   - Explication détaillée du pipeline
   - Guide de dépannage
   - Exemples de logs

3. **README mis à jour** : `README.md`
   - Badge de statut du workflow
   - Section "CI/CD Pipeline"
   - Instructions pour les contributeurs

4. **Rapport de complétion** : `docs/issue-11-completion.md`
   - Résumé des modifications
   - Captures d'écran des workflows réussis
   - Logs de déploiement

## ✅ Critères d'Acceptation

- ✅ Le pipeline s'exécute automatiquement à chaque push sur `main`
- ✅ Le pipeline s'exécute sur les Pull Requests
- ✅ Les tests passent avec succès (tous les tests unitaires)
- ✅ L'image Docker est construite sans erreur
- ✅ L'image est poussée vers Docker Hub avec les bons tags
- ✅ Le badge CI affiche le statut correct dans le README
- ✅ La documentation est claire et complète
- ✅ Le workflow échoue correctement en cas d'erreur de tests ou de build

## 🏗️ Architecture du Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Push/PR                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Job 1: Linting & Tests                     │
│  • Checkout code                                        │
│  • Setup Python 3.11                                    │
│  • Install dependencies                                 │
│  • Run flake8                                           │
│  • Run pytest                                           │
│  • Generate coverage report                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         Job 2: Build & Push Docker Image                │
│  • Checkout code                                        │
│  • Login to Docker Hub                                  │
│  • Build Docker image                                   │
│  • Tag image (latest + version)                         │
│  • Push to Docker Hub                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         Job 3: Deploy (Optionnel)                       │
│  • Setup kubectl                                        │
│  • Apply k8s manifests                                  │
│  • Verify deployment                                    │
└─────────────────────────────────────────────────────────┘
```

## 🔗 Ressources Utiles

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build and Push Action](https://github.com/docker/build-push-action)
- [Python Setup Action](https://github.com/actions/setup-python)
- [Kubernetes Actions](https://github.com/marketplace/actions/kubernetes-cli-kubectl)

## 📌 Dépendances

- ✅ Issue #10 (Manifestes Kubernetes) - Complétée
- ✅ Compte Docker Hub configuré
- ✅ Repository GitHub avec accès aux Actions
- ⚠️ Secrets GitHub à configurer

## 🚀 Plan d'Exécution

### Phase 1 : Configuration de Base (Prioritaire)
1. Créer la structure `.github/workflows/`
2. Implémenter le job de linting et tests
3. Configurer les secrets Docker Hub
4. Implémenter le job de build et push Docker

### Phase 2 : Documentation et Badges
1. Ajouter les badges dans le README
2. Créer la documentation CI/CD complète
3. Tester le workflow sur une Pull Request

### Phase 3 : Déploiement Automatique (Optionnel)
1. Configurer les secrets Kubernetes
2. Implémenter le job de déploiement
3. Ajouter des tests de fumée post-déploiement

---

**Labels** : `enhancement`, `ci/cd`, `devops`, `priority:high`  
**Milestone** : Sprint 3 - Automatisation  
**Estimation** : 3-4 heures  
**Status** : 📋 EN PLANIFICATION
