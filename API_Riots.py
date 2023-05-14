import requests
import psycopg2
import json
import time


def envoie_demande_liste_challengers(api_key):
    """
    envoie une demande GET à l'API Riot pour obtenir la liste des ID des joueurs challengers
    """
    requete = f'https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
    response = requests.get(requete)
    # Vérifier le code de réponse
    if response.status_code == 200:
    # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("data_challenger_id.json", "w") as f:
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
    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("data_summoner_id.json", "w") as f:
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

    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("data_match_id.json", "w") as f:
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
    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("list_match.json", "w") as f:
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
    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open(f"match_info/{match_id}.json", "w") as f:
            json.dump(data, f)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)