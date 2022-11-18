import psycopg2
from psycopg2.extras import RealDictCursor
import time

def connection():
    while True :
        try:
            connecting_rule()
            print("Database connection was sucessful!")
            break;
        except Exception as error:
            print("Connecting to database failed")
            error_rule(error)
            


def connecting_rule():
     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password = 'damilola4u', cursor_factory=RealDictCursor)
     cursor=conn.cursor()
     return {"connect":conn, "cursor":cursor}

def error_rule(error):
     print("Error:",error )
     time.sleep(2)