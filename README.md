# ProjetKarmineCorp
Test à faire pour pouvoir être pris en stage à la Karmine.

## Objectif:
Récupérez automatiquement les soloQ des joueurs challengers et les stockez dans une base de donnée

## Comment faire ça ?

  #### Générer une clé API Riot :

### Partie Python :
  #### Grâce à l’API Riot:

        Récupérez la liste des challengers
        Pour chaque challenger player, récupérez son historique de matchids de matchs joués (depuis le début de la saison) – à faire en parallèle de la création de base de données.
        Créer une fonction qui récupère/télécharge les 2 éléments de données pour un matchid (timeline, game)
        Stockez ces 2 éléments de données dans la base de données indexées par le matchid
   #### Setup une base PostgreSQL:
   
        1. Soit une base de donnée managée type DigitalOcean (recommandée), soit sur sa propre machine
        2. Créer les tables asssociées:
            1. Joueur challenger (quels colonnes mettre?)
            2. Matchid avec les challengers/joueurs dans la partie par id (quel id utilisé ?
            3. Json associé à la timeline
            4. Json associé à la game


## Ce que je dois faire dans l'ordre :
0 – Lire le developper portal.
1 – generer une clé API riot
2 – Lire la documentation des api riots.
3 - Envoi de requêtes : Les développeurs envoient des requêtes HTTP aux points de terminaison de l'API Riot en utilisant des méthodes telles que GET, POST, PUT, DELETE, etc. Les requêtes contiennent des informations spécifiques pour demander les données souhaitées.
4 - Réception des réponses : L'API répond aux requêtes avec des données structurées dans un format tel que JSON. Les développeurs peuvent extraire ces données et les utiliser dans leurs propres applications ou services.
5 - Gestion des limites et des autorisations : L'API Riot impose certaines limites d'utilisation, telles que des quotas de requêtes par minute ou par jour, afin de prévenir les abus et de garantir une utilisation équitable de l'API. Les développeurs doivent gérer ces limites et s'assurer de respecter les politiques d'utilisation de Riot Games.

### Lecture de la doc de l'api riot :
Lecture de la page explicative des API Riots :



Différentes clés API possibles :

La clé « API Developpement Key » :

	Clé pour des prototypes de projet perso, limité en quantité de requests/s et doit être regénérée toutes les 24h.

	Limites API lors de l’inscription :
20 requests every 1 seconds(s)
100 requests every 2 minutes(s)

	Ma clé API :
RGAPI-e36f5233-1d2a-4bf2-b91e-9cfe410de395


La clé «PERSONAL API KEYS » :

	Clé pour des projets perso, limité en quantité de requests/s et plus besoin d’être regénérée toutes les 24h. Mais doit enregistrer son produit dans riot pour la recevoir.

	Limites API lors de l’inscription :

20 requests every 1 second 
100 requests every 2 minutes 
	Ma clé API :
Doit proposer le produit à Riot.

La clé «PRODUCTION API KEYS » :


Clé pour des produits déstinés à des utilisations publiques. Limité en terme de Requests/s et plus besoin d’être regénérées toutes les 24h, mais doit enregistrer son produit dans Riot pour la recevoir.
La durée nécéssaire pour obtenir cette clé après avoir enregistré le produit est variante.


	Limites API lors de l’inscription :
500 requests every 10 seconds.
30,000 requests every 10 minutes.

	Ma clé API :
Doit proposer le produit à Riot.
