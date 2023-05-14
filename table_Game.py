import requests
import psycopg2
import json
import time
from API_Riots import *

def create_tables(cursor):
    cursor.execute("CREATE TABLE matches (matchId VARCHAR(50) PRIMARY KEY(match_id) , file JSON);")


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



