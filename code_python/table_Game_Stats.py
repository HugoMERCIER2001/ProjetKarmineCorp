import requests
import psycopg2
import json
import time
import glob
import os
from API_Riots import *

def crée_table_game_stats_vide(cursor):
    """Fonction qui crée la table Game_Stats vide, avec les colonnes selon si elles ont dans la table Key, pour la colonne table_stockage la valeur 'Game_Stats'."""
    cursor.execute("SELECT Nom_clé, Chemin_clé, Type_valeur FROM Key WHERE Table_stockage = 'Game_Stats';")
    rows = cursor.fetchall()
    param_creation = ""
    param_extraction = ""
    i = 0
    L_Nom_clé, Chemin_clé, Type_valeur = [], [], []
    for row in rows:
        L_Nom_clé.append(row[0])
        Chemin_clé.append(row[1])
        Type_valeur.append(row[2])
        param_creation += f"{row[0]} {row[2]}, "
        if i != 0 :
                param_extraction += f", "
        param_extraction += f"'{row[0]}'"
        i += 1
    cursor.execute(f"CREATE TABLE Game_Stats (MatchId TEXT, {param_creation}PRIMARY KEY (MatchId));")
    cursor.execute(f"UPDATE Key SET Extraite = '1' WHERE Nom_clé IN ({param_extraction});")


def suppression_table_game_stats(cursor):
     """Fonction qui supprime la table Game_Stats et pense à changer la valeur de Extraite dans la table clé, pour les clés correspondantes."""
     cursor.execute(f"DROP TABLE Game_Stats;")
     cursor.execute(f"UPDATE Key SET Extraite = '0' WHERE Table_stockage = 'Game_Stats' AND Extraite = '1';")


def rempli_table_game_stats_depuis_database(cursor):
    cursor.execute("SELECT Nom_clé, Chemin_clé, Type_valeur FROM Key WHERE Table_stockage = 'Game_Stats' AND Extraite = '1';")#on va chercher les chemins de clés, pour les clés correspondants aux colonnes de la table Game_Stats.
    rows = cursor.fetchall()
    L_Nom_clé, Chemin_clé, Type_valeur = [], [], ['TEXT']
    for row in rows:
        L_Nom_clé.append(row[0])#On se fait une liste avec le nom des colonnes de la table Game_Stats (pas très utile si ce n'est pour des test).
        Chemin_clé.append(row[1])#On se fait une liste de chemins de clés permettant d'aller chercher plus tard la valeur que l'on souhaite inserer dans la table Game_Stats
        Type_valeur.append(row[2])
    print(Type_valeur)
    cursor.execute("SELECT MatchId FROM Match WHERE Extrait_Game_Stats = 1")
    rows = cursor.fetchall()
    if len(rows) == 0:
        return("Pas de nouveau Match_JSON à extraire.")
    L_insert = []#On prepare le parametre du executemany que l'on va réaliser apres pour récuperer les valeurs que l'on va inserer dans la table Game_Stats
    param_Match_id = f"("
    param_select = f""
    for j, chemin in enumerate(Chemin_clé):
        param = f"file"
        L = chemin.split("-")
        for clé in L:
            print("type =", type(clé))
            if clé in ['0', '1', '2', '3', '4', '5', '6', '7','8', '9']:
                param += f"->{clé}"
            else:
                param += f"->'{clé}'"
        if j != 0:
            param_select += ", "
        param_select += param
    for i in range(len(rows)):
        if i != 0:
             param_Match_id += ', '
        param_Match_id += f"'{rows[i][0]}'"
    cursor.execute(f"SELECT MatchId, {param_select} FROM Match WHERE MatchId IN {param_Match_id});")
    Nom_colonnes = f""
    param_insert = f"("
    i = 0
    k = 0
    donnees = cursor.fetchall()
    for clé in L_Nom_clé :
        if k != 0:
            Nom_colonnes += ", "
        Nom_colonnes += f"{clé}"
        k += 1
    for donne in donnees:
        if i != 0 :
            param_insert += "), ("
        param = f""
        j = 0
        for l in range(len(donne)):
            if j != 0 :
                param += ", "
            if Type_valeur[l] == 'TEXT':
                param += f"'{donne[l]}'"
            else :
                param += f"{donne[j]}"
            j += 1
        param_insert += param
        i += 1
    print(i)
    print("Nom_colonnes = ", Nom_colonnes)
    print("param_insert = ", param_insert)
    cursor.execute(f"UPDATE Match SET Extrait_Game_Stats = 1 WHERE MatchId IN {param_Match_id});")
    cursor.execute(f"INSERT INTO Game_Stats (MatchId, {Nom_colonnes}) VALUES {param_insert});")



"""cursor.executemany("SELECT FROM", param)"""

""""""
"SELECT file->'info'->'gameCreation', file->'info'->'gameDuration', file->'info'->'queueId', file->'info'->'gameEndTimestamp', file->'info'->'gameStartTimestamp', file->'info'->'gameType', file->'info'->'gameVersion', file->'info'->'mapId', file->'info'->'participants'->'0'->'challenges'->'earliestBaron', file->'info'->'participants'->'0'->'challenges'->'firstTurretKilledTime', file->'info'->'participants'->'0'->'gameEndedInEarlySurrender', file->'info'->'participants'->'0'->'gameEndedInSurrender', file->'info'->'platformId', file->'info'->'tournamentCode' FROM Match WHERE MatchId = '',[('EUW_34444', ), ()]"