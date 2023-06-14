import requests
import psycopg2
import json
import time
import glob
import os
from API_Riots import *

PARAM_TEXT = ""
print("PARAM TEXT = ", PARAM_TEXT)

clée_API_openai = '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'


#####################Création du fichier clés_Match.txt###################################################################################################################################

def recupere_les_clés_MatchJSON(fichier_JSON, L_clés_visités, L_clés, chemin_acces_fichier_txt):
    """
    Fonction Récursive.
    Fonction qui récupère le nom de toutes les clés contenue dans un fichier JSON et les stocks dans un fichier.txt.
    fichier_JSON est le fichier JSON que l'on va traiter.
    L_clés représente la liste d'enchainement de clé nécéssaire pour aller jusqu'à l'objet qui nous intéresse.
    chemin_acces_fichier_txt représente le chemin d'acces pour le ficheier.txt dans lequel on va écrire.
    """
    with open(f"{fichier_JSON}", "r") as f:
        #print("on est rentré", L_clés)
        data = json.load(f)
        f.close()
    for clé in L_clés:
        if type(clé) == str:
            data = data.get(clé, 'Problème')
        if type(clé) == int:
            data = data[clé]
    if type(data) == dict:
        clés_suiv = data.keys()
        for clé_suiv in clés_suiv:
            if clé_suiv not in L_clés_visités:
                L_chemin_clé = recupere_les_clés_MatchJSON(fichier_JSON,L_clés_visités, L_clés + [clé_suiv], chemin_acces_fichier_txt)
                for clé_du_chemin in L_chemin_clé:
                    if clé_du_chemin not in L_clés_visités and not 'participants':
                        if type(clé_du_chemin) == str:
                            L_clés_visités.append(clé_du_chemin)
    if type(data) == list:
        for i in range(len(data)):
            L_chemin_clé = recupere_les_clés_MatchJSON(fichier_JSON,L_clés_visités, L_clés + [i], chemin_acces_fichier_txt)
    if type(data) != dict and type(data) != list:
        global PARAM_TEXT
        chemin_acces_cle = f""
        for clé in L_clés:
            if type(clé) == int:
                if clé != 0:
                    return L_clés
            if clé != L_clés[len(L_clés) - 1]:
                chemin_acces_cle += f"{clé}-"
            if clé == L_clés[len(L_clés) - 1]:
                chemin_acces_cle += f"{clé}"
                nom_clé = f"{clé}"
                type_clé = f"{type(clé)}"
                PARAM_TEXT += f"Table où est stockée la data : ''\n"
                PARAM_TEXT += f"Nom de la clé dans la database : ''\n"
                PARAM_TEXT += f"Description de la clé : ''\n"
                PARAM_TEXT += f"//////\n"
                PARAM_TEXT += f"Nom clé : {nom_clé}\n"
                PARAM_TEXT += f"Chemin de clés pour obtenir cette clé : {chemin_acces_cle}\n"
                PARAM_TEXT += f"Type de la valeur stockée : {type_clé}\n"
                PARAM_TEXT += f"Exemple de valeur possible : {data}\n"
                PARAM_TEXT += "--------------------------------------------------------------------------------------\n"
                print("ON A ECRITTTT")
                print("pour L_clés =", L_clés, "data =", type(data))

        f.close()            
    return L_clés

def ecrit_clés():
        param_textuel = recupere_les_clés_MatchJSON('data/match/match_info/EUW1_6335475357.json', [], [], 'clés_Match2.txt')
        with open("clés_Match.txt", "w") as f:
            global PARAM_TEXT
            print("PARAM_TEXT2 = ", PARAM_TEXT)
            f.write(PARAM_TEXT)
            f.close()


###################################################################################################################################################################################


