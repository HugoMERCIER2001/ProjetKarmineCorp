import requests
import psycopg2
import json
import time

CLE_API = 'RGAPI-1d6c027d-c2a6-4ec2-83f2-c297c0135b29'


##############################################Partie API Riots################################################################################

def envoie_demande_liste_challengers(api_key):
    """envoie une demande GET à l'API Riot pour obtenir la liste des ID des joueurs challengers"""
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
    """envoie une demande GET à l'API Riot pour obtenir le PUUID d'un joueur de summonerID : 'summoner_id'"""
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
    """envoie une demande GET à l'API Riot pour obtenir la liste des ID des matchs niveau Challengers"""
    requete = f'https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
    # Exemple de requête GET
    response = requests.get(requete)

    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json() # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("data_match_idea.json", "w") as f:
            json.dump(data, f)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)



##############################################Partie PostgreSQL######################################################################
conn = psycopg2.connect( #Instaure une connexion vers la database DigitalOcean.
host="lol-database-do-user-14101148-0.b.db.ondigitalocean.com",
port="25060",
database="defaultdb",
user="doadmin",
password="AVNS_K2PNPsHumOCRMHRYaSP"
)
cursor = conn.cursor()#définit le curseur(besoin du curseur pour executer des commandes en PostgreSQL)


def rempli_table_challenger():
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
            parametre += f"('{element['summonerId']}','{element['summonerName']}', {element['leaguePoints']}, '{element['rank']}',{element['wins']},{element['losses']})"
    commande = f"INSERT INTO Joueurs (summonerId, summonerName, leaguePoints, rank, wins, losses) VALUES {parametre}"
    cursor.execute(commande)
    t2 = time.time()
    print("temps =",t2 - t1)

##############################################################################################################################################################################################################################


def associe_PUUID_aux_challengers(api_key):
    print()
    cursor.execute("SELECT summonerId FROM Joueurs WHERE puuid = NULL")
    summoner_ids = cursor.fetchall()
    liste_time = []
    compteur_appel = 0
    liste_time.append(time.time())
    t1 = time.time()
    for summoner_id in summoner_ids:
        compteur_appel += 1
        envoie_demande_PUUID_summoner(summoner_id, api_key)
        with open("data_summoner_id.json", "r") as f:#data_summoner_id.json représente le document type JSON qui contient les données obtenue par la requête pour obtenir le PUUID d'un joueur.
            objet = json.load(f)
        if compteur_appel == 20:
            t2 = time.time()
        break
    print(t2 - t1)



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



def main(api_key):
    associe_PUUID_aux_challengers(api_key)
    #envoie_demande_liste_challengers(api_key)
    #envoie_demande_liste_match_challengers(api_keys):
    cursor.execute("CREATE TABLE Games (gameId INT, summonerId TEXT, championId INT, lane TEXT, role TEXT, win TEXT, PRIMARY KEY (gameId));")
    #cursor.execute("CREATE TABLE Joueurs (summonerId TEXT,summonerName TEXT, leaguePoints INT, rank TEXT,wins INT, losses INT, PRIMARY KEY (summonerId));")
    #cursor.execute("DROP TABLE Joueurs;")
    #rempli_table_challenger()
    conn.commit()
    """cursor.execute("SELECT * FROM Joueurs")
    rows = cursor.fetchall()
    for row in rows:
    print(row)"""

main(CLE_API)
