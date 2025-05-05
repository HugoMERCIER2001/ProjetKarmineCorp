import requests
import psycopg2
import json
import time
from Table_Keys import *
from API_Riots import *
from table_Joueurs import *
from table_Match import *
from table_Game_Stats import *
from table_Timeline import *
from table_Liaison import *
from Keys import *
from API_OpenAI import *
from table_Team_Stats import *


print("DEBUT DE PROGRAMME")

CLE_API = ''

clée_API_openai = ''

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
    cursor.execute("CREATE TABLE Joueurs (summonerId TEXT,summonerName TEXT, leaguePoints INT, rank TEXT,wins INT, losses INT, puuid TEXT, PRIMARY KEY (summonerId));")
    rempli_table_challenger(cursor)
    associe_PUUID_aux_challengers(cursor,api_key)
    #cursor.execute("DROP TABLE Joueurs")
    #actualisation_table_Joueurs(cursor, api_key)
    conn.commit()
    #cursor.close()        
    #conn.close()

def liaison(cursor, api_key):
    #cree_table_liaison_complete(cursor, api_key)
    #cursor.execute("DROP TABLE Liaison")
    actualisation_table_liaison(cursor, api_key)
    conn.commit()
    #cursor.close()        
    #conn.close()
    print('FIN')


def Game(cursor, api_key):
    #create_table_Game_complete(cursor, api_key)
    #actualisation_table_Game(cursor, api_key, False)
    #create_table_Timeline_complete(cursor, api_key)
    #actualisation_table_Timeline(cursor, api_key)
    #suppression_table_game_stats(cursor)
    #cursor.execute("DROP TABLE Game_Stats")
    #cursor.execute("UPDATE Key SET table_stockage = 'Team_Stats' WHERE Nom_clé IN ('Durée_Avant_Premier_Baron', 'Durée_Avant_Chute_Première_Tour')")
    #cursor.execute("SELECT Nom_clé, Chemin_clé, Type_valeur FROM Key WHERE Table_stockage = 'Game_Stats' AND Extraite = '1';")
    #cursor.execute("UPDATE Key SET Type_valeur = 'BIGINT' WHERE Nom_clé IN ('Date_Création', 'Date_Fin',  'Date_Début');")
    cursor.execute("SELECT * FROM Game_Stats")
    #cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'key';")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.commit()
    cursor.close()        
    conn.close()
    print('FIN')



def Keys(cursor):
    #cree_table_cle_pleine(cursor)
    #crée_table_game_stats_vide(cursor)
    #rempli_table_game_stats(cursor)
    #rempli_table_game_stats_depuis_database(cursor)
    #cursor.execute("SELECT file->\'info\'->\'gameCreation\', file->\'info\'->\'gameDuration\' FROM Match WHERE MatchId = 'EUW1_6336853773'")
    conn.commit()
    cursor.close()
    conn.close()
    print('FIN')

def Team_Stats(cursor):
    crée_table_team_stats_vide(cursor)
    conn.commit()
    cursor.close()
    conn.close()
    print('FIN')



#joueurs(CURSEUR, CLE_API)
#liaison(CURSEUR, CLE_API)
#Game(CURSEUR, CLE_API)
#Keys(CURSEUR)
#Team_Stats(CURSEUR)
CURSEUR.execute("SELECT * FROM Joueurs")
raws = CURSEUR.fetchall()
for row in raws:
    print(row)

L = ['ZyY8BiyCwr8NmveDFyZzSo4gwmoZCBicJpIWqqBpPgp67oc','zTr6iTedMEK5kLJ_jqJc8XPKnkM7L5L_q4ni6wZeRNRAX4M','_ZQUVCGxbOQ75y62QmxblXylc2eseFZaiDllNt78imZ_rqqg']
