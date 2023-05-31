import requests
import psycopg2
import json
import time
from API_Riots import *



######Création ######################################################################################################################################################################################################
def rempli_table_challenger(cursor):
    """Fonction qui remplie la table avec les joueurs challengers crée précedemment"""
    with open("data/summoner/data_challenger_id.json", "r") as f:#data_challenger_id.json représente le document type JSON qui contient les données obtenue par la requête pour obtenir la liste des joueuurs challengers.
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
            parametre += f"('{element['summonerId']}', '{element['summonerName']}', {element['leaguePoints']}, '{element['rank']}', {element['wins']}, {element['losses']}, '0')"      
    commande = f"INSERT INTO Joueurs (summonerId, summonerName, leaguePoints, rank, wins, losses, puuid) VALUES {parametre};"
    cursor.execute(commande)
    t2 = time.time()
    print("temps =",t2 - t1)

########################Actualisation#########################################################################################################################################################
def associe_PUUID_aux_challengers(cursor, api_key):
    """fonction qui associe aux joueurs challengers leur puiid, peut se faire en actualisation"""
    cursor.execute("SELECT summonerId, puuid FROM Joueurs WHERE puuid = '0';")
    summoner_ids = cursor.fetchall()
    parametre = ""
    compteur = 0
    liste_summoner_id = []
    for summoner_id in summoner_ids:
        compteur += 1
        envoie_demande_PUUID_summoner(summoner_id[0], api_key)
        with open("data/summoner/data_summoner_id.json", "r") as f:#data_summoner_id.json représente le document type JSON qui contient les données obtenue par la requête pour obtenir le PUUID d'un joueur.
            objet = json.load(f)
            parametre += f"WHEN summonerId = '{objet['id']}' THEN '{objet['puuid']}' "
        if compteur == 90:
            break
    commande = f"UPDATE Joueurs SET puuid = CASE {parametre}ELSE puuid END;"
    cursor.execute(commande)


############################Actualisation###########################################################################################################################################################

"""Il reste à mettre en paramètre le fait que on supprime ou pas les joueurs qui ne sont plus challengers, et à rajouter une colonne qui donne le rank("challenger ou pas") dans notre database"""

