import requests
import psycopg2
import json
import time
import glob
import os
from API_Riots import *

def rempli_table_clés(cursor, fichier_txt):
    """Fonction qui prend un entrée un fichier .txt formaté par la fonction précédente et rempli la table des clés correctement avec"""
    with open(f"{fichier_txt}", "r") as f:
        text = f.read()
        L_bloc = text.split("--------------------------------------------------------------------------------------")
        L_table_stockage, L_nom_clé, L_vrai_nom, L_type, L_description = [], [], [], [], []
        for bloc in L_bloc:
            L = bloc.split("\n")
            if len(L) != 2:
                for element in L :
                    print("len(l) =",len(L))
                    print("0", L[0])
                    print("1",L[1])
                    print("2",L[2])
                    print("3",L[3])
                    print("4",L[4])
                    print(L[5])
                    print(L[6])
                    print(L[7])
                    print(L[8])

rempli_table_clés("cursor", "param_clés.txt")