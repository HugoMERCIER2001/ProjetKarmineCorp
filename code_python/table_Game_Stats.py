import requests
import psycopg2
import json
import time
import glob
import os
from API_Riots import *

def crée_table_game_stats_vide(cursor):
    cursor.execute("SELECT Nom_clé, Chemin_clé, Type_valeur FROM Key WHERE Table_stockage = 'Game_Stats';")
    rows = cursor.fetchall()
    param_creation = ""
    L_Nom_clé, Chemin_clé, Type_valeur = [], [], []
    for row in rows:
        print(row)
        L_Nom_clé.append(row[0])
        Chemin_clé.append(row[1])
        Type_valeur.append(row[2])
        param_creation += f"{row[0]} {row[2]}, "
    cursor.execute(f"CREATE TABLE Game_Stats (MatchId TEXT, {param_creation}PRIMARY KEY (MatchId))")

def rempli_table_game_stats(cursor):
    cursor.execute("SELECT Nom_clé, Chemin_clé, Type_valeur FROM Key WHERE Table_stockage = 'Game_Stats';")
    rows = cursor.fetchall()
    param_creation = ""
    L_Nom_clé, Chemin_clé, Type_valeur = [], [], []
    for row in rows:
        L_Nom_clé.append(row[0])
        Chemin_clé.append(row[1])
        Type_valeur.append(row[2])
    print("L_Nom_clé = ", L_Nom_clé)
    print("Chemin_clé = ", Chemin_clé)
