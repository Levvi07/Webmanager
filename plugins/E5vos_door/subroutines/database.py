from mysql import connector
from LLogger import *
class Database():
    db = None
    def __init__(self, source, port, username, password, db_name, table, entry_table):
        self.source = source
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
        self.table = table
        self.entry_table = entry_table
        print(source, port, username, password, db_name, table)
    
    def Connect(self):
        global db
        try:
            db = connector.connect(host=self.source, port=self.port, user=self.username, password=self.password, database=self.db_name)
            CreateLog(f"Connected to database at {self.source}, with user {self.username}", 0, "SystemLogs/Plugins/E5vos_door")
        except Exception as e:
            CreateLog(f"Couldn't connect to database at {self.source}, because of the following error: {e}", 2, "SystemLogs/Plugins/E5vos_door")

    def Close(self):
        global db
        if db != None: 
            db.close() 
            db = None

    def Validate(self, UUID):
        global db
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT UUID FROM `{self.db_name}`.`{self.table}` WHERE `UUID` = '{UUID}'")
        ct = cursor.rowcount
        cursor.close()
        cursor = db.cursor(buffered=True)
        cursor.execute(f"INSERT INTO {self.entry_table} (UUID, Succesful) VALUES (%s, %s)", (UUID, int(ct)))
        db.commit()
        cursor.close()
        if ct == 1:
            #door opens
            CreateLog(f"Succesful entry with UUID `{UUID}`", 0,"SystemLogs/Plugins/E5vos_door")
            return 1
        elif ct == 0:
            #Door doesn't open, log failed try
            CreateLog(f"Entry failed with UUID `{UUID}`", 1,"SystemLogs/Plugins/E5vos_door")
            return 0
        else:
            #weird number, log issue
            CreateLog(f"Multiple rows returned for UUID `{UUID}`!!!!!", 2,"SystemLogs/Plugins/E5vos_door")
            pass


    def Add(self, UUID, name, email, e5kod, comment):
        global db
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT UUID FROM `{self.db_name}`.`{self.table}` WHERE `UUID` = '{UUID}'")
        ct = cursor.rowcount
        cursor.close()
        if ct:
            return "Already exists!"
        
        cursor = db.cursor(buffered=True)
        print(f"INSERT INTO {self.table} (`UUID`, `Name`, `Email`, `E5kod`, `Comment`) VALUES ('{UUID}','{name}','{email}','{e5kod}','{comment}')")
        cursor.execute(f"INSERT INTO {self.table} (`UUID`, `Name`, `Email`, `E5kod`, `Comment`) VALUES ('{UUID}','{name}','{email}','{e5kod}','{comment}')")
        db.commit()
        cursor.close()