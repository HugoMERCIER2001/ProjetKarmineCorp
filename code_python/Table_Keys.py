import requests
import psycopg2
import json
import time
import glob
import os
from code_python.API_Riots import *



#########Fonction qui rempli correctement à partir d'un fichier txt bien formaté, la table Key###############################################################################

def rempli_table_clés(cursor, fichier_txt, type_fichier):
    """Fonction qui prend un entrée un fichier .txt formaté par la fonction précédente et rempli la table des clés correctement avec
        Le paramètre type_fichier est un str qui porte le nom Match_JSON par exemple si on rempli la table avec un fichier txt qui est un fichier JSON de Match.
    """
    cle_restante = ""
    with open(f"{fichier_txt}", "r") as f:
        nb_cle = 0
        text = f.read()
        L_bloc = text.split("--------------------------------------------------------------------------------------")
        parametre_insertion = f""
        i = 0
        for bloc in L_bloc:
            nb_cle += 1
            L = bloc.split("\n")
            if len(L) > 2:
                if L[1] != "Table où est stockée la data : ''":
                    Liste = L[1].split("'")
                    Table_stockage = f"'{Liste[1]}'"
                    Liste = L[2].split("'")
                    Nom_clé = f"'{Liste[1]}'"
                    Liste = L[3].split("'")
                    Description = f""
                    for j, elements in enumerate(Liste) :
                        if j >= 1:
                            Description += f"{elements}"
                    Liste = L[5].split(" ")
                    Nom_clé_JSON = f"'{Liste[3]}'"
                    Liste = L[6].split(" ")
                    Chemin_clé =  f"'{Liste[8]}'"
                    Liste = L[7].split(" ")
                    Type_valeur = f"'{Liste[6]}'"
                    Nom_fichier = f"'{type_fichier}'"
                    if i != 0:
                        parametre_insertion += ", "
                    parametre_insertion += f"({Table_stockage}, {Nom_clé}, '{Description}', {Nom_clé_JSON}, {Chemin_clé}, {Type_valeur}, {Nom_fichier}, '0')"
                    i += 1
                else :
                    print(L)
                    for k in range(len(L)):
                        if k != 0 and k != 9:
                            cle_restante += f"{L[k]}\n"
                    cle_restante += "--------------------------------------------------------------------------------------\n"
    with open("../fichier_clé_txt/clés_Match_restantes.txt", "w") as f:
        f.write(cle_restante)
        f.close()
    cursor.execute(f"INSERT INTO Key (Table_stockage, Nom_clé, Description, Nom_clé_JSON, Chemin_clé, Type_valeur, Nom_fichier, Extraite) VALUES {parametre_insertion};")


############## Création de la Table ######################################################################################################################################################################

def cree_table_cle_vide(cursor):
    """Fonction qui crée la table vide Key."""
    cursor.execute("CREATE TABLE Key (Nom_clé TEXT, Nom_Fichier TEXT, Table_stockage TEXT, Nom_clé_JSON TEXT, Type_valeur TEXT, Chemin_clé TEXT, Description TEXT, Extraite INT, PRIMARY KEY (Nom_clé, Table_stockage));")


def cree_table_cle_pleine(cursor):
    """Fonction qui crée et rempli la table Key, il faut faire appel à cette fonction pour créer la table Key.
    (Il faut finir de modifier le fichier param_clés.txt pour pouvoir correctement créer la table clé).
    """
    cree_table_cle_vide(cursor)
    rempli_table_clés(cursor, "../fichier_clé_txt/param_clés.txt", "Match_JSON")


#################Ajout de nouvelles clés à partir d'un fichier txt bien formaté#####################################################################################################################

def rajoute_cle(cursor, nouvelle_cle_txt):
    """Fonction qui permet de rajouter une clé.
        le paramètre nouvelle_cle_txt correspond à un fichier txt bien formaté contenant les nouvelles clés.
    """