from django.shortcuts import render
import psycopg2



# Create your views here.

from django.shortcuts import render
from django.db import connection

conn = psycopg2.connect( #Instaure une connexion vers la database DigitalOcean.
host="lol-database-do-user-14101148-0.b.db.ondigitalocean.com",
port="25060",
database="defaultdb",
user="doadmin",
password="AVNS_K2PNPsHumOCRMHRYaSP"
)
CURSEUR = conn.cursor()

def afficher_donnees(request):
    CURSEUR.execute("SELECT * FROM Joueurs;")
    resultats = CURSEUR.fetchall()
    return render(request, 'template.html', {'resultats': resultats})