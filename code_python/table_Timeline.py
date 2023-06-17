import requests
import psycopg2
import json
import time
import glob
import os
from API_Riots import *



#########################Création de la Table Timeline#######################################################################################################

def create_tables_Timeline_vide(cursor):
    cursor.execute("CREATE TABLE Timeline (matchId VARCHAR(50), file JSONB, PRIMARY KEY (matchId));")


def create_table_Timeline_complete(cursor, api_key):
    create_tables_Timeline_vide(cursor)
    compteur_Timeline = 0
    parametre_fichier_JSON = []
    cursor.execute("SELECT MatchId FROM Liaison")
    rows = cursor.fetchall()
    for row in rows:
        compteur_Timeline += 1
        get_timeline_by_id(row[0], api_key)

        with open(f"../ProjetKarmineCorp/data/match/match_timeline/{row[0]}.json", 'r') as f:
            contenu_json = json.load(f)
            parametre_fichier_JSON.append((f"{row[0]}", json.dumps(contenu_json)))

        if compteur_Timeline == 10:
            break
    print(parametre_fichier_JSON)
    cursor.executemany(f"INSERT INTO Timeline (matchId, file) VALUES (%s, %s);", parametre_fichier_JSON)
    #suppression_fichier_timeline('data/match/match_timeline')

##################################Actualisation de la Table Timeline##############################################################################################################

def actualisation_table_Timeline(cursor, api_key):
    """
    Fonction qui actualise la Table Timeline de la base de donnée (Il faut actualiser la Table Liaison avant).
    (Quasiment même fonction que la fonction précédente avec juste une vérification que le matchId n'a pas été traité pécédemment.)
    """
    parametre_fichier_JSON, list_match_deja_vu = [], []
    compteur_actualisé = 0
    cursor.execute("SELECT MatchId FROM Timeline") #va chercher les matchId qui sont éja stockés dans la database, pour eviter de les straiter à nouveau.
    rows = cursor.fetchall()
    for row in rows :
        list_match_deja_vu.append(row[0])
    cursor.execute("SELECT MatchId FROM Liaison") #va chercher tous les match Id à traiter.
    rows = cursor.fetchall()
    for row in rows:
        if row[0] not in list_match_deja_vu: #vérifie si le matchId n'est pas déja traité dans la databse.
            get_timeline_by_id(row[0], api_key)
            with open(f"../ProjetKarmineCorp/data/match/match_timeline/{row[0]}.json", 'r') as f:
                contenu_json = json.load(f)
                parametre_fichier_JSON.append((f"{row[0]}", json.dumps(contenu_json)))
            compteur_actualisé += 1
        if compteur_actualisé == 150:
            break    
    if compteur_actualisé != 0:
        cursor.executemany(f"INSERT INTO Timeline (matchId, file) VALUES (%s, %s);", parametre_fichier_JSON)
    #suppression_fichier_timeline('data/match/match_timeline')

#############################Suppression Fichiers crées###############################################################################################################################################

def suppression_fichier_timeline(chemin_acces_dossier):
    t1 = time.time()
    liste_timeline_JSON = glob.glob(f"{chemin_acces_dossier}/*")
    for Timeline in liste_timeline_JSON:
        os.remove(Timeline)
    t2 = time.time()
    print(t2 - t1)