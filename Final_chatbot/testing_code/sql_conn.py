import mysql.connector

def create_conn():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clg_va"
            )
        print("connected")
    except:
        print("not connected")
        return 0
    
    return db

