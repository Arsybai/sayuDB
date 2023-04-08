import json
import requests
import os
import base64

def encode_base64(input_string):
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decode_base64(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

def check_network(host):
    response = requests.get(host)
    return response

def sendRequest(host, data, method='GET'):
    if method == 'GET':
        response = requests.get(host, data=data).text
    elif method == 'POST':
        response = requests.post(host, data=data).text
    else:
        response = "Invalid method"
    return response

class remote:

    def __init__(self, username:str, password:str, host:str):
        self.username = username
        self.password = password
        self.host = host
        response = sendRequest(host+'/oauth', {'username':encode_base64(username), 'password':encode_base64(password)})
        if response != 'ok':
            exit(response)
        return
    
    def database_exsistence(self, database:str):
        response = sendRequest(self.host+'/existence', {'username':encode_base64(self.username), 'password':encode_base64(self.password), 'database':database})
        if response != 'ok':
            exit(response)
        return True
    
    def commit_database(self, database:str, content):
        response = sendRequest(self.host+'/commit', {'username':encode_base64(self.username), 'password':encode_base64(self.password), 'database':database, 'content':encode_base64(str(content))}, 'POST')
        if response != 'ok':
            exit(response)
        return True
    
    def pull_database(self, database:str):
        response = sendRequest(self.host+'/pull', {'username':encode_base64(self.username), 'password':encode_base64(self.password), 'database':database})
        return json.loads(response)