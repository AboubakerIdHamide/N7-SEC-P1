# Captures Postman - derniere etape

1. Demarrer le backend puis ouvrir Postman.
2. Import > Files > selectionner `tests/IncidentDesk.postman_collection.json`.
3. Executer la collection complete dans l'ordre avec Collection Runner (une iteration).
4. Pour chaque requete numerotee 01-09, afficher la reponse et prendre une capture avec methode, URL, statut et JSON. Si le Runner ne conserve pas les reponses, activer leur sauvegarde avant execution ou envoyer chaque requete manuellement dans l'ordre.
5. Enregistrer les neuf images dans `docs/screenshots/postman/`.

| Capture | Statut attendu |
|---|---|
| 01-no-jwt.png | 401 |
| 02-invalid-jwt.png | 401 |
| 03-expired-jwt.png | 401 |
| 04-employee-admin.png | 403 |
| 05-other-owner.png | 403 |
| 06-unassigned-technician.png | 403 |
| 07-disabled-login.png | 401 |
| 08-duplicate-email.png | 409 |
| 09-invalid-data.png | 400 |

Pour le test 07, executer la requete Setup - Disable employee 2 juste avant, puis Cleanup - Reenable employee 2 apres. Les JWT normaux expirent apres cinq minutes : relancer les quatre logins si necessaire. Ne pas remplacer le JWT du test 03 par un token simplement malforme : il doit etre correctement signe et expire.

Les 40 controles HTTP ont ete executes par le script Python. La collection Postman est preparee ; son execution dans l'interface et ses captures restent a effectuer par l'utilisateur, car le controle natif de Postman n'est pas disponible dans cette session.
