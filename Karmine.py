import requests



def requestAPI(api_key):
    response = requests.get("https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key{api_key}")
    return response.json()


