import sqlite3
import os.path
import json

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
    __cursor.execute(f'SELECT {select_str} FROM {from_} {command};')
    list = __cursor.fetchall()
    __db_close()
    return list

def selectUserById(UserId):
    return select("*","user",f"where id = '{UserId}' ")

def selectToJson(select_str:str,from_:str,command:str) -> dict:
    data = select(select_str,from_,command)
    str = ''
    for item in data[0]:
        str = str + item
    str = str.replace("'",'"')
    return json.loads(str)

def insert(table:str,data:str):
    __conn_db()
    __cursor.execute(f'INSERT INTO {table} VALUES ({data});')
    __conn.commit()
    __db_close()

def insertItem(table:str,item:str,data:str):
    __conn_db()
    __cursor.execute(f'INSERT INTO {table} ({item}) VALUES ({data});')
    __conn.commit()
    __db_close()

def update(table:str,set:str, where:str):
    __conn_db()
    __cursor.execute(f'UPDATE {table} SET {set} WHERE {where};')
    __conn.commit()
    __db_close()