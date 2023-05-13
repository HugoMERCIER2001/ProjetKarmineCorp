import requests


CLE_API = 'RGAPI-e36f5233-1d2a-4bf2-b91e-9cfe410de395'

def envoie_demande_liste_challengers():
    """envoie une demande GET à l'API Riot pour obtenir la liste des ID des joueurs challengers"""
    # Exemple de requête GET
    response = requests.get('https://api.example.com/endpoint')

    # Vérifier le code de réponse
    if response.status_code == 200:
        # La requête a réussi
        data = response.json()  # Récupérer les données de réponse au format JSON
        # Traiter les données
        print(data)
    # Gérer les erreurs de requête
    else:
        print('La requête a échoué. Code de réponse :', response.status_code)