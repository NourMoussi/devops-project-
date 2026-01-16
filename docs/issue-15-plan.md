# Issue #15 - Configuration Scan DAST (OWASP ZAP) 🛡️

## 📋 Objectif
Intégrer une analyse de sécurité dynamique (DAST) dans le pipeline CI/CD pour détecter les vulnérabilités de l'application en cours d'exécution (XSS, Injection SQL, mauvaises configurations, etc.).

## 📝 Tâches

- [ ] **Mise à jour du Pipeline CI/CD** : Ajouter un job `dast-scan` dans `.github/workflows/ci-cd.yml`.
- [ ] **Lancement de l'Application** : Configurer le job pour démarrer l'application (conteneur Docker) avant le scan.
- [ ] **Scan OWASP ZAP** : Utiliser `zaproxy/action-baseline` pour scanner l'application.
- [ ] **Gestion des Rapports** : Publier le rapport de scan comme artefact GitHub.
- [ ] **Documentation** : Mettre à jour `docs/security-report.md` avec les infos sur le DAST.

## 🛠️ Détails Techniques

### Configuration ZAP (Baseline Scan)
Nous utiliserons le "Baseline Scan" qui est plus rapide et adapté au CI/CD qu'un "Full Scan". Il vérifie les en-têtes de sécurité, les cookies, et effectue une exploration passive (spidering).

```yaml
  dast:
    name: 🛡️ DAST (OWASP ZAP)
    runs-on: ubuntu-latest
    needs: build-and-push
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🐳 Run Application Container
        run: |
          docker run -d -p 5000:5000 --name task-manager nourmoussi/devops-project-api:test
          sleep 10 # Wait for app startup

      - name: 🧟 Run ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.11.0
        with:
          target: 'http://localhost:5000'
          # Fail only on High severity
          fail_action: false 
          allow_issue_writing: false
```

## 🚀 Critères d'Acceptation
1. Le pipeline CI/CD contient une étape DAST fonctionnelle.
2. Le scan s'exécute contre l'application lancée.
3. Un rapport de vulnérabilité est généré.
