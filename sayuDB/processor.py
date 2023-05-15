import json, os, shutil, sys
from tabulate import tabulate
from operator import itemgetter
import sayuDB.remote as remote
import datetime, random, time

functions = [
    "today()",
    "index()",
    "genID()",
    "increase()"
]

def genID():
    return random.randint(10000, 99999)

def today():
    now = datetime.datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    return dt_string

def create_database(name: str):
    config_ = {
        "name":name
    }
    if not os.path.isfile(f'{os.path.dirname(__file__)}/datas/{name}.ezdb'):
        with open(f'{os.path.dirname(__file__)}/datas/{name}.ezdb', 'w') as cdb:
            json.dump(config_, cdb, indent=4)
        print(f"Database created [ {name} ]")
    else:
        print("Database already exist")
        
def show_databases():
    databases = os.listdir(f'{os.path.dirname(__file__)}/datas/')
    lists = []
    for i in databases:
        if '.ezdb' in i:
            print(f"> {i.replace('.ezdb','')}")
            lists.append(i.replace('.ezdb',''))
    return lists
        
def drop_database(name: str):
    if os.path.isfile(f'{os.path.dirname(__file__)}/datas/{name}.ezdb'):
        os.remove(f'{os.path.dirname(__file__)}/datas/{name}.ezdb')
        print(f"Database dropped [ {name} ]")
    else:
        print("Database not found")
        
def export_database(name: str, path_: str):
    if os.path.isfile(f'{os.path.dirname(__file__)}/datas/{name}.ezdb'):
        shutil.copyfile(f'{os.path.dirname(__file__)}/datas/{name}.ezdb', f"{path_}/{name}.ezdb")
        print(f"Database exported [ {name}.ezdb ]")
    else:
        print("Database not found")
        
def import_database(path_: str):
    if os.path.isfile(path_):
        with open(path_, 'r') as rdb:
            try:
                db_ = eval(rdb.read())
            except:
                db_ = rdb.read()
        with open(f'{os.path.dirname(__file__)}/datas/{db_["name"]}.ezdb', 'w') as wdb:
            try:
                json.dump(db_, wdb, indent=4)
                print(f"Database imported [ {db_['name']} ]")
            except:
                print("Import error")
    else:
        print("File or directory not found")
        

