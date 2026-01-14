# Issue #7 - Tracing & Logging ✅

## 📋 Résumé

L'Issue #7 a été complétée. Chaque requête est maintenant identifiée par un ID unique, propagé à travers les logs et la réponse HTTP.

## ✅ Checklist Complétée

- [x] Implémenter un filtre de logging `RequestIdFilter`
- [x] Intercepter toutes les requêtes pour générer/récupérer `X-Request-ID`
- [x] Injecter l'ID dans le contexte global `flask.g`
- [x] Ajouter l'ID dans le format JSON des logs
- [x] Retourner l'ID dans les headers de réponse HTTP

## 💻 Architecture du Tracing

### Flux de Tracing
1.  **Entrée** : Le client appelle l'API (avec ou sans header `X-Request-ID`).
2.  **Middleware** : Flask génère un UUID si le header est absent et le stocke.
3.  **Application** : Le code métier s'exécute.
4.  **Logging** : `RequestIdFilter` intercepte chaque écriture de log et y ajoute l'ID.
5.  **Sortie** : Le header `X-Request-ID` est ajouté à la réponse.

### Format des Logs
```json
{
  "asctime": "2026-01-14 21:58:01,123",
  "levelname": "INFO",
  "name": "root",
  "request_id": "a7d75228-cc99-488c-89f1-f1ef4b267c5b",
  "message": "Task created: xyz-123"
}
```

## 🧪 Tests Effectués
Le script `test_tracing.py` a validé :
1.  La présence du header `X-Request-ID` dans la réponse.
2.  La propagation correcte d'un ID envoyé par le client (contexte distribué).

## 📌 Prochaines Étapes

**Issue #8** : Documentation de l'API (OpenAPI/Swagger).
Pour le rendre utilisable par d'autres, documentons l'API. (Note: Le plan initial parle de Docker ensuite, nous pouvons aussi passer direct à Docker).

---

**Status** : ✅ COMPLÉTÉ
**Date** : 2026-01-14
