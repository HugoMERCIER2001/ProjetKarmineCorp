import requests
import psycopg2
import json
import time
from API_Riots import *

def create_table(cursor):
    cursor.execute("CREATE TABLE Liaison (matchId VARCHAR(50), summonerId VARCHAR(50), PRIMARY KEY (matchId,summonerId));")


def rempli_table_liaison(list_matchId,list_summonerId,cursor):
    """
    Rempli la table Liaison avec les matchs de la liste list_matchId et les summonerId de la liste list_summonerId
    """
    parametre = ""
    for i in range(len(list_matchId)):
        if i != 0:
            parametre += ","
        parametre += f"'{list_matchId[i]}', '{list_summonerId[i]}'"
    cursor.execute("INSERT INTO Liaison (matchId,summonerId) VALUES ({parametre});")

