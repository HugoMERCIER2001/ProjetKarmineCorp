import requests
import psycopg2
import json
import time
from API_Riots import *

def create_table(cursor,conn):
    cursor.execute("CREATE TABLE Liaison (matchId VARCHAR(50), summonerId VARCHAR(50), PRIMARY KEY (matchId,summonerId));")
    conn.commit()

def rempli_table_liaison(matchId,summonerId,cursor,conn):
    cursor.execute("INSERT INTO Liaison (matchId,summonerId) VALUES (%s,%s);",(matchId,summonerId))
    conn.commit()
