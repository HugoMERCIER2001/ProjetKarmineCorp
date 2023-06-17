import requests
import psycopg2
import json
import time

T_APP1 = 'pas encore définie'
T_APP2 = 'pas encore définie'

T0_METH1 = 'pas encore définie'
T0_METH2 = 'pas encore définie'

T1_METH1 = 'pas encore définie'
T1_METH2 = 'pas encore définie'

T2_METH1 = 'pas encore définie'
T2_METH2 = 'pas encore définie'

T3_METH1 = 'pas encore définie'
T3_METH2 = 'pas encore définie'

T4_METH1 = 'pas encore définie'
T4_METH2 = 'pas encore définie'

##################################Fonction permettant de ne pas dépasser les limites de requetes/s###########################################################################################################################################

def verifie_pas_de_depassement(response, type_de_requete = 0):
    """
    Fonction qui assure que on dépasse pas le nombre de requetes limite par secondes
    type_de_requete peux valoir :
                - 0 = liste_challenger ==> signifie que il s'agit de la requete permettant d'obtenir la liste des joueurs challengers.
                - 1 = PUUID_by_summonner ==> signifie que il s'agit de la requete permettant d'obtenir le PUUID d'un joueur à partir de son summonerId.
                - 2 = liste_match_challenger ==> signifie que il s'agit de la requete permettant d'obtenir la liste des matchId des matchs joués entre challengers.
                - 3 = match_by_puuid ==> signifie que il s'agit de la requete permettant d'obtenir la liste des matchId des matchs joué par le joueur ayant le PUUID donné.
                - 4 = match_info ==> signifie que il s'agit de la requete permettant d'obtenir les infos d'un match à partir du match_id.
    """
    #global T_APP1, T_APP2
    #print(T_APP1, T_APP2)
    X_App_Rate_Limit = response.headers.get('X-App-Rate-Limit')#gère les limitations de requetes liés à la clé API.
    X_App_Rate_Limit_count = response.headers.get('X-App-Rate-Limit-Count')
    Liste_Limit_App = [] #liste qui au final va contenir : [0 - max_operations_App1, 1 - temps_App1, 2 - max_operations_App2, 3 - temps_App2, 4 - nbr_operation_faite_App1, 5 - INUTILE, 6 - nbr_operation_faite_App2, 7 - INUTILE]
    elements_de_X_App_Rate_Limit = X_App_Rate_Limit.split(',')
    for element in elements_de_X_App_Rate_Limit:
        sous_elements = element.split(':')
        for données in sous_elements :
            Liste_Limit_App.append(int(données))
    elements_de_X_App_Rate_Limit_Count = X_App_Rate_Limit_count.split(',')
    for element in elements_de_X_App_Rate_Limit_Count :
        sous_elements = element.split(':')
        for données in sous_elements :
            Liste_Limit_App.append(int(données))

    """X_Method_Rate_Limit = response.headers.get('X-Method-Rate-Limit')#gère les limitations de requetes liés à la requete
    X_Method_Rate_Limit_Count = response.headers.get('X-Method-Rate-Limit-Count')
    Liste_Limit_Meth = [] #Liste qui au final va contenir : [0 - max_operations_Meth1, 1 - temps_Meth1]
    elements_de_X_Method_Rate_Limit = X_Method_Rate_Limit.split(',')
    for element in elements_de_X_Method_Rate_Limit:
        sous_elements = element.split(':')
        for données in sous_elements:
            Liste_Limit_Meth.append(int(données))
    max_operations_Meth1 = int(X_Method_Rate_Limit[0:2])
    temps_Meth1 = int(X_Method_Rate_Limit[3:])
    nbr_operation_faite_Meth1 = int(X_Method_Rate_Limit_Count[0:2])"""
    #if len(X_Method_Rate_Limit) > 5:
        #max_operations_Meth2 = X_Method_Rate_Limit[6:8]
        #temps_Meth2 = X_Method_Rate_Limit[9:11]
        #nbr_operation_faite_Meth2 = X_Method_Rate_Limit_Count[6:8]

    if Liste_Limit_App[4] <= 1:
        global T_APP1
        T_APP1 = time.time()
    if Liste_Limit_App[6] <= 1:
        global T_APP2
        T_APP2 = time.time()
    if Liste_Limit_App[4] >= Liste_Limit_App[0]:
        print(Liste_Limit_App[1], time.time(), T_APP1)
        temps_a_attendre1 = Liste_Limit_App[1] - (time.time() - T_APP1)
        print("On dépasse, on a que on a fait ", Liste_Limit_App[1], "alors que on pouvait en faire que", Liste_Limit_App[0])
        time.sleep(temps_a_attendre1)

    if Liste_Limit_App[6] >= Liste_Limit_App[2] :
        print(Liste_Limit_App[3], time.time(), T_APP2)
        temps_a_attendre2 = Liste_Limit_App[3] - (time.time() - T_APP2)
        print("On dépasse, on a que on a fait ", Liste_Limit_App[6], "alors que on pouvait en faire que", Liste_Limit_App[2])
        time.sleep(temps_a_attendre2)

    """if nbr_operation_faite_Meth1 <= 1:
        if type_de_requete == 0:
            global T0_METH1
            T0_METH1 = time.time()
        if type_de_requete == 1:
            global T1_METH1
            T1_METH1 = time.time()
        if type_de_requete == 2:
            global T2_METH1
            T2_METH1 = time.time()
        if type_de_requete == 3:
            global T3_METH1
            T3_METH1 = time.time()
        if type_de_requete == 4:
            global T4_METH1
            T4_METH1 = time.time()
    if nbr_operation_faite_Meth1 >= max_operations_Meth1:
        if type_de_requete == 0:
            temps_a_attendre1 = temps_Meth1 - (time.time() - T0_METH1)
            time.sleep(temps_a_attendre1)
        if type_de_requete == 1:
            temps_a_attendre1 = temps_Meth1 - (time.time() - T0_METH1)
            time.sleep(temps_a_attendre1)
        if type_de_requete == 2:
            temps_a_attendre1 = temps_Meth1 - (time.time() - T0_METH1)
            time.sleep(temps_a_attendre1)
        if type_de_requete == 3:
            temps_a_attendre1 = temps_Meth1 - (time.time() - T0_METH1)
            time.sleep(temps_a_attendre1)
        if type_de_requete == 4:
            temps_a_attendre1 = temps_Meth1 - (time.time() - T0_METH1)
            time.sleep(temps_a_attendre1)
        print("On a dépassé en temps sur la méthode")  """




