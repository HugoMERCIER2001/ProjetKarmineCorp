import requests
import psycopg2
import json
import time
from API_Riots import *

def create_tables(cursor,conn):
    cursor.execute("CREATE TABLE matches (matchId VARCHAR(50) PRIMARY KEY, file JSON);")
    conn.commit()

def rempli_table_match(cursor,conn,matchId,file):
    cursor.execute("INSERT INTO matches (matchId,file) VALUES (%s,%s);",(matchId,file))
    conn.commit()


