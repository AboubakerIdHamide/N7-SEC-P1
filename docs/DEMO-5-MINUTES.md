# Demonstration orale en cinq minutes

## 0:00 - 1:00 : employe
Connexion employee1@demo.test / Demo1234! ; creer un incident PHISHING / HIGH. Expliquer que la requete porte un Bearer JWT. Ouvrir My incidents : seuls les incidents du compte sont visibles.

## 1:00 - 2:00 : administrateur
Se deconnecter ; connexion admin@demo.test. Montrer les statistiques et les utilisateurs. Ouvrir l'incident et l'affecter a Technician A. L'etat devient ASSIGNED.

## 2:00 - 3:00 : technicien
Connexion tech@demo.test. Ouvrir Assigned incidents, passer l'incident a IN_PROGRESS, ajouter une note puis passer a RESOLVED.

## 3:00 - 4:00 : retour employe
Revenir avec employee1@demo.test ; montrer RESOLVED et l'historique horodate avec les acteurs. Montrer le profil et les champs de changement de mot de passe.

## 4:00 - 5:00 : preuve de securite
Dans Postman, montrer 401 sans JWT et 403 sur l'incident d'un autre employe. Expliquer : authentification = qui je suis ; role = quelle action je peux faire ; propriete = sur quelle donnee je peux agir.

## Questions du professeur

- Pourquoi BCrypt ? Le serveur conserve un hash sale et verifie le mot de passe avec matches ; il ne le dechiffre pas.
- Que contient le token ? sub=email, iat=creation, exp=expiration, role. La signature detecte toute modification.
- Pourquoi STATELESS ? Aucune session HTTP serveur n'est utilisee pour authentifier les requetes ; chacune porte son JWT.
- Pourquoi LAZY ? Ne charger les utilisateurs lies a l'incident que lorsque necessaire ; DTO construits dans une transaction.
- Pourquoi pas seulement RoleRoute ? Un client peut appeler l'API directement ; le backend verifie role ET proprietaire.
- 401 versus 403 ? Identite absente/invalide versus identite reconnue sans autorisation suffisante.
- Refresh token ? Facultatif et non implemente. Il servirait a obtenir un access token apres expiration ; une solution complete gere rotation et revocation.
