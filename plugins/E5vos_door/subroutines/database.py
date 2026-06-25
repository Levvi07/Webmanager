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

    def update_last_used(self, UUID):
        cursor = db.cursor(buffered=True)
        cursor.execute(f"UPDATE `{self.table}` SET last_used_at = CURRENT_TIMESTAMP() WHERE UUID='{UUID}'")
        db.commit()
        cursor.close()

    def Validate(self, UUID):
        global db
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT UUID FROM `{self.db_name}`.`{self.table}` WHERE `UUID` = '{UUID}'")
        ct = cursor.rowcount
        cursor.close()
        if ct == 1:
            self.update_last_used(UUID)
            #door opens
            #validate enabled
            cursor = db.cursor(buffered=True)
            cursor.execute(f"SELECT Enabled FROM `{self.db_name}`.`{self.table}` WHERE `UUID` = '{UUID}'")
            row = cursor.fetchone()
            cursor.close()
            if int(row[0]) == 0:
                cursor = db.cursor(buffered=True)
                cursor.execute(f"INSERT INTO {self.entry_table} (UUID, Succesful) VALUES (%s, %s)", (UUID, 0))
                db.commit()
                cursor.close()
                CreateLog(f"Entry failed with UUID `{UUID}`", 1,"SystemLogs/Plugins/E5vos_door")
                return 0
            
            #validate groups
            cursor = db.cursor(buffered=True)
            cursor.execute(f"SELECT Groups FROM `{self.db_name}`.`{self.table}` WHERE `UUID` = '{UUID}'")
            groups = cursor.fetchone()[0]
            cursor.close()
            groups = groups.split(";")
            allowed = 0
            for g in groups:
                cursor = db.cursor(buffered=True)
                cursor.execute(f"SELECT Enabled FROM `{self.db_name}`.`groups` WHERE `ID` = '{g}'")
                enabled = cursor.fetchone()[0]
                if int(enabled):
                    allowed = 1
                cursor.close()

            if not allowed:
                cursor = db.cursor(buffered=True)
                cursor.execute(f"INSERT INTO {self.entry_table} (UUID, Succesful) VALUES (%s, %s)", (UUID, 0))
                db.commit()
                cursor.close()
                CreateLog(f"Entry failed with UUID `{UUID}`", 1,"SystemLogs/Plugins/E5vos_door")
                return 0
            CreateLog(f"Succesful entry with UUID `{UUID}`", 0,"SystemLogs/Plugins/E5vos_door")
            cursor = db.cursor(buffered=True)
            cursor.execute(f"INSERT INTO {self.entry_table} (UUID, Succesful) VALUES (%s, %s)", (UUID, 1))
            db.commit()
            cursor.close()
            return 1
        elif ct == 0:
            #Door doesn't open, log failed try
            CreateLog(f"Entry failed with UUID `{UUID}`", 1,"SystemLogs/Plugins/E5vos_door")
            cursor = db.cursor(buffered=True)
            cursor.execute(f"INSERT INTO {self.entry_table} (UUID, Succesful) VALUES (%s, %s)", (UUID, 0))
            db.commit()
            cursor.close()
            return 0
        else:
            #weird number, log issue
            CreateLog(f"Multiple rows returned for UUID `{UUID}`!", 2,"SystemLogs/Plugins/E5vos_door")
            return 0


    def Add(self, UUID, name, email, e5kod, comment):
        global db
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT UUID FROM `{self.db_name}`.`{self.table}` WHERE `UUID` = '{UUID}'")
        ct = cursor.rowcount
        cursor.close()
        if ct:
            return "Already exists!"
        
        cursor = db.cursor(buffered=True)

        try:
            default_group = dr.plugin_configs["Default_group"]
        except:
            default_group = "Users"

        cursor.execute(f"INSERT INTO {self.table} (`UUID`, `Name`, `Email`, `E5kod`, `Comment`, `Groups`, `Enabled`) VALUES ('{UUID}','{name}','{email}','{e5kod}','{comment}','{default_group}',1)")
        db.commit()
        cursor.close()

    def get_users(self):
        users = []
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM `{self.db_name}`.`{self.table}`")
        for (UUID, name, email, e5kod, comment, groups, enabled, created, lastused) in cursor:
            users.append([UUID, name, email, e5kod, comment, groups, enabled, created, lastused])
        cursor.close()
        return users
    
    def get_single_user(self, UUID):
        user = None
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM `{self.db_name}`.`{self.table}` WHERE UUID = '{UUID}'")
        for (UUID, name, email, e5kod, comment, groups, enabled, created, lastused) in cursor:
            user = [UUID, name, email, e5kod, comment, groups, enabled, created, lastused]
        cursor.close()
        return user
    
    def get_groups(self):
        groups = []
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM `{self.db_name}`.`groups`")
        for (ID, name, enabled) in cursor:
            groups.append([ID, name, enabled])
        cursor.close()
        return groups
    
    def update_groups(self, UUID, group_data):
            cursor = db.cursor(buffered=True)
            cursor.execute(f"UPDATE {self.table} SET Groups = '{group_data}' WHERE UUID='{UUID}' ")
            db.commit()
            cursor.close()

    def update_tag_data(self, UUID, name, email, e5kod, comment, enabled):
            cursor = db.cursor(buffered=True)
            cursor.execute(f"UPDATE {self.table} SET Name = '{name}', Email = '{email}', E5kod = '{e5kod}', Comment = '{comment}', Enabled = '{enabled}' WHERE UUID='{UUID}' ")
            db.commit()
            cursor.close()

    def delete_tag(self, UUID):
        cursor = db.cursor(buffered=True)
        cursor.execute(f"DELETE FROM `{self.table}` WHERE UUID='{UUID}'")
        db.commit()
        cursor.close()

    def set_group_enabled(self, id, enabled):
        cursor = db.cursor(buffered=True)
        cursor.execute(f"UPDATE `groups` SET Enabled = '{str(enabled)}' WHERE ID='{id}'")
        db.commit()
        cursor.close()

    def update_last_used(self, UUID):
        cursor = db.cursor(buffered=True)
        cursor.execute(f"UPDATE `{self.table}` SET last_used_at = CURRENT_TIMESTAMP() WHERE UUID='{UUID}'")
        db.commit()
        cursor.close()

    def get_entries(self):
        entries = []
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM `{self.db_name}`.`{self.entry_table}`")
        for (ID, UUID, Succesful, entry_time) in cursor:
            entries.append([ID, UUID, Succesful, entry_time])
        cursor.close()
        return entries