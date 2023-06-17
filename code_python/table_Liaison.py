import requests
import psycopg2
import json
import time
from API_Riots import *



################################Création de la table de liaison##################################################################################################


##################Fonctions utilisées pour la création de la table de liaison###############################################################################
def create_table_liaison_vide(cursor):
    """
    Crée la table Liaison
    """
    cursor.execute("CREATE TABLE Liaison (matchId VARCHAR(50), summonerId TEXT, PRIMARY KEY (matchId,summonerId));")

def cree_liste_match(cursor, api_key):
    """
    fonction qui crée les listes : list_matchId, list_summonerId pour les joueurs challengers
    """
    Liste_summoners_ids, Liste_match = [], []
    compteur_puuid_manquant = 0
    compteur_appels_API = 0
    cursor.execute("SELECT summonerId, puuid FROM Joueurs")
    rows = cursor.fetchall()
    for row in rows :
        if row[1] != '0':
            get_games_by_puuid(row[1], api_key, 100)
            compteur_appels_API +=1
            with open("../ProjetKarmineCorp/data/match/list_match.json", "r") as f:
                objet = json.load(f)
                for match_id in objet:
                    Liste_match.append(match_id)
                    Liste_summoners_ids.append(row[0])
        if compteur_appels_API == 10:
            break            
        else :
            compteur_puuid_manquant += 1
    print(f"Il manque {compteur_puuid_manquant} puuid à calculer, veuillez lancez la fonction d'association des puuids")
    rempli_table_liaison(Liste_match, Liste_summoners_ids, cursor)



def rempli_table_liaison(list_matchId,list_summonerId,cursor):
    """
    Rempli la table Liaison avec les matchs de la liste list_matchId et les summonerId de la liste list_summonerId
    """
    parametre = ""
    for i in range(len(list_matchId)):
        if i != 0:
            parametre += ","
        parametre += f"('{list_matchId[i]}', '{list_summonerId[i]}')" 
    cursor.execute(f"INSERT INTO Liaison (matchId,summonerId) VALUES {parametre};")
    

########################FONCTION QU'IL FAUT APPELER POUR CREER LA TABLE DE LIAISON COMPLETE###########################################################################

def cree_table_liaison_complete(cursor, api_key):
    """
    Fonction qui crée et rempli la table de liaison, il faut juste que la table joueur soit déjà définie !
    """
    create_table_liaison_vide(cursor)
    cree_liste_match(cursor, api_key)
    print("FIN")

#######################ACTUALISATION DE LA TABLE DE LIAISON#############################################################################################################

def actualisation_table_liaison(cursor, api_key):
    Liste_deja_sauvegarde = []
    cursor.execute("SELECT matchId, summonerId FROM Liaison")
    données = cursor.fetchall()
    for couple in données:
        Liste_deja_sauvegarde.append((couple[0], couple[1]))
    Liste_nouveaux_summoners_ids, Liste_nouveaux_match = [], []
    compteur_puuid_manquant, compteur_actualisation, compteur_appels_API = 0, 0, 0
    cursor.execute("SELECT summonerId, puuid FROM Joueurs")
    select2 = cursor.fetchall()
    for summoner_puuid in select2 :
        if summoner_puuid[1] != '0':
            get_games_by_puuid(summoner_puuid[1], api_key, 100)
            compteur_appels_API +=1
            with open("../ProjetKarmineCorp/data/match/list_match.json", "r") as f:
                objet = json.load(f)
                i = 0
                while (objet[i],summoner_puuid[0]) not in Liste_deja_sauvegarde:
                    Liste_nouveaux_match.append(objet[i])
                    Liste_nouveaux_summoners_ids.append(summoner_puuid[0])
                    compteur_actualisation += 1
                    i += 1
                    if i == 100:
                        break
        if summoner_puuid[1] == '0' :
            compteur_puuid_manquant += 1
            print(compteur_puuid_manquant)
    print(f"Il manque {compteur_puuid_manquant} puuid à calculer, veuillez lancez la fonction d'association des puuids")
    print(compteur_actualisation)
    if compteur_actualisation != 0:
        rempli_table_liaison(Liste_nouveaux_match, Liste_nouveaux_summoners_ids, cursor)
        
##########################################################################################################################################################"#######################################"