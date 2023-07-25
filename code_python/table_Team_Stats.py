import requests
import psycopg2
import json
import time
import glob
import os
from API_Riots import *

#################################Création de la table Team_Stats####################################################

def crée_table_team_stats_vide(cursor):
    """Fonction qui crée la table Team_Stats vide, avec les colonnes selon si elles ont dans la table Key, pour la colonne table_stockage la valeur 'Team_Stats'."""
    cursor.execute("SELECT Nom_clé, Chemin_clé, Type_valeur FROM Key WHERE Table_stockage = 'Team_Stats';")
    rows = cursor.fetchall()
    param_création = ""
    param_extraction = ""
    i = 0
    for row in rows:
        param_création += f"{row[0]} {row[2]}, "
        if i != 0:
            param_extraction += f", "
        param_extraction += f"'{row[0]}'"
        i += 1
    print(param_extraction)
    cursor.execute(f"CREATE TABLE Team_Stats (MatchId TEXT, Side TEXT, Participant TEXT[], {param_création}PRIMARY KEY (MatchId, Side));")
    cursor.execute(f"UPDATE Key SET Extraite = '1' WHERE Nom_clé IN ({param_extraction});")
