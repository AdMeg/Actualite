README DANS LE RAPPORT


Actualite

Ce sous-projet vise à mettre en place un système de fil d'actualité pour le projet plus large de portail du personnel.
Il s'agit d'un système de communication unidirectionnel. Une annonce/actualité est transmise à un ou plusieurs groupe
d'utilisateurs. De cette manière les utilisateurs cibles de cette annonce la verront dès leur connexion.

Pour ce faire, nous utiliserons un serveur Debian 12 qui comprendra un serveur de base de données avec différentes
tables et un docker contenant le code. Le code lui-même aura plusieurs endpoints qui pourront être requêté à la manière
d'une API.




Explications des routes

GET /get_messages

GET /
GET /get_groupes

POST /create_groupe


GET /get_groupe_actu

POST /create_groupe_actu

POST /get_actu_groupe

GET /get_thematique

POST /create_thematique
