import sqlite3

class Database():
    def __init__(self, source, username, password, db_name="Tags", table="default"):
        print(source, username, password, db_name, table)