##################################Fonction de requêtes API#####################################################################################################

def envoie_demande_liste_challengers(api_key):
    """
    envoie une demande GET à l'API Riot pour obtenir la liste des ID des joueurs challengers
    """
    requete = f'https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
    response = requests.get(requete)
    verifie_pas_de_depassement(response, 0)
    # Vérifier le code de réponse
    if response.status_code == 200:
    # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("../ProjetKarmineCorp/data/summoner/data_challenger_id.json", "w") as f:
            json.dump(data, f)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)




def envoie_demande_PUUID_summoner(summoner_id, api_key):
    """
    envoie une demande GET à l'API Riot pour obtenir le PUUID d'un joueur de summonerID : 'summoner_id'
    """
    requete = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={api_key}'
    response = requests.get(requete)
    verifie_pas_de_depassement(response, 1)
    print(response.headers)
    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("../ProjetKarmineCorp/data/summoner/data_summoner_id.json", "w") as f:
            json.dump(data, f)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)




def envoie_demande_liste_match_challengers(api_key):
    """
    envoie une demande GET à l'API Riot pour obtenir la liste des ID des matchs niveau Challengers
    """
    requete = f'https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
    # Exemple de requête GET
    response = requests.get(requete)
    verifie_pas_de_depassement(response, 2)

    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("../ProjetKarmineCorp/data/match/data_match_id.json", "w") as f:
            json.dump(data, f)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)





def get_games_by_puuid(puuid, api_key, nb_games=100):
    """
    Récupérer les nb_games derniers matchs d'un joueur à partir de son PUUID
    Pour les stocker dans le json list_match
    """
    request = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={nb_games}&api_key={api_key}"
    response = requests.get(request)
    verifie_pas_de_depassement(response, 3)
    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("../ProjetKarmineCorp/data/match/list_match.json", "w") as f:
            json.dump(data, f)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)



def get_match_by_id(match_id, api_key):
    """
    Récupère les infos d'un match à partir du match_id
    Stocke ces données dans un json du nom du match_id dans le fichier match_info
    """
    request = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    response = requests.get(request)
    verifie_pas_de_depassement(response, 4)
    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open(f"../ProjetKarmineCorp/data/match/match_info/{match_id}.json", "w") as f:
            json.dump(data, f)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)


def get_timeline_by_id(match_id, api_key):
    """
    Récupère les infos d'un match à partir du match_id
    Stocke ces données dans un json du nom du match_id dans le fichier match_info
    """
    request = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={api_key}"
    response = requests.get(request)
    verifie_pas_de_depassement(response, 0)
    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open(f"../ProjetKarmineCorp/data/match/match_timeline/{match_id}.json", "w") as f:
            json.dump(data, f)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)
#####################################################################################################################################################################
