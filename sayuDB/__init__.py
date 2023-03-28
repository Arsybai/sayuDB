from .processor import *
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