# Rapport de Sécurité (DevSecOps) 🛡️

## 🎯 Objectif
Ce document détaille la stratégie de sécurité automatisée mise en place dans le pipeline CI/CD pour garantir l'intégrité et la sécurité de l'application **Task Manager API**.

## 🛠️ Outils et Configuration

### 1. Analyse Statique (SAST) - Bandit
* **Outil** : [Bandit](https://bandit.readthedocs.io/)
* **Cible** : Code source Python (`.py`)
* **Intégration** : Job `security` dans GitHub Actions
* **Configuration** :
  * Exclusions : Tests (`test_*.py`), Environnement virtuel (`venv/`)
  * Sévérité bloquante : `MEDIUM` et `HIGH`
  * Exceptions : `B104` (Bind on 0.0.0.0) autorisé explicitement pour Docker.

### 2. Audit des Dépendances - Pip-audit
* **Outil** : [pip-audit](https://pypi.org/project/pip-audit/)
* **Cible** : `requirements.txt` et environnement installé
* **Intégration** : Job `security` dans GitHub Actions
* **Fonctionnement** : Vérifie les packages installés contre la base de données de vulnérabilités PyPI (OSV).

### 3. Scan de Conteneur - Trivy
* **Outil** : [Trivy](https://github.com/aquasecurity/trivy)
* **Cible** : Image Docker finale
* **Intégration** : Job `build-and-push`
* **Configuration** :
  * Sévérités bloquantes : `CRITICAL`, `HIGH`
  * Ignore les vulnérabilités non corrigées (unfixed)
  * Types de scan : OS (système) et Librairies (Python)

## 📊 Résultats des Scans Initiaux (Exemple)

### Bandit (Code)
```text
Run started:2026-01-15 17:45:00
Total lines of code: 187
Total issues (by severity):
  Undefined: 0
  Low: 0
  Medium: 0 (Après exclusion B104)
  High: 0
Confidence: Total
```

### Pip-audit (Dépendances)
```text
Found 0 known vulnerabilities.
```
*(Après mise à jour de Werkzeug >= 3.0.3)*

### Trivy (Image Docker)
```text
image: devops-project-api:test
Total: 0 (CRITICAL: 0, HIGH: 0)
```

## 🚨 Gestion des Incidents

Si le pipeline échoue pour raison de sécurité :

1. **Identifier la faille** dans les logs GitHub Actions.
2. **Analyser la sévérité** et l'impact réel.
3. **Corriger** :
   * Code : Modifier le code incriminé.
   * Dépendance : Mettre à jour `requirements.txt`.
   * Image de base : Mettre à jour `Dockerfile` (`FROM python:3.9-slim` plus récent).
4. **Faux Positif ?** :
   * Ajouter un commentaire `# nosec` (Bandit).
   * Ajouter au fichier `.trivyignore`.

---
**Dernière mise à jour** : 2026-01-15
**Responsable** : Equipe DevOps
