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
            2. Matchid avec les challengers/joueurs dans la partie par id (quel id utilisé ?)
            3. Json associé à la timeline
            4. Json associé à la game


## Ce que je dois faire dans l'ordre :
0. Lire le developper portal.
1. generer une clé API riot
2. Lire la documentation des api riots.
3. Envoi de requêtes : Les développeurs envoient des requêtes HTTP aux points de terminaison de l'API Riot en utilisant des méthodes telles que GET, POST, PUT, DELETE, etc. Les requêtes contiennent des informations spécifiques pour demander les données souhaitées.
4. Réception des réponses : L'API répond aux requêtes avec des données structurées dans un format tel que JSON. Les développeurs peuvent extraire ces données et les utiliser dans leurs propres applications ou services.
5. Gestion des limites et des autorisations : L'API Riot impose certaines limites d'utilisation, telles que des quotas de requêtes par minute ou par jour, afin de prévenir les abus et de garantir une utilisation équitable de l'API. Les développeurs doivent gérer ces limites et s'assurer de respecter les politiques d'utilisation de Riot Games.
6. Comprendre le module Panda permet de mieux visualiser et de faire des calculs sur les données/Poetrie/Puis la nan

### Lecture de la doc de l'api riot :
Lecture de la page explicative des API Riots :



#### Différentes clés API possibles :

#### La clé « API Developpement Key » :

Clé pour des prototypes de projet perso, limité en quantité de requests/s et doit être regénérée toutes les 24h.

##### Limite clé API lors de l'inscription :
20 requests every 1 seconds(s)
100 requests every 2 minutes(s)

##### Ma clé API :
RGAPI-e36f5233-1d2a-4bf2-b91e-9cfe410de395


#### La clé «PERSONAL API KEYS » :

Clé pour des projets perso, limité en quantité de requests/s et plus besoin d’être regénérée toutes les 24h. Mais doit enregistrer son produit dans riot pour la recevoir.

##### Limites API lors de l’inscription :

20 requests every 1 second 
100 requests every 2 minutes 

##### Ma clé API :
Doit proposer le produit à Riot.

#### La  clé «PRODUCTION API KEYS » :

Clé pour des produits déstinés à des utilisations publiques. Limité en terme de Requests/s et plus besoin d’être regénérées toutes les 24h, mais doit enregistrer son produit dans Riot pour la recevoir.
La durée nécéssaire pour obtenir cette clé après avoir enregistré le produit est variante.
La Limite Api lors de l'inscription est variable selon la région dans le monde et peut après ça demander unne clé tournois ou pro.

##### Limites API lors de l’inscription :
500 requests every 10 seconds.
30,000 requests every 10 minutes.

##### Ma clé API :
Doit proposer le produit à Riot.


## Commandes PostgreSQL :

### CREATE DATABASE :
Cette commande permet de créer une nouvelle base de données.

### DROP DATABASE :
Cette commande permet de supprimer complètement une base de données. (les données sont perdus pour toujours).

### CREATE TABLE :
Cette commande permet de créer une nouvelle table dans une base de données. Elle spécifie les colonnes, les types de données et les contraintes pour chaque colonnes.

### ALTER TABLE :
Cette commande permet de modifier la structure d'une table existante. On pet ajouter, renommer ou supprimer des colonnes, définir des contraintes ...

### SELECT ... FROM ... WHERE ... :
Permet de récuperer des données à partir d'une table ou de plusieurs tables.

### INSERT INTO ... VALUES (...) :
Cette commande permet d'inserer de nouvelles lignes de données dans une table existante.

### UPDATE (nom_de_la_table) SET (colonne = nouvelle_valeur) WHERE condition :
Cette commande permet de mettre à jour les données existantes dans une table.

### DELETE FROM (nom de la table) WHERE condition :
Cette commande permet de de supprimer des lignes spécifiques d'une table.

### CREATE INDEX :
Cette commande permet de créer un index sur une ou plusieurs colonnes d'une table. Les indexs améliorent les performances des requêtes en accélérant la recherche de données.

### CREATE VIEW :
Cette commande permet de créer une vue, qui est une représentation virtuelle d'une ou plusieurs tables. Les vues permettent d'abstraire la complexité des requêtes et de simplifier l'accès aux données.

### CREATE FUNCTION :
Cette commande permet de créer une fonction stockée, qui est un bloc de code SQL réutilisable.Les fonctions peuvent accepter des paramètres, effectuer des opérations et renvoyer des résultats.

### CREATE TRIGGER :
Cette commande permet de créer un déclancheur, qui est un bloc de code SQL executé automatiquement en réponse à un évênement spécifique sur une table. Les déclencheurs sont utilisés pour effectuer des actions supplémentaires, telles que la mise à jour d'autres tables ou l'éxecution de fonctions.

### BEGIN, COMMIT, ROLLBACK: 
Ces commandes sont utilisées pour gérer les transactions dans PostgreSQL. Vous pouvez regrouper plusieurs commandes en une seule transaction et les valider (COMMIT) ou les annuler (ROLLBACK) en fonction du résultat.



