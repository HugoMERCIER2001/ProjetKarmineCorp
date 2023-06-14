import requests
import psycopg2
import json
import time
from API_Riots import *
from table_Joueurs import *
from table_Game import *
from table_Timeline import *
from table_Liaison import *
from Keys import *
from API_OpenAI import *


print("DEBUT DE PROGRAMME")

CLE_API = 'RGAPI-227531d5-6ccc-4584-8288-4264b0dac394'

clée_API_openai = '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'

openai.api_key = clée_API_openai

conn = psycopg2.connect( #Instaure une connexion vers la database DigitalOcean.
host="lol-database-do-user-14101148-0.b.db.ondigitalocean.com",
port="25060",
database="defaultdb",
user="doadmin",
password="AVNS_K2PNPsHumOCRMHRYaSP"
)

print("CONNEXION A LA DATABASE REUSSI")

CURSEUR = conn.cursor()#définit le curseur(besoin du curseur pour executer des commandes en PostgreSQL)

def joueurs(cursor, api_key):
    """
    liste de toutes les fonctions utilisables liées à la table joueur
    """
    #cursor.execute("CREATE TABLE Joueurs (summonerId TEXT,summonerName TEXT, leaguePoints INT, rank TEXT,wins INT, losses INT, puuid TEXT, PRIMARY KEY (summonerId));")
    #cursor.execute("DROP TABLE Joueurs")
    #associe_PUUID_aux_challengers(cursor,api_key)
    #rempli_table_challenger(cursor)
    actualisation_table_Joueurs(cursor, api_key)
    conn.commit()
    cursor.close()        
    conn.close()

def liaison(cursor, api_key):
    #cree_table_liaison_complete(cursor, api_key)
    #cursor.execute("DROP TABLE Liaison")
    #actualisation_table_liaison(cursor, api_key)
    #conn.commit()
    #cursor.close()        
    #conn.close()
    print('FIN')


def Game(cursor, api_key):
    #create_table_Game_complete(cursor, api_key)
    #actualisation_table_Game(cursor, api_key, False)
    #create_table_Timeline_complete(cursor, api_key)
    #actualisation_table_Timeline(cursor, api_key)
    cursor.execute("SELECT * FROM Joueurs")
    #cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Joueurs';")
    rows = cursor.fetchall()
    print("rows = ", rows)
    #for row in rows:
        #print(row)
        #print("ok")
    conn.commit()
    cursor.close()        
    conn.close()
    print('FIN')



def Keys():
    ecrit_clés()
    #demande_def_clé_match_chatGPT('matchId')



#joueurs(CURSEUR, CLE_API)
#liaison(CURSEUR, CLE_API)
Game(CURSEUR, CLE_API)
#Keys()





L = ['ZyY8BiyCwr8NmveDFyZzSo4gwmoZCBicJpIWqqBpPgp67oc','zTr6iTedMEK5kLJ_jqJc8XPKnkM7L5L_q4ni6wZeRNRAX4M','_ZQUVCGxbOQ75y62QmxblXylc2eseFZaiDllNt78imZ_rqqg']
