import sqlite3
import os

def dict_factory(cursor, row):
    """Convert SQLite row to dictionary"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class sql:

    def __init__(self, database:str, as_json:bool=False, auto_commit:bool=True) -> None:
        self.as_json = as_json
        self.auto_commit = auto_commit
        if as_json:
            self.connection = sqlite3.connect(f'{os.path.dirname(__file__)}/sql/{database}.db')
            self.connection.row_factory = dict_factory
        else:
            self.connection = sqlite3.connect(f'{os.path.dirname(__file__)}/sql/{database}.db')
        # if host == None:
        pass

    def execute(self, query, param=None):
        try:
            if param != None:
                response = self.connection.execute(query, param)
            else:
                response = self.connection.execute(query)
            if self.auto_commit:
                self.connection.commit()
            
            return response
        except Exception as e:
            return e
        
    def insert(self, query, param=None):
        cur = self.connection.cursor()
        if param == None:
            response = cur.execute(query)
        else:
            response = cur.execute(query, param)
        if self.auto_commit:
            self.connection.commit()
        
        return response

    def fetchAll(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
            return data
        except Exception as e:
            return e
    
    def fetchOne(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            
            return data
        except Exception as e:
            return e
        
    def printTable(self, query):
        try:
            connection = self.connection
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            header = [description[0] for description in cursor.description]
            print('|'.join(header))
            separator = '-' * (len(header) * 10)
            print(separator)
            for row in rows:
                print('|'.join(str(value) for value in row))
            connection.close()
        except Exception as e:
            print(e)