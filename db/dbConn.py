import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "./card.db")
__conn:sqlite3.Connection
__cursor:sqlite3.Cursor 

def __conn_db():
    global __conn,__cursor
    __conn = sqlite3.connect(db_path)
    __cursor = __conn.cursor()

def __db_close():
    __cursor.close()
    __conn.close()


def select(select_str:str,from_:str,command:str):
    __conn_db()
    __cursor.execute('SELECT * FROM card;')
    __cursor.execute(f'SELECT {select_str} FROM {from_} {command};')
    list = __cursor.fetchall()
    __db_close()
    return list



