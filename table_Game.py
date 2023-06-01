import requests
import psycopg2
import json
import time
import glob
from API_Riots import *



#########################Création de la Table Game#######################################################################################################

def create_tables_Game_vide(cursor):
    cursor.execute("CREATE TABLE Match (matchId VARCHAR(50) PRIMARY KEY(match_id) , file JSON);")


def rempli_table_match(cursor,list_matchId,list_file):
    """
    Rempli la table match avec les matchs de la liste list_matchId et les fichiers json de la liste list_file
    """
    parametre = ""
    for i in range(len(list_matchId)):
        if i != 0:
            parametre += ","
        parametre += f"'{list_matchId[i]}', '{list_file[i]}'"
    cursor.execute(f"INSERT INTO matches (matchId,file) VALUES ({parametre});")


def create_table_Game_complete(cursor, api_key):
    list_matchId, list_file = [], []
    cursor.execute("SELECT MatchId FROM Liaison")
    rows = cursor.fetchall()
    for row in rows:
        list_matchId.append(row[0])
        get_match_by_id(row[0], api_key)
        chemin_repertoire = f"data/match/match_info/{row[0]}.json"
        list_file.append(glob.glob(chemin_repertoire))
    rempli_table_match(cursor, list_matchId, list_file)

##################################Actualisation de la Table Game##############################################################################################################

def actualisation_table_Game(cursor, api_key):
    list_matchId, list_file, list_match_deja_vu = [], [], []
    cursor.execute("SELECT MatchId FROM Match")
    rows = cursor.fetchall()
    for row in rows :
        list_match_deja_vu.append(row[0])
    cursor.execute("SELECT MatchId FROM Liaison")
    rows = cursor.fetchall()
    for row in rows:
        print(row)