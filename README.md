# Incident Desk - Spring Security, JWT et React

Application de declaration et de suivi des incidents informatiques. Projet local realise a partir des concepts de l'atelier TP2.

## Demarrage rapide

Prerequis : Java 17+ (teste avec Java 21), Maven 3.8+, Node.js 18+ (teste avec Node 24), npm.
Depuis le dossier PROJECT, ouvrir deux terminaux :

```bash
bash start-backend.sh
```

```bash
bash start-frontend.sh
```

- React : http://127.0.0.1:5173
- API Spring Boot : http://127.0.0.1:8080
- H2 : http://127.0.0.1:8080/h2-console ; JDBC `jdbc:h2:file:./data/incidents`, utilisateur `sa`, mot de passe vide.
- H2 conserve les donnees dans `backend/data/`. Toujours lancer le backend depuis `backend/` ou avec le script.
- Autres commandes : `cd backend && mvn test` ; `cd frontend && npm run build`.
- Ne pas lancer une deuxieme instance sur le meme port. Ctrl+C dans chaque terminal arrete le serveur.

## Comptes de demonstration

Tous utilisent le mot de passe `Demo1234!`.

| Email | Role |
|---|---|
| employee1@demo.test | EMPLOYEE |
| employee2@demo.test | EMPLOYEE |
| tech@demo.test | TECHNICIAN |
| admin@demo.test | ADMIN |

Les comptes sont initialises automatiquement si absents. L'inscription publique attribue uniquement EMPLOYEE, meme si un champ role est envoye. Les comptes ADMIN/TECHNICIAN sont initialises par `DemoData`, pas par le formulaire public.

## Fonctionnalites realisees

- Inscription, connexion, BCrypt, JWT signe avec `sub` (email), `iat`, `exp`, `role`.
- Duree JWT : 5 minutes. React conserve la session dans sessionStorage ; Axios ajoute le Bearer token. Une reponse API 401 efface la session et redirige vers Login avec un message.
- Backend stateless, CORS limite aux origines React locales, protection par role et par proprietaire/affectation.
- EMPLOYEE : creation et consultation de ses incidents uniquement.
- TECHNICIAN : incidents affectes, modification de statut et notes de traitement.
- ADMIN : tous les incidents, affectation, utilisateurs actifs/inactifs et statistiques.
- Historique horodate : creation, affectation, changements de statut, ajout de note.
- Un incident CLOSED ne peut plus etre modifie ni reaffecte.
- Profils : nom/email, changement de mot de passe avec verification de l'ancien et confirmation.
- Validation des DTO, erreurs JSON 400/401/403/404/409, trois dashboards, filtres de liste.
- ProtectedRoute et RoleRoute React ; controle reel toujours dans le backend.
- Refresh token : extension facultative non implementee.

## Principaux endpoints

| Methode | Chemin | Acces |
|---|---|---|
| POST | /auth/register, /auth/login | Public |
| GET, PUT | /api/profile | Authentifie |
| PUT | /api/profile/password | Authentifie |
| POST | /api/incidents | EMPLOYEE |
| GET | /api/incidents/my | EMPLOYEE |
| GET | /api/incidents/assigned | TECHNICIAN |
| GET | /api/incidents | ADMIN |
| GET | /api/incidents/{id} | Proprietaire, technicien affecte ou ADMIN |
| PUT | /api/incidents/{id}/status | Technicien affecte ou ADMIN |
| PUT | /api/incidents/{id}/assign/{technicianId} | ADMIN |
| POST | /api/incidents/{id}/comments | Technicien affecte |
| GET | /api/admin/users | ADMIN |
| PUT | /api/admin/users/{id}/enable ou /disable | ADMIN |
| GET | /api/admin/statistics | ADMIN |

Exemple de creation :

```json
{"title":"Phishing suspect","description":"Un email demande mon mot de passe.","category":"PHISHING","priority":"HIGH"}
```

Categories : NETWORK, MALWARE, PHISHING, ACCESS, SOFTWARE, HARDWARE, DATA_LEAK, OTHER.
Priorites : LOW, MEDIUM, HIGH, CRITICAL. Etats : OPEN, ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED.
L'affectation d'un incident OPEN passe son etat a ASSIGNED. Le technicien peut ensuite passer a IN_PROGRESS, puis RESOLVED.

## Verification et preuves

```bash
python3 tests/verify.py
```

Ce script execute 40 controles HTTP, cree des donnees de demonstration et conserve les resultats dans `docs/test-results.json`. Il couvre les neuf tests de securite imposes et le scenario employe/admin/technicien. Il n'efface pas les donnees ; plusieurs executions ajoutent des incidents.

Importer `tests/IncidentDesk.postman_collection.json` dans Postman, puis executer la collection dans l'ordre. Les tokens et identifiants sont renseignes automatiquement. Les neuf requetes numerotees 01-09 correspondent aux tests obligatoires. La collection inclut un JWT de demonstration signe mais expire, utilisable uniquement avec la cle de demonstration par defaut.

**Captures Postman a finaliser manuellement :** ouvrir chaque requete 01-09 apres execution et capturer URL, methode, statut et corps JSON. Enregistrer dans `docs/screenshots/postman/`. Les resultats du script Python ne sont pas des captures Postman. Voir `docs/POSTMAN-CAPTURES.md`.

Les captures reelles de l'interface sont dans `docs/screenshots/`. Les diagrammes SVG et leur source Mermaid sont dans `docs/`. Le rapport PDF est dans `output/pdf/rapport-incident-desk.pdf`.

## Comprendre le code en cinq minutes

1. `JwtService.java` : emission et validation cryptographique du JWT.
2. `JwtFilter.java` : extraction du token, lecture du compte et remplissage du SecurityContext.
3. `SecurityConfig.java` et `IncidentController.java` : routes publiques et autorisations par role.
4. `IncidentService.java` : comparaison entre utilisateur courant et proprietaire/technicien ; historique et regles metier.
5. `frontend/src/services/api.js` : interceptors Axios ; `ProtectedRoute.jsx` et `RoleRoute.jsx` : navigation.

## Choix et limites

- Application de demonstration locale : comptes/cle connus et console H2 publique selon l'enonce. Ces reglages doivent changer avant tout deploiement reel.
- Le JWT est signe, pas chiffre. Il ne contient pas le mot de passe.
- Le role et l'etat enabled sont relus en base a chaque requete ; la desactivation bloque aussi un JWT deja emis.
- Modifier l'email renvoie un nouveau JWT ; les anciens tokens utilisant l'ancien email ne trouvent plus le compte.
- Changer le mot de passe ne revoque pas les autres JWT existants ; ils expirent au plus tard apres cinq minutes. La deconnexion efface la session du navigateur.
- Le formulaire n'impose pas une matrice complete de transitions : seules les autorisations et l'immutabilite de CLOSED sont imposees, conformement aux regles explicites du sujet.
- Les relations LAZY sont lues dans une transaction puis converties en DTO : pas de mot de passe expose et pas de recursion JSON.
- Le rapport distingue les verifications executees des captures Postman restant a prendre.
