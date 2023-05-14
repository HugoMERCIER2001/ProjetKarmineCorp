import requests
import psycopg2
import json
import time
from API_Riots import *



######Création ######################################################################################################################################################################################################
def rempli_table_challenger(cursor):
    """Fonction qui remplie la table avec les joueurs challengers crée précedemment"""
    with open("data_challenger_id.json", "r") as f:#data_challenger_id.json représente le document type JSON qui contient les données obtenue par la requête pour obtenir la liste des joueuurs challengers.
        objet = json.load(f)
        """print(objet["name"], "\n")"""#liste des clés non utilisées.
        """print(objet["tier"], "\n")"""
        """print(objet["leagueId"],"\n")"""
        """print(objet["queue"], "\n")"""
        entries = objet["entries"]#entries est une liste d'éléments de type dictionnaire.
        t1 = time.time()
        parametre = f""
        for element in entries :
            if element != entries[0]:
                parametre+= ","
            parametre += f"('{element['summonerId']}', '{element['summonerName']}', {element['leaguePoints']}, '{element['rank']}', {element['wins']}, {element['losses']}, 'NULL')"
    commande = f"INSERT INTO Joueurs (summonerId, summonerName, leaguePoints, rank, wins, losses, puuid) VALUES {parametre};"
    cursor.execute(commande)
    t2 = time.time()
    print("temps =",t2 - t1)

########################Actualisation#########################################################################################################################################################
def associe_PUUID_aux_challengers(cursor, api_key):
    """fonction qui associe aux joueurs challengers leur puiid, peut se faire en actualisation"""
    cursor.execute("SELECT summonerId, puuid FROM Joueurs WHERE puuid = 'NULL';")
    summoner_ids = cursor.fetchall()
    parametre = ""
    compteur = 0
    for summoner_id in summoner_ids:
        compteur += 1
        envoie_demande_PUUID_summoner(summoner_id[0], api_key)
        print(compteur)
        with open("data_summoner_id.json", "r") as f:#data_summoner_id.json représente le document type JSON qui contient les données obtenue par la requête pour obtenir le PUUID d'un joueur.
            objet = json.load(f)
            parametre += f" WHEN joueurs.summonerid = '{objet['id']}' THEN '{objet['puuid']}'"
        if compteur == 90:
            print("on s'est arreté avant")
            break
    commande = f"UPDATE Joueurs SET puuid = CASE {parametre} END WHERE puuid = NULL;"   
    cursor.execute(commande)


    

def actualisation_table_Joueurs(cursor, api_key):
    """fonction qui actualise la table Joueurs"""
    envoie_demande_liste_challengers(api_key)
    cursor.execute("SELECT summonerId, puuid FROM Joueurs WHERE puuid = 'NULL';")
    rows = cursor.fetchall()
    compteur_insert_to = 0
    parametre_inser_to = f""
    Liste_summoner_ids = []
    for row in rows:
        Liste_summoner_ids.append(row[0])
    with open("data_challenger_id.json", "r") as f:#data_challenger_id.json représente le document type JSON qui contient les données obtenue par la requête pour obtenir la liste des joueuurs challengers.
        objet = json.load(f)
        entries = objet["entries"]
        for element in entries:
            if element['summonerId'] not in Liste_summoner_ids:
                if compteur_insert_to == 0:
                    parametre_inser_to += f"('{element['summonerId']}', '{element['summonerName']}', {element['leaguePoints']}, '{element['rank']}', {element['wins']}, {element['losses']}, 'NULL')"
                else :
                    parametre_inser_to += ", "