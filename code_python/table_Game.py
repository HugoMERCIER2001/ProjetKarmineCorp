import requests
import psycopg2
import json
import time
import glob
import os
from API_Riots import *



#########################Création de la Table Game#######################################################################################################

def create_tables_Game_vide(cursor):
    cursor.execute("CREATE TABLE Match (matchId VARCHAR(50), file JSONB, PRIMARY KEY (matchId));")


def create_table_Game_complete(cursor, api_key, suppression = False):
    """
    Fonction qui crée la table Match avec les données.
    Le paramètre suppression est un booléen qui vaut True si on souhaite supprimer les fichiers JSON des matchs. Par default à False.
    """
    create_tables_Game_vide(cursor)
    compteur_Game = 0
    parametre_fichier_JSON = []
    cursor.execute("SELECT MatchId FROM Liaison")
    rows = cursor.fetchall()
    for row in rows:
        compteur_Game += 1
        get_match_by_id(row[0], api_key)

        with open(f"../ProjetKarmineCorp/data/match/match_info/{row[0]}.json", 'r') as f:
            contenu_json = json.load(f)
            parametre_fichier_JSON.append((f"{row[0]}", json.dumps(contenu_json)))

        if compteur_Game == 10:
            break
    print(parametre_fichier_JSON)
    cursor.executemany(f"INSERT INTO Match (matchId, file) VALUES (%s, %s);", parametre_fichier_JSON)
    suppression_fichier_game('../ProjetKarmineCorp/data/match/match_info')

##################################Actualisation de la Table Game##############################################################################################################

def actualisation_table_Game(cursor, api_key, suppression = False):
    """
    Fonction qui actualise la Table Game de la base de donnée (Il faut actualiser la Table Liaison avant).
    Le paramètre suppression vaut True si on veut supprimer les fichiers JSON crées de l'ordinateur. De base en False.
    (Quasiment même fonction que la fonction précédente avec juste une vérification que le matchId n'a pas été traité pécédemment.)
    """
    parametre_fichier_JSON, list_match_deja_vu = [], []
    compteur_actualisé = 0
    cursor.execute("SELECT MatchId FROM Match") #va chercher les matchId qui sont éja stockés dans la database, pour eviter de les straiter à nouveau.
    rows = cursor.fetchall()
    for row in rows :
        list_match_deja_vu.append(row[0])
    cursor.execute("SELECT MatchId FROM Liaison") #va chercher tous les match Id à traiter.
    rows = cursor.fetchall()
    for row in rows:
        if row[0] not in list_match_deja_vu: #vérifie si le matchId n'est pas déja traité dans la databse.
            get_match_by_id(row[0], api_key)
            with open(f"../ProjetKarmineCorp/data/match/match_info/{row[0]}.json", 'r') as f:
                contenu_json = json.load(f)
                parametre_fichier_JSON.append((f"{row[0]}", json.dumps(contenu_json)))
            compteur_actualisé += 1
        if compteur_actualisé == 1:
            break
    if compteur_actualisé != 0:
        cursor.executemany(f"INSERT INTO Match (matchId, file) VALUES (%s, %s);", parametre_fichier_JSON)
    if suppression :
        suppression_fichier_game('../ProjetKarmineCorp/data/match/match_info')

##########################Suppresion Fichiers crées##################################################################################################################################################

def suppression_fichier_game(chemin_acces_dossier):
    liste_Game_JSON = glob.glob(f"{chemin_acces_dossier}/*")
    for Game in liste_Game_JSON:
        os.remove(Game)