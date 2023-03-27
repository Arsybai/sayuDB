import sys, json
import sayuDB.processor as sayuDB

with open('sayuDB/users.json', 'r') as user:
    user = json.load(user)
with open('sayuDB/config.json', 'r') as config:
    config = json.load(config)

def save_conf():
    with open('sayuDB/users.json', 'w')as wconf:
        json.dump(user, wconf, indent=4)
    with open('sayuDB/config.json', 'w')as wconf:
        json.dump(config, wconf, indent=4)
    return

try:
    sys.argv[1]
except:
    print("Read the doc here : https://github.com/Arsybai/sayuDB/blob/main/README.md")
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

[ SERVER ]
Activate Server \t: activate server <port>
Block IP  \t\t\t: block ip <ip>
    """)
    exit()

if sys.argv[1] == "help" or sys.argv[1] == '--h':
    print("sayuDB v0.0.1\nRead the doc here : https://github.com/Arsybai/sayuDB/blob/main/README.md")
    print("""
[ USERS ]
Show Users  \t\t: show users
Create user \t\t: create user <username> <password>
Remove user \t\t: remove user <username>

[ DATABASE ]
Show Database   \t: show database
Create Database \t: create database <database_name>
Drop Database \t\t: drop database <database_name>
Grant user \t\t: grant user <username> <database_name>

[ SERVER ]
Activate Server \t: activate server <port>
Block IP  \t\t: block ip <ip> (coming soon)
Unblock IP  \t\t: unblock ip <ip> (coming soon)
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
        os.system(f'py sayuDB/server.py {sys.argv[3]}')
    else:
        os.system(f'python3 sayuDB/server.py {sys.argv[3]}')