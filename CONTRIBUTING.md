# Contributing to Task Manager API

Merci de votre intérêt pour contribuer à ce projet ! 🎉

## 📋 Code of Conduct

Ce projet adhère à un code de conduite professionnel. En participant, vous vous engagez à maintenir un environnement respectueux et collaboratif.

## 🚀 Comment Contribuer

### 1. Signaler un Bug

Si vous trouvez un bug, veuillez créer une issue avec :
- **Titre clair** : Décrivez brièvement le problème
- **Description détaillée** : Étapes pour reproduire le bug
- **Comportement attendu** : Ce qui devrait se passer
- **Comportement actuel** : Ce qui se passe réellement
- **Environnement** : OS, version Python, etc.
- **Logs/Screenshots** : Si applicable

### 2. Proposer une Fonctionnalité

Pour proposer une nouvelle fonctionnalité :
1. Créez une issue avec le label `enhancement`
2. Décrivez clairement la fonctionnalité et son utilité
3. Attendez la validation avant de commencer l'implémentation

### 3. Soumettre une Pull Request

#### Workflow Git

```bash
# 1. Fork le projet et clone ton fork
git clone https://github.com/VOTRE-USERNAME/devops-project-.git
cd devops-project-

# 2. Créer une branche pour votre fonctionnalité
git checkout -b feature/nom-de-la-fonctionnalite

# 3. Faire vos modifications et commiter
git add .
git commit -m "feat: description de la fonctionnalité"

# 4. Pousser vers votre fork
git push origin feature/nom-de-la-fonctionnalite

# 5. Ouvrir une Pull Request sur GitHub
```

#### Conventions de Commit

Utilisez le format [Conventional Commits](https://www.conventionalcommits.org/) :

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Modification de documentation
- `style:` Formatage, points-virgules manquants, etc.
- `refactor:` Refactoring de code
- `test:` Ajout ou modification de tests
- `chore:` Tâches de maintenance

**Exemples :**
```
feat: ajout du endpoint DELETE /tasks/<id>
fix: correction de la validation des tâches
docs: mise à jour du README avec exemples API
```

### 4. Standards de Code

#### Python Style Guide

- Suivre [PEP 8](https://pep8.org/)
- Utiliser des noms de variables descriptifs
- Commenter le code complexe
- Maximum 150 lignes pour le fichier principal `app.py`

#### Linting

Avant de soumettre, exécutez :

```bash
# Installer flake8
pip install flake8

# Vérifier le code
flake8 app.py --max-line-length=100
```

### 5. Tests

- Ajoutez des tests pour toute nouvelle fonctionnalité
- Assurez-vous que tous les tests passent avant de soumettre
- Visez une couverture de code > 80%

```bash
# Exécuter les tests
pytest tests/

# Avec couverture
pytest --cov=app tests/
```

### 6. Documentation

- Mettez à jour le README si nécessaire
- Documentez les nouveaux endpoints dans `docs/api.md`
- Ajoutez des docstrings aux fonctions

## 🔍 Processus de Review

1. **Soumission** : Vous ouvrez une Pull Request
2. **CI/CD** : Les tests automatiques s'exécutent
3. **Review** : Un mainteneur examine votre code
4. **Modifications** : Vous apportez les changements demandés
5. **Merge** : Votre PR est fusionnée dans `main`

### Critères d'Acceptation

- ✅ Tous les tests passent
- ✅ Code respecte les standards (PEP 8)
- ✅ Pas de vulnérabilités de sécurité
- ✅ Documentation à jour
- ✅ Commits bien formatés

## 📞 Questions ?

Si vous avez des questions, n'hésitez pas à :
- Ouvrir une issue avec le label `question`
- Contacter le mainteneur via GitHub

## 🙏 Merci !

Vos contributions rendent ce projet meilleur pour tout le monde. Merci de prendre le temps de contribuer ! 🚀

---

**Happy Coding!** 💻
