import requests
import psycopg2
import json
import time
from API_Riots import *
from table_Joueurs import *
from table_Game import *
from table_Timeline import *
from table_Liaison import *

CLE_API = 'RGAPI-1d6c027d-c2a6-4ec2-83f2-c297c0135b29'

conn = psycopg2.connect( #Instaure une connexion vers la database DigitalOcean.
host="lol-database-do-user-14101148-0.b.db.ondigitalocean.com",
port="25060",
database="defaultdb",
user="doadmin",
password="AVNS_K2PNPsHumOCRMHRYaSP"
)
CURSEUR = conn.cursor()#définit le curseur(besoin du curseur pour executer des commandes en PostgreSQL)

def main(cursor, api_key):
    #envoie_demande_liste_challengers(api_key)
    #envoie_demande_liste_match_challengers(api_keys)
    #cursor.execute("CREATE TABLE Joueurs (summonerId TEXT,summonerName TEXT, leaguePoints INT, rank TEXT,wins INT, losses INT, puuid TEXT, PRIMARY KEY (summonerId));")
    #cursor.execute("DROP TABLE Joueurs")
    associe_PUUID_aux_challengers(cursor,api_key)
    #rempli_table_challenger()
    conn.commit()
    cursor.execute("SELECT summonerId FROM Joueurs")
    rows = cursor.fetchall()
    #for row in rows:
    print(rows)

main(CURSEUR, CLE_API)