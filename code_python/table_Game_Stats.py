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


def rempli_table_game_stats(cursor):
    cursor.execute("SELECT Nom_clé, Chemin_clé FROM Key WHERE Table_stockage = 'Game_Stats' AND Extraite = '1';")#on va chercher les chemins de clés, pour les clés correspondants aux colonnes de la table Game_Stats.
    rows = cursor.fetchall()
    param_creation = ""
    L_Nom_clé, Chemin_clé, L_Match_id_deja_dans_table = [], [], []
    for row in rows:
        L_Nom_clé.append(row[0])#On se fait une liste avec le nom des colonnes de la table Game_Stats (pas très utile si ce n'est pour des test).
        Chemin_clé.append(row[1])#On se fait une liste de chemins de clés permettant d'aller chercher plus tard la valeur que l'on souhaite inserer dans la table Game_Stats
    cursor.execute("SELECT MatchId FROM Game_Stats")#On va chercher les MatchId déjà dans la table pour pas repasser dessus.
    rows = cursor.fetchall()
    for row in rows:
         L_Match_id_deja_dans_table.append(row[0])#On se fait une liste des Matchs que l'on a déjà traité.
    cursor.execute("SELECT MatchId FROM Match")
    rows = cursor.fetchall()
    print("len(rows) = ", len(rows), "rows = ", rows)
    i = 0
    parametre_execute_many = []#On prepare le parametre du executemany que l'on va réaliser apres pour récuperer les valeurs que l'on va inserer dans la table Game_Stats
    while rows[i][0] not in L_Match_id_deja_dans_table and i < (len(rows) - 1):
        param_select = f""
        for j, element in enumerate(Chemin_clé):
            print("j =", j, "i = ", i)
            L_cle_dans_chemin_cle = element.split("-")
            param_select_2 = f""
            param_select_3 = f""
            if j != 0:
                 param_select += ", "
            for cle in L_cle_dans_chemin_cle :
                param_select_2 += f"->'{cle}'"
            print("row[i][0] =", rows[i][0])
            print("L_Nom_clé[j] =", L_Nom_clé[j])
            param_select_3 += f"{rows[i][0]}_{L_Nom_clé[j]}"
            param_select += f"file{param_select_2} AS {param_select_3}"      
        param_where = f"{rows[i][0]}"
        print("param_select =", param_select)
        parametre_execute_many.append((param_select, param_where))
        i += 1
    print(tuple(parametre_execute_many))
    cursor.executemany("SELECT %s FROM Match WHERE MatchId = %s", tuple(parametre_execute_many))
    rows = cursor.fetchall()
    for row in rows: 
        print(row)
        """la fonction se lance mais il dit que il n'a pas de données en sortie, il faut donc essayer la commande execute sans le many déja et voir ce que ca peut donner."""


""""        L_match_a_prendre.append(rows[i][0])
    param_select = f""
    i = 0
    for element in L_match_a_prendre:
        if i != 0:
            param_select += ", "
        param_select += f"{element}"
        i += 1
    cursor.execute(f"SELECT (file, MatchId) FROM Match WHERE MatchId IN ({param_select});")
    rows = cursor.fetchall()
    for row in rows:"""