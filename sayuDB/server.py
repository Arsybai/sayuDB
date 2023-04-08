from flask import Flask, jsonify, request
import os
import json
import base64
import sys
import sayuDB

app = Flask(__name__)
app.secret_key = "OAKsoaksSayuAskpasdasd"
application = app

def encode_base64(input_string):
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decode_base64(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

def user():
    with open(f'{os.path.dirname(__file__)}/users.json', 'r') as user:
        user = json.load(user)
    return user
def config():
    with open(f'{os.path.dirname(__file__)}/config.json', 'r') as config:
        config = json.load(config)
    return config

def save_conf():
    with open('users.json', 'w')as wconf:
        json.dump(user(), wconf, indent=4)
    with open('config.json', 'w')as wconf:
        json.dump(config(), wconf, indent=4)
    return

def checkAuth():
    username = decode_base64(request.form['username'])
    password = decode_base64(request.form['password'])
    if username not in user():
        return "User not found"
    if password != user()[username]['password']:
        return "Invalid credentials"
    if username == 'root':
        return "Action rejected"
    return True

def hasAccess(username, database):
    if database in user()[username]['access']:
        return True
    return

@app.route('/')
def ping():
    return 'ok'

@app.route('/oauth')
def oauth():
    username = decode_base64(request.form['username'])
    password = decode_base64(request.form['password'])
    if username not in user():
        return "User not found"
    if password != user()[username]['password']:
        return "Invalid credentials"
    return 'ok'

@app.route('/existence')
def database_existence():
    username = decode_base64(request.form['username'])
    database = request.form['database']
    db = sayuDB.show_databases()
    if database not in db:
        return "Database not found in server"
    if not checkAuth():
        return "Authorization rejected"
    if username not in user() or database not in user()[username]['access']:
        return "Database not found in server"
    return 'ok'
    
@app.route('/commit', methods=['POST'])
def commit():
    username = decode_base64(request.form['username'])
    database = request.form['database']
    content = decode_base64(request.form['content'])
    if not checkAuth():
        return "Authorization rejected"
    if not hasAccess(username, database):
        return "Database not found in server"
    sayuDB.sayuDB(database).save_db(eval(content))
    return 'ok'

@app.route('/pull')
def pull():
    username = decode_base64(request.form['username'])
    database = request.form['database']
    if not checkAuth():
        return "Authorization rejected"
    if not hasAccess(username, database):
        return "Database not found in server"
    return jsonify(sayuDB.sayuDB(database).openDB())


if __name__ == "__main__":
    app.run(debug=True, port=int(sys.argv[1]), host='0.0.0.0')