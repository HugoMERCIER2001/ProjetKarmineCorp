import requests
import psycopg2
import json
import time

CLE_API = 'RGAPI-e36f5233-1d2a-4bf2-b91e-9cfe410de395'

def envoie_demande_liste_challengers(api_key):
    """envoie une demande GET à l'API Riot pour obtenir la liste des ID des joueurs challengers"""
    requete = f'https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
    print(requete)
    # Exemple de requête GET
    response = requests.get(requete)

    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json()  # Récupérer les données de réponse au format JSON
        # Traiter les données
        with open("data.json", "w") as f:
            json.dump(data, f)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)
#envoie_demande_liste_challengers(CLE_API)

conn = psycopg2.connect( #Instaure une connexion vers la database DigitalOcean.
    host="private-lol-database-do-user-14101148-0.b.db.ondigitalocean.com",
    port="25060",
    database="defaultdb",
    user="doadmin",
    password="AVNS_K2PNPsHumOCRMHRYaSP"
)

cursor = conn.cursor()#définit le curseur(besoin du curseur pour executer des commandes en PostgreSQL)
cursor.execute("CREATE TABLE Joueurs (summonerId TEXT,summonerName TEXT, leaguePoints INT, rank TEXT,wins INT, losses INT, PRIMARY KEY (summonerId))")

def rempli_table():
    with open("data.json", "r") as f:
        objet = json.load(f)
        """print(objet["name"], "\n")""" #liste des clés non utilisées.
        """print(objet["tier"], "\n")"""
        """print(objet["leagueId"],"\n")"""
        """print(objet["queue"], "\n")"""
        entries = objet["entries"] #entries est une liste d'éléments de type dictionnaire.
        t1 = time.time()
        for element in entries :
            i = 0
            summonerId, summonerName, leaguePoints, rank, wins, losses = element["summonerId"],element["summonerName"], element["leaguePoints"], element["rank"],element["wins"],element["losses"]
            commande = f"INSERT INTO Joueurs (summonerId, summonerName, leaguePoints, rank, wins, losses) VALUES ('{summonerId}','{summonerName}', {leaguePoints}, '{rank}', {wins}, {losses})"
            cursor.execute(commande)
        t2 = time.time()
        print("temps =",t2 - t1)

cursor.execute("SELECT * FROM Joueurs")
rows = cursor.fetchall()
for row in rows:
    print(row)