# EXTRACTION DES DONNES DU JSON INFO UTILES:
Dans le JSON Game, il y a une liste stockée avec l'enchainement de clé : metadata-participants, cette liste de 10 éléments contient les puuids de chaque joueurs dans la game. Il faut exploiter cette liste pour toutes les données stockées dans les dictionnaires d'enchainement : info-participants-... car ce sont des données associées à 1 joueur en particulier dans la Game.

# Questions clés:
Quelle est la différence entre un kill et un takedown ? (partout)
baronBuffGoldAdvantageOverThreshold le palier est questin, c'est quel palier ? (ligne 225)
Quelle diff entre barontakedown et baron kills ? (ligne 235 et un peu avant)
Que veut dire cette clé : blastConeOppositeOpponentCount ? (ligne 243)
Que veut dire cette clé : completeSupportQuestInTime ? (ligne 270)
Que veut dire cette clé : dancedWithRiftHerald ? (ligne 315)
Que veut dire cette clé : earlyLaningPhaseGoldExpAdvantage ? (ligne 368)
Que veut dire cette clé : elderDragonKillsWithOpposingSoul ? (ligne 387)
Que veut dire cette clé : flawlessAces ? (ligne 468)
Que veut dire cette clé : getTakedownsInAllLanesEarlyJungleAsLaner ? (ligne 496)
Que veut dire cette clé : hadOpenNexus ? (ligne 513)
Que veut dire cette clé : killedChampTookFullTeamDamageSurvived ? (ligne 602)
Que veut dire cette clé : killsOnOtherLanesEarlyJungleAsLaner ? (ligne 621)
Que veut dire cette clé : killsOnRecentlyHealedByAramPack ? (ligne 629)
Que veut dire cette clé : takedownOnFirstTurret ? (ligne 980)
Que veut dire cette clé : takedownsInAlcove ? ( ligne 1025)
Que veut dire cette clé : threeWardsOneSweeperCount ? (ligne 1088)
Que veut dire cette clé : tookLargeDamageSurvived ? (ligne 1097)
Que veut dire cette clé : twentyMinionsIn3SecondsCount ? (ligne 1133)
Que veut dire cette clé : visionScoreAdvantageLaneOpponent ? (ligne 1151)
Que veut dire cette clé : eligibleForProgression ? (ligne 1340)
Que veut dire cette clé : riotIdName ? (ligne 1889)
Que veut dire cette clé : riotIdTagline ? (ligne 1898)
Que veut dire cette clé : sightWardsBoughtInGame ? (ligne 1916)
Que veut dire cette clé : unrealKills ? (ligne 2222)

Problème de compréhension de tout ce qui est perks (runes je crois) (ligne 1741 à 1822)
Quelle est la différence entre individual position, team position et lane ?


  
  ## Choses à ne pas oublier :
Les données renvoyer par les API Riots sont cryptés, donc pas les mêmes id etc si des clés différentes.

On ne peut pas dépasser une certaine limite de requetes API/s, pour cela on a fait une fonction qui attend pour ne pas dépassser ces quotas. Il y a à la fois un nombre de requetes/s liés à la clé API et une liée au type de requete que l'on fait. Il faut donc recréer une variable globale pour chaque NOUVEAUX TYPES DE REQUETE que l'on fait pour pouvoir calculer le temps à attendre avant de refaire une requete API, pour respecter les quotas liée AU TYPE DE REQUETE.

Il ne faut surtout pas changer le formatage du fichier clés_params.txt (sinon les fonctions qui introduisent les valeurs dans les tables correspondantes ne fonctionneront plus). Il est cependant possible de rajouter des lignes mais pas de changer le nom des lignes préexistantes, ou les éléments séparateurs de blocs-clés. (les "----..."). 

SummonerName,puuid, SummonerId et SummonerLvl sont dans le JSON game, et sont donc sauvegardé aussi dans Liaison_Stats, à voir ce que l'on fait (dédoublement de l'information qui est à la fois dans Joueurs et Liaison_Stats ou pas ?).

Il faut que lorsque on extrait les JSON, si une clé dans le chemin clé est un entier comme un indice d'élement d'une liste, il faut que dans l'enchainement : file->'participant'->0->donne, 0 ne soit pas entre guillements.

Les Timestamps stockée doivent être stockés en BIGINT et pas en INT.

1 - finir de sortir des JSON.
1bis - réorganiser les fichiers. (il faut que tout soit mis dans des dossier et en plus que on ait une fonction actualisation et une création que on a juste à lancer pour que tout soit actualisé ou créé.)
2 - Droplet.
2bis - Voir ce que on peut faire avec les retryafter
3 - Découvrir le module Panda et Poetry
4 - Test
5 - Faire Agrandissement.py
6 - Faire Transfert.py

  ### IDEES

  Si on fait une page pour TFT, il faudrait que en connectant son compte à la page TFT on puisse sauvegarder des compos automatiquement qui ont marchés, ou rappeler les dernières bonnes compos jous par le joueur.

  Si on fait un page TFT, il faudrait faire des entrainements à choix, comme pour les echecs on place le joueur dans certaines situations, et on note ses choix.