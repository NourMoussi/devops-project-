# Plan d'action - Issue #12 : Implémentation DevSecOps 🛡️

## 🎯 Objectif
Sécuriser le pipeline CI/CD en intégrant des analyses de sécurité automatisées pour le code (SAST) et les conteneurs.

## 📋 Étapes à réaliser

### Phase 1 : Analyse Statique (SAST) avec Bandit
- [ ] Installer Bandit localement pour tester
- [ ] Exécuter un audit initial du code : `bandit -r app.py`
- [ ] Créer la configuration Bandit (si nécessaire) pour exclure les faux positifs
- [ ] Ajouter l'étape Bandit dans le workflow GitHub Actions

### Phase 2 : Scan des Dépendances
- [ ] Installer `pip-audit`
- [ ] Vérifier les vulnérabilités des dépendances actuelles
- [ ] Ajouter l'étape de scan de dépendances dans le workflow

### Phase 3 : Container Scanning avec Trivy
- [ ] Intégrer l'action Trivy dans le workflow après le build Docker
- [ ] Configurer le scan pour échouer sur les vulnérabilités "CRITICAL"

### Phase 4 : Documentation
- [ ] Créer `docs/security-report.md`
- [ ] Documenter les résultats des scans initiaux
- [ ] Mettre à jour `README.md` avec des badges de sécurité (si disponibles)

## 🛠️ Outils utilisés
- **Bandit** : Sécurité du code Python
- **Pip-audit** : Vulnérabilités des packages Python
- **Trivy** : Sécurité des images Docker

---
**Status** : ⏳ En cours
