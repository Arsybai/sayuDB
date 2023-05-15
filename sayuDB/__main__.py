import sys, json, os
import sayuDB.processor as sayuDB

with open(f'{os.path.dirname(__file__)}/users.json', 'r') as user:
    user = json.load(user)
with open(f'{os.path.dirname(__file__)}/config.json', 'r') as config:
    config = json.load(config)

def save_conf():
    with open(f'{os.path.dirname(__file__)}/users.json', 'w')as wconf:
        json.dump(user, wconf, indent=4)
    with open(f'{os.path.dirname(__file__)}/config.json', 'w')as wconf:
        json.dump(config, wconf, indent=4)
    return

try:
    sys.argv[1]
except:
    print("Read the doc here : https://github.com/Arsybai/blob/main/README.md")
    print("""Invalid commad. get help by
--h""")
    exit()

if sys.argv[1] == "help" or sys.argv[1] == '--h':
    print("sayuDB v1.0.0\nRead the doc here : https://github.com/Arsybai/blob/main/README.md")
    print("""
[ USERS ]
Show Users  \t\t: show users
Create user \t\t: create user <username> <password>
Remove user \t\t: remove user <username>

[ DATABASE ]
Show Database   \t: show databases
Create Database \t: create database <database_name>
Drop Database \t\t: drop database <database_name>
Grant user \t\t: grant user <username> <database_name>
Import Database \t: import database <path_to_ezdb>
Export Database \t: export database <database_name> <output_path>

[ SERVER ]
Activate Server \t: activate server <port>
Deactivate Server \t: deactivate server

if you can't access the server after activate. setup the public access by
setup public server <server_name> <port>
leave it with your server public IP in server_name if you don't have domain and the port must be same when you activate
after that you can acces it within your IP server.
    """)

elif sys.argv[1] == 'create':
    if sys.argv[2] == 'user':
        username_ = sys.argv[3]
        if username_ in user:
            sys.exit("Username already exist")
        password_ = sys.argv[4]
        user[username_] = {
            "username": username_,
            "password": password_,
            "access": []
        }
        save_conf()
        print("User created")
    elif sys.argv[2] == 'database':
        sayuDB.create_database(sys.argv[3])

elif sys.argv[1] == 'show':
    if sys.argv[2] == 'users':
        for i in user:
            print(f"> {i}")
    elif sys.argv[2] == 'databases':
        sayuDB.show_databases()

elif sys.argv[1] == 'remove':
    if sys.argv[2] == 'user':
        if sys.argv[3] in user:
            del user[sys.argv[3]]
            print("User deleted")
            save_conf()
        else:
            print("User not found")

elif sys.argv[1] == 'drop' and sys.argv[2] == 'database':
    sayuDB.drop_database(sys.argv[3])

elif sys.argv[1] == 'grant' and sys.argv[2] == 'user':
    if sys.argv[3] not in user:
        exit("User not found")
    if sys.argv[4] not in sayuDB.show_databases():
        exit("Database not found")
    user[sys.argv[3]]['access'].append(sys.argv[4])
    save_conf()
    print(f"Granted all privileges of {sys.argv[4]} to {sys.argv[3]}")

elif sys.argv[1] == 'activate' and sys.argv[2] == 'server':
    import os, platform
    if platform.system() == 'Windows':
        os.system(f'py {os.path.dirname(__file__)}/server.py {sys.argv[3]}')
    else:
        os.system(f"screen -X -S sayuDB kill")
        os.system(f"screen -dmS sayuDB")
        os.system(f"screen -S sayuDB -X stuff 'python3 {os.path.dirname(__file__)}/server.py {sys.argv[3]}\n'")
    print("Server activated. access it within your IP")

elif sys.argv[1] == 'deactivate' and sys.argv[2] == 'server':
    import os, platform
    if platform.system() == 'Windows':
        os.system(f'Just press ctrl+c')
    else:
        os.system(f"screen -X -S sayuDB kill")
    print("Server Deactivated.")

elif sys.argv[1] == 'import' and sys.argv[2] == 'database':
    sayuDB.import_database(sys.argv[3])
elif sys.argv[1] == 'export' and sys.argv[2] == 'database':
    sayuDB.export_database(sys.argv[3], sys.argv[4])

elif sys.argv[1] == 'setup' and sys.argv[2] == 'public':
    if sys.argv[3] == 'server':
        nginx_conf = """server {
    listen 80;
    server_name """+sys.argv[4]+""";
    location / {
        proxy_pass http://127.0.0.1:"""+sys.argv[5]+""";
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}"""
        os.system("sudo apt install nginx -y")
        os.system("sudo ufw allow 'Nginx Full'")
        with open("/etc/nginx/sites-enabled/sayuDB", "w") as wcc:
            wcc.write(nginx_conf)
        os.system("sudo systemctl restart nginx")
        os.system("clear")
        print(f"Successfully setup public server.\nhttp://{sys.argv[4]}")
    else:
        print("Public what? what must I setup?")