import requests
import psycopg2
import json
import time
from API_Riots import *

def create_tables(cursor):
    cursor.execute("CREATE TABLE matches (matchId VARCHAR(50) PRIMARY KEY(match_id) , file JSON);")


def rempli_table_match(cursor,list_matchId):
    parametre = ""
    for match_id in list_matchId:
        if match_id != list_matchId[0]:
            parametre+= ","
        parametre += f"'{match_id}', '{match_id}'.json"
    cursor.execute(f"INSERT INTO matches (matchId,file) VALUES ({parametre});")



