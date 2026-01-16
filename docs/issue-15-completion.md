# Issue #15 - Configuration Scan DAST (OWASP ZAP) 🛡️

## 📋 Résumé
L'Issue #15 a été complétée. Nous avons intégré un scan de sécurité dynamique (DAST) utilisant **OWASP ZAP** directement dans le pipeline CI/CD GitHub Actions.

## ✅ Livrables

### 🛡 Job DAST (`.github/workflows/ci-cd.yml`)
Un nouveau job `dast` a été ajouté au pipeline. Il s'exécute après le build Docker et effectue les opérations suivantes :
1. **Démarrage de l'Application** : Lance le conteneur Docker `task-manager-api` fraîchement construit.
2. **Scan ZAP Baseline** : Utilise l'action `zaproxy/action-baseline` pour scanner `http://localhost:5000` (spidering passif).
3. **Archivage des Rapports** : Les rapports (HTML, JSON, MD) sont sauvegardés comme artefacts GitHub.

### ⚙️ Configuration
- **Cible** : `http://localhost:5000`
- **Fail Action** : `false` (Pour l'instant, le pipeline n'échoue pas en cas d'alerte, permettant une phase d'apprentissage/triage).
- **Règles** : Utilise la configuration par défaut (Baseline).

## 🚀 Utilisation
À chaque push sur `main`, l'application est scannée automatiquement.
Pour voir les résultats :
1. Allez dans l'onglet **Actions** du dépôt GitHub.
2. Sélectionnez le workflow exécuté.
3. Téléchargez l'artefact `zap-scan-report`.

---
**Status** : ✅ COMPLÉTÉ
**Date** : 2026-01-16