class sayuDB:
    
    def __init__(self, database, username:str=None, password:str=None, host:str=None, as_json=None):
        self.database = database
        self.is_remote = False
        self.as_json = as_json
        if username != None and host != None:
            self.is_remote = True
            self.remote = remote.remote(username, password, host)
            self.remote.database_exsistence(database)
        return None
    
    def save_table(self, name: str, content: object):
        if self.is_remote:
            self.remote.commit_database(self.database, content)
        else:
            with open(f'{os.path.dirname(__file__)}/datas/{self.database}.ezdb', 'w') as wdb:
                json.dump(content, wdb, indent=4)
        return

    def save_db(self, content: object):
        with open(f'{os.path.dirname(__file__)}/datas/{self.database}.ezdb', 'w') as wdb:
            json.dump(content, wdb, indent=4)
        return
    
    def openDB(self):
        if self.is_remote:
            db_ = self.remote.pull_database(self.database)
        else:
            with open(f'{os.path.dirname(__file__)}/datas/{self.database}.ezdb', 'r') as rdb:
                db_ = json.loads(rdb.read())
        return db_
    
    def eval_typedata(self, typedata, content):
        try:
            return eval(f'{typedata}({content})')
        except:
            return content
    
    def create_table(self, name: str, col: list):
        """_summary_
        
        Args:
            name (str): the table name
            col (list): [['column_name', 'datatype']]
        
        the datatypes:
        - str   
        - float
        - int   
        - dict
        """
        rdb = self.openDB()
        if name in rdb:
            print("Table already exist")
        else:
            tables_ = {
                "name": name,
                "column": {},
                "datas":[]
            }
            for i in col:
                tables_["column"][i[0]] = i[1]
            rdb[name] = tables_
            self.save_table(name, rdb)
            print("Table created")
            
    def drop_table(self, name: str):
        with open(f'{os.path.dirname(__file__)}/datas/{self.database}.ezdb', 'r') as rdb:
            rdb = eval(rdb.read())
        if name not in rdb:
            print("Table not found")
        else:
            del rdb[name]
            self.save_table(name, rdb)
            print("Table dropped")
            
    def show_table(self, name: str):
        db_ = self.openDB()
        if name not in db_:
            print("Table not found")
        else:
            headeer_ = []
            rows_ = []
            for i in db_[name]['column']:
                headeer_.append(i)
            for i in db_[name]['datas']:
                row_ = []
                for u in i:
                    row_.append(i[u])
                rows_.append(row_)
            print(tabulate(rows_, headers=headeer_))

    def insert_row(self, table:str, col, contents: list):
        """
        _summary_

        Args:
            table (str): the table name
            col (list): column name. EX ['col1', 'col2']
            contents (list): the content for each column EX ['content 1', 'content 2']
            
            _Note : You can also use str for col with comma for the separated EX 'col1,col2'_

        Contents Function:
            today()\t\t: Generate today datetime (only work in str typedata)
            index()\t\t: Indexing the number of row. it can be use as id too (only work in int typedata)
            genID()\t\t: Generate random 5 digits ID
            increase()\t: Increase from the last row value (Only work in int typedata)
        """


        db_ = self.openDB()
        def index():
            return len(db_[table]["datas"]) + 1
        if type(col) == str:
            col = col.split(',')
        column_ = db_[table]["column"]
        for i in col:
            if i not in column_:
                raise Exception(f"Unknown column {i}")
        idx = 0
        data_ = {}
        for i in column_:
            if column_[i] == "str":
                data_[i] = "null"
            elif column_[i] == "int":
                data_[i] = 0
            elif column_[i] == "float":
                data_[i] = 0.0
            elif column_[i] == "dict":
                data_[i] = {}
        for i in col:
            if i not in db_[table]['column']:
                print(f"Column {i} not found")
                sys.exit()
            elif len(col) != len(contents):
                print("The length of column and contents doesn't match")
                sys.exit()
            elif db_[table]['column'][i] == 'str':
                try:
                    if contents[idx] in functions:
                        data_[i] = eval(contents[idx])
                    else:
                        data_[i] = str(contents[idx])
                except:
                    print(f"The content typedata invalid at column {i} content {contents[idx]}")
                    sys.exit()
            elif db_[table]['column'][i] == 'int':
                def increase():
                    try:
                        return int(db_[table]['datas'][-1][i]) + 1
                    except:
                        return 0
                try:
                    if contents[idx] in functions:
                        data_[i] = eval(contents[idx])
                    else:
                        data_[i] = int(contents[idx])
                except:
                    print(f"The content typedata invalid at column {i} content {contents[idx]}")
                    sys.exit()
            elif db_[table]['column'][i] == 'float':
                try:
                    data_[i] = float(contents[idx])
                except:
                    print(f"The content typedata invalid at column {i} content {contents[idx]}")
                    sys.exit()
            elif db_[table]['column'][i] == 'dict':
                try:
                    try:
                        data_[i] = eval(contents[idx])
                    except:
                        data_[i] = eval(str(contents[idx]))
                except:
                    print(f"The content typedata invalid at column {i} content {contents[idx]}")
                    sys.exit()
            idx += 1
        db_[table]['datas'].append(data_)
        self.save_table(table, db_)

    def insert_many(self, table:str, col, contents:list):
        """
        contents = [
        ["a"],
        ["b"]
        ]
        """
        try:
            contents[0][0]
            for row in contents:
                self.insert_row(table, col, row)
        except:
            raise Exception("Invalid contents list")
        
    def select_row(self, table: str, col, where=None, order_by=None, as_json=False, limit=None):
        """_summary_

        Args:
            table (str): The table name
            col (_type_): The column what you want to show. use * for all column
            where (_type_, optional): where the column contain some value. Defaults to None.
            order_by (_type_, optional): short data by column asc or desc. Defaults to None.
            as_json (bool, optional): return as json or table. Defaults to False.
        """
        if self.as_json != None:
            as_json = self.as_json
        db_ = self.openDB()
        datas_ = db_[table]['datas']
        if col == '*':
            datas_ = datas_
        else:
            col = col.split(',')
            idx = 0
            for i in datas_:
                for u in list(i):
                    if u not in col:
                        del i[u]
                idx += 1
        def findWhere(wheree, type_=None):
            temp_ = []
            if type_ == "AND":
                for i in datas_:
                    def isMatch(ii):
                        if i[wheree[ii].split("=")[0]] == self.eval_typedata(db_[table]['column'][wheree[ii].split("=")[0]], wheree[ii].split("=")[1]):
                            return True
                        return False
                    def isNot(ii):
                        if i[wheree[ii].split("!=")[0]] != self.eval_typedata(db_[table]['column'][wheree[ii].split("!=")[0]], wheree[ii].split("!=")[1]):
                            return True
                        return False
                    def isContain(ii):
                        if self.eval_typedata('str', wheree[ii].split(" contain ")[1]) in str(i[wheree[ii].split(" contain ")[0]]):
                            return True
                        return False
                    
                    the_e = []
                    if " contain " in wheree[0]:
                        the_e.append("isContain(0)")
                    elif "!=" in wheree[0]:
                        the_e.append("isNot(0)")
                    else:
                        the_e.append("isMatch(0)")
                    if " contain " in wheree[1]:
                        the_e.append("isContain(1)")
                    elif "!=" in wheree[1]:
                        the_e.append("isNot(1)")
                    else:
                        the_e.append("isMatch(1)")
                    
                    if eval(the_e[0]) and eval(the_e[1]):
                        temp_.append(i)

            elif type_ == "OR":
                for i in datas_:
                    def isMatch(ii):
                        if i[wheree[ii].split("=")[0]] == self.eval_typedata(db_[table]['column'][wheree[ii].split("=")[0]], wheree[ii].split("=")[1]):
                            return True
                        return False
                    def isNot(ii):
                        if i[wheree[ii].split("!=")[0]] != self.eval_typedata(db_[table]['column'][wheree[ii].split("!=")[0]], wheree[ii].split("!=")[1]):
                            return True
                        return False
                    def isContain(ii):
                        if self.eval_typedata('str', wheree[ii].split(" contain ")[1]) in str(i[wheree[ii].split(" contain ")[0]]):
                            return True
                        return False
                    
                    the_e = []
                    if " contain " in wheree[0]:
                        the_e.append("isContain(0)")
                    elif "!=" in wheree[0]:
                        the_e.append("isNot(0)")
                    else:
                        the_e.append("isMatch(0)")
                    if " contain " in wheree[1]:
                        the_e.append("isContain(1)")
                    elif "!=" in wheree[1]:
                        the_e.append("isNot(1)")
                    else:
                        the_e.append("isMatch(1)")
                    
                    if eval(the_e[0]) or eval(the_e[1]):
                        temp_.append(i)

            else:
                for i in datas_:
                    def isMatch(ii):
                        if i[wheree[ii].split("=")[0]] == self.eval_typedata(db_[table]['column'][wheree[ii].split("=")[0]], wheree[ii].split("=")[1]):
                            return True
                        return False
                    def isNot(ii):
                        if i[wheree[ii].split("!=")[0]] != self.eval_typedata(db_[table]['column'][wheree[ii].split("!=")[0]], wheree[ii].split("!=")[1]):
                            return True
                        return False
                    def isContain(ii):
                        if self.eval_typedata('str', wheree[ii].split(" contain ")[1]) in str(i[wheree[ii].split(" contain ")[0]]):
                            return True
                        return False
                    
                    the_e = []
                    if " contain " in wheree[0]:
                        the_e.append("isContain(0)")
                    elif "!=" in wheree[0]:
                        the_e.append("isNot(0)")
                    else:
                        the_e.append("isMatch(0)")
                    
                    if eval(the_e[0]):
                        temp_.append(i)
            return temp_
        
        if where != None:
            if " && " in where:
                datas_ = findWhere(where.split(" && "), "AND")
            elif " || " in where:
                datas_ = findWhere(where.split(" || "), "OR")
            else:
                datas_ = findWhere([where])

        if order_by != None:
            key_ = order_by.split("|")[0]
            sort_ = order_by.split("|")[1]
            if sort_ == 'asc':
                datas_ = sorted(datas_, key=itemgetter(key_))
            elif sort_ == 'desc':
                datas_ = sorted(datas_, key=itemgetter(key_), reverse=True)
                    
        #the anu anu
        if limit != None:
            datas_ = datas_[:limit]
        if as_json:
            try:
                return json.loads(datas_)
            except:
                return datas_
        headeer_ = []
        rows_ = []
        try:
            if datas_ != []:
                for i in datas_[0]:
                    headeer_.append(i)
            elif col == '*':
                for i in db_[table]['column']:
                    headeer_.append(i)
            else:
                for i in col:
                    headeer_.append(i)
        except:
            for i in db_[table]['column']:
                headeer_.append(i)
        for i in datas_:
            row_ = []
            for u in i:
                row_.append(i[u])
            rows_.append(row_)
        return f"{tabulate(rows_, headers=headeer_)}\n\n{len(rows_)} Rows"
    
    def update_row(self, table: str, set_: str, where: str):
        db_ = self.openDB()
        if table not in db_:
            sys.exit("Table not found")
        if ' contain ' in where:
            col_ = where.split(" contain ")[0]
            val_ = where.split(" contain ")[1]
        else:
            col_ = where.split("=")[0]
            val_ = where.split("=")[1]
        set_col = set_.split("=")[0]
        set_val = set_.split("=")[1]
        if col_ not in db_[table]['column']:
            sys.exit("Column not found")        
        if set_col not in db_[table]['column']:
            sys.exit("Column not found")        
        for i in db_[table]['datas']:
            if 'contain' in where:
                if str(val_) in str(i[col_]):
                    i[set_col] = set_val
            else:
                if str(i[col_]) == val_:
                    i[set_col] = set_val
        self.save_table(table, db_)
        return "Column updated"
    
    def update_row_json(self, table:str, set_:object, where:str):
        """
        set_ = {
        "col1":"data1",
        "col2":"data2"
        }
        """
        for i in set_:
            self.update_row(table, f"{i}={set_[i]}", where)
        return "Column updated"
    
    def delete_row(self, table: str, where: str):
        db_ = self.openDB()
        temp_ = []
        if table not in db_:
            sys.exit("Table not found")
        if '=' in where:
            col_ = where.split('=')[0]
            val_ = where.split('=')[1]
            for i in db_[table]['datas']:
                if str(i[col_]) != str(val_):
                    temp_.append(i)
        elif ' contain ' in where:
            col_ = where.split(' contain ')[0]
            val_ = where.split(' contain ')[1]
            for i in db_[table]['datas']:
                if str(val_) not in str(i[col_]):
                    temp_.append(i)
        elif 'row between ' in where:
            temp_ = []
            to_del_ = []
            pp_ = where.replace("row between ","").split("-")
            if int(pp_[0]) > len(db_[table]["datas"]) or int(pp_[1]) > len(db_[table]["datas"]):
                raise Exception("Row number out of range")
            if int(pp_[0]) > int(pp_[1]):
                raise Exception("The number between x-y. the x can not bigger or same with the y")
            for i in range(int(pp_[0])-1, int(pp_[1])-1):
                to_del_.append(db_[table]["datas"][i])
            for i in db_[table]["datas"]:
                if i not in to_del_:
                    temp_.append(i)
        elif 'row ' in where and 'between' not in where:
            temp_ = []
            to_del_ = []
            pp_ = where.replace("row ","")
            if int(pp_) > len(db_[table]["datas"]):
                raise Exception("Row number out of range")
            to_del_.append(db_[table]["datas"][int(pp_)-1])
            for i in db_[table]["datas"]:
                if i not in to_del_:
                    temp_.append(i)
        db_[table]["datas"] = temp_
        self.save_table(table, db_)

    def alter_table_rename_column(self,table:str, col:str, to_:str):
        db = self.openDB()
        db[table]["column"][to_] = db[table]["column"][col]
        del db[table]["column"][col]
        for i in reversed(db[table]["datas"]):
            data = i
            data[to_] = data[col]
            db[table]["datas"].append(data)
            db[table]["datas"].remove(i)
            del data[col]
        self.save_table(table, db)
        return
                
    def alter_table_add_column(self, table:str, col_name:str, datatypes:str):
        db = self.openDB()
        db[table]['column'][col_name] = datatypes
        for i in db[table]['datas']:
            if datatypes == 'str':
                i[col_name] = "null"
            elif datatypes == 'int':
                i[col_name] = 0
            elif datatypes == 'float':
                i[col_name] = 0.0
            elif datatypes == 'dict':
                i[col_name] = {}
            else:
                sys.exit("Unknown datatypes")
        self.save_table(table, db)
        return
    
    def alter_table_drop_column(self, table:str, col_name:str):
        db = self.openDB()
        if col_name not in db[table]['column']:
            sys.exit("Column not found")
        del db[table]['column'][col_name]
        for i in db[table]['datas']:
            del i[col_name]
        self.save_table(table, db)
        return
    
    def copy_table(self, table:str, to_table:str):
        db = self.openDB()
        if table not in db or to_table not in db:
            sys.exit("Table not found")
        if db[table]['column'] != db[to_table]['column']:
            sys.exit("The table structure must be same")
        db[to_table]['datas'] = db[table]['datas'] + db[to_table]['datas']
        self.save_table(to_table, db)
        return
    
    def clear_table(self, table:str):
        db = self.openDB()
        db[table]['datas'] = []
        self.save_table(table, db)
        return
    
    def count_rows(self, table) -> int:
        db = self.openDB()
        return len(db[table]['datas'])