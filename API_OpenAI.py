import requests
import psycopg2
import json
import time
import glob
import os
import openai

clée_API_openai = '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'

def demande_def_clé_match_chatGPT(clé):
    question = f"Peux tu m'expliquer ce que représente la clé {clé} du fichier json réponse de l'API Riot demandant les statistiques d'un match de League of Legend ? "
    response = openai.Completion.create(
    engine='davinci',
    prompt=question,
    max_tokens=100,
    n=1,
    stop=None,
    )
    reponse_complete = response['choices'][0]['text']
    L_reponse = reponse_complete.split("\n")
    print("REPONSE COMPLETE =================",reponse_complete)
    print("REPONSEEEEE ====", L_reponse[0])