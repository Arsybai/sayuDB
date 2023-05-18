from .processor import *
from .SQLite import sql
import os, json

if not os.path.isfile(f'{os.path.dirname(__file__)}/config.json'):
    with open(f'{os.path.dirname(__file__)}/config.json', 'w') as ww:
        json.dump({
    "blocked_ip": []
}, ww, indent=4)
if not os.path.isfile(f'{os.path.dirname(__file__)}/users.json'):
    with open(f'{os.path.dirname(__file__)}/users.json', 'w') as ww:
        json.dump({
    "root": {
        "username": "root",
        "password": "",
        "access": []
    }
}, ww, indent=4)

if not os.path.isdir(f'{os.path.dirname(__file__)}/datas'):
    os.makedirs(f'{os.path.dirname(__file__)}/datas')
if not os.path.isdir(f'{os.path.dirname(__file__)}/sql'):
    os.makedirs(f'{os.path.dirname(__file__)}/sql')

def show_sql_databases():
    databases = os.listdir(f'{os.path.dirname(__file__)}/sql/')
    lists = []
    for i in databases:
        if '.db' in i:
            lists.append(i.replace('.db',''))
    return lists

def export_sqldb(database, path):
    if os.path.isfile(f'{os.path.dirname(__file__)}/sql/{database}.db'):
        shutil.copyfile(f'{os.path.dirname(__file__)}/sql/{database}.db', f"{path}/{database}.db")
        print(f"Database exported [ {database}.db ]")
    else:
        print("Database not found")

def import_sqldb(dbname, path):
    if os.path.isfile(path):
        shutil.copyfile(path, f'{os.path.dirname(__file__)}/sql/{dbname}.db')
        print(f"Database Imported [ {dbname}.db ]")
    else:
        print("File not found")