def actualisation_table_Joueurs(cursor, api_key, suppression = False): #la fonction réalise 1 appel API Riots et 4 commandes SQL.
    """fonction qui actualise la table Joueurs, le paramètre suppresion est un booléén, qui vaut False de base et qui permet de dire si on veut spprimer les joueurs qui ne sont plus challenger de notre table"""
    envoie_demande_liste_challengers(api_key)
    cursor.execute("SELECT summonerId, leaguePoints, rank, wins, losses FROM Joueurs;")
    rows = cursor.fetchall()
    compteur_insert_to, compteur_suppression, compteur_update, compteur_joueurs  = 0, 0, 0, 0 #compteur qui permet de savoir si la ligne que l'on doit ajouter dans le tableau est la première ligne ou pas (pour les virgules dans la commande SQL c'est important)
    new_summoners_id_liste = [] #liste des summoners_ids des joueurs challengers après requête API (donc la liste actualisée)
    new_summoners_stats = {} #dictionnaire des statistiques sur les joueurs challengers reçue après requête API (donc le dictionnaire actualisé)
    parametre_inser_to, parametre_update_leaguePoints, parametre_update_rank, parametre_update_wins, parametre_update_losses = f"", f"", f"", f"", f"" #initialisation du paramètre pour la commande d'insertion de nouvelles lignes et des paramètres pour l'update des lignes.
    (liste_id_a_supprimer,Liste_summoners_ids) = ([], [])
    Liste_summoners_stats = {}
    #Liste_id_a_supprimer = liste des summoners_ids des joueurs qui étaient mais ne sont plus challengers.
    #liste des summoners_ids = liste des joueurs challengers stockée dans la database (la liste que il faut mettre à jour).
    #Liste_summoner_stats = dictionnaire des données des joueurs qui étaient challenger stockée (clé_primaire = summmonerid valeur ={sous_clé1 = leaguePoints,sous_clé2 = rank,sous_clé3 = wins,sous_clé4 = losses})
    for row in rows:
        compteur_joueurs += 1
        Liste_summoners_stats[row[0]] = {"leaguePoints" : row[1], "rank" : row[2], "wins" : row[3], "losses" : row[4]}
        Liste_summoners_ids.append(row[0])   
    with open("data/summoner/data_challenger_id.json", "r") as f:#data_challenger_id.json représente le document type JSON qui contient les données obtenue par la requête pour obtenir la liste des joueuurs challengers.
        objet = json.load(f)
        entries = objet["entries"]
        for element in entries:
            new_summoners_id_liste.append(element['summonerId'])
            new_summoners_stats[element['summonerId']] = {"leaguePoints" : element['leaguePoints'], "rank" : element['rank'], "wins" : element['wins'], "losses" : element['losses']}

            if element['summonerId'] not in Liste_summoners_ids:#partie insertion des nouvelles lignes.
                if compteur_insert_to == 0:
                    parametre_inser_to += f"('{element['summonerId']}', '{element['summonerName']}', {element['leaguePoints']}, '{element['rank']}', {element['wins']}, {element['losses']}, '0')"
                    compteur_insert_to += 1
                else :
                    parametre_inser_to += ", "
                    parametre_inser_to += f"('{element['summonerId']}', '{element['summonerName']}', {element['leaguePoints']}, '{element['rank']}', {element['wins']}, {element['losses']}, '0')"
            #print(Liste_summoners_ids)
            if element['summonerId'] in Liste_summoners_ids:#partie mise à jour des lignes
                if new_summoners_stats[element['summonerId']] != Liste_summoners_stats[element['summonerId']]:
                    compteur_update += 1
                    parametre_update_leaguePoints += f"WHEN summonerId = '{element['summonerId']}' THEN '{new_summoners_stats[element['summonerId']]['leaguePoints']}' "
                    parametre_update_rank += f"WHEN summonerId = '{element['summonerId']}' THEN '{new_summoners_stats[element['summonerId']]['rank']}' "
                    parametre_update_wins += f"WHEN summonerId = '{element['summonerId']}' THEN '{new_summoners_stats[element['summonerId']]['wins']}' "
                    parametre_update_losses += f"WHEN summonerId = '{element['summonerId']}' THEN '{new_summoners_stats[element['summonerId']]['losses']}' "

    for anciens_challengers_id in Liste_summoners_ids:#partie où on supprime des lignes.
        if anciens_challengers_id not in new_summoners_id_liste:
            compteur_suppression += 1
            liste_id_a_supprimer.append(f"'{anciens_challengers_id}'")
    id_a_supprimer_str = ','.join(map(str, liste_id_a_supprimer))

    if compteur_insert_to != 0:
        commande_insertion = f"INSERT INTO Joueurs (summonerId, summonerName, leaguePoints, rank, wins, losses, puuid) VALUES {parametre_inser_to};"
        cursor.execute(commande_insertion) #on execute la commande SQL d'insertion de nouvelles lignes (1 seul appel pour limiter la complexité temporelle).

    if compteur_suppression != 0 and suppression:    
        commande_suppression = f"DELETE FROM Joueurs WHERE summonerId IN ({str(id_a_supprimer_str)});"
        cursor.execute(commande_suppression) #on execute la commande SQL de suppression des lignes (1 seul appel pour limiter la complexité temporelle).

    if compteur_update != 0:    
        commande_update = f"UPDATE Joueurs SET leaguePoints = CASE {parametre_update_leaguePoints}ELSE leaguePoints END, rank = CASE {parametre_update_rank}ELSE rank END, wins = CASE {parametre_update_wins}ELSE wins END, losses = CASE {parametre_update_losses}ELSE losses END;"
        cursor.execute(commande_update)#on execute la commande SQL de mise à jour des données des joueurs challengers (1 seul appel pour limiter la complexité temporelle).

###############################################################################################################################################################################################################################################################################################################################           