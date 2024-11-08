import csv,json,hashlib,threading,time
users_data = []
tokens_data = []
hash_data = []
user_perm_data = []
site_perm_data = []
site_config_data = {}
roles_data = []
groups_data = []
plugin_configs = {}

checksums = {}

def auto_refresh():
    global site_config_data
    while 1:
        for filename in checksums.keys():
            f = open("./data/" + filename, encoding="UTF-8")
            cur_check = hashlib.md5(f.read().encode()).hexdigest()
            if cur_check != checksums[filename]:
                print("File changed:", filename)
                checksums[filename] = cur_check
                funcs[filename]()
        time.sleep(int(site_config_data["RefreshDataFrequency"]))

def refresh_users_data():
    global users_data
    users_file = open("./data/users.csv", encoding="UTF-8")
    csv_reader = csv.reader(users_file)
    users_data = []
    for row in csv_reader:
        users_data.append(row)
    #returning cursor to the start cause python cant read the file again otherwise
    users_file.seek(0)    
    checksums["users.csv"] = hashlib.md5(users_file.read().encode()).hexdigest()
    users_file.close()


def refresh_tokens_data():
    global tokens_data
    tokens_file = open("./data/tokens.csv", encoding="UTF-8")
    csv_reader = csv.reader(tokens_file)
    tokens_data = []
    for row in csv_reader:
        tokens_data.append(row)
    #returning cursor to the start cause python cant read the file again otherwise
    tokens_file.seek(0)    
    checksums["tokens.csv"] = hashlib.md5(tokens_file.read().encode()).hexdigest()    
    tokens_file.close()


def refresh_hash_data():
    global hash_data
    hash_file = open("./data/pwd_hashes.csv", encoding="UTF-8")
    csv_reader = csv.reader(hash_file)
    hash_data = []
    for row in csv_reader:
        hash_data.append(row)
    #returning cursor to the start cause python cant read the file again otherwise
    hash_file.seek(0)    
    checksums["pwd_hashes.csv"] = hashlib.md5((hash_file.read().encode())).hexdigest()
    hash_file.close()


def refresh_user_perm_data():
    global user_perm_data
    user_perm_file = open("./data/user_perms.csv", encoding="UTF-8")
    csv_reader = csv.reader(user_perm_file)
    user_perm_data = []
    for row in csv_reader:
        user_perm_data.append(row)
    #returning cursor to the start cause python cant read the file again otherwise
    user_perm_file.seek(0)    
    checksums["user_perms.csv"] = hashlib.md5(user_perm_file.read().encode()).hexdigest()    
    user_perm_file.close()


def refresh_site_perms_data():
    global site_perm_data
    site_perm_file = open("./data/site_perms.csv", encoding="UTF-8")
    csv_reader = csv.reader(site_perm_file)
    site_perm_data = []
    for row in csv_reader:
        site_perm_data.append(row)
    #returning cursor to the start cause python cant read the file again otherwise
    site_perm_file.seek(0)
    checksums["site_perms.csv"] = hashlib.md5(site_perm_file.read().encode()).hexdigest()    
    site_perm_file.close()


def refresh_site_config_data():
    global site_config_data
    global plugin_configs
    site_config_file = open("./data/site_configs.json", encoding="UTF-8")
    content = site_config_file.read()
    site_config_data = json.loads(content)
    checksums["site_configs.json"] = hashlib.md5(content.encode()).hexdigest()
    site_config_file.close()
    #adding plugin configs on top of normal configs
    site_config_data = {**site_config_data, **plugin_configs}

def refresh_roles_data():
    global roles_data
    roles_file = open("./data/roles.csv", encoding="UTF-8")
    csv_reader = csv.reader(roles_file)
    roles_data = []
    for row in csv_reader:
        roles_data.append(row)
    #returning cursor to the start cause python cant read the file again otherwise
    roles_file.seek(0)
    checksums["roles.csv"] = hashlib.md5(roles_file.read().encode()).hexdigest()    
    roles_file.close()


def refresh_groups_data():
    global groups_data
    groups_file = open("./data/groups.csv", encoding="UTF-8")
    csv_reader = csv.reader(groups_file)
    groups_data = []
    for row in csv_reader:
        groups_data.append(row)
    #returning cursor to the start cause python cant read the file again otherwise
    groups_file.seek(0)
    checksums["groups.csv"] = hashlib.md5(groups_file.read().encode()).hexdigest()    
    groups_file.close()  



funcs = {
    "users.csv": refresh_users_data,
    "tokens.csv": refresh_tokens_data,
    "pwd_hashes.csv":refresh_hash_data,
    "user_perms.csv":refresh_user_perm_data,
    "site_perms.csv":refresh_site_perms_data,
    "site_configs.json": refresh_site_config_data,
    "roles.csv":refresh_roles_data,
    "groups.csv":refresh_groups_data
}

# This function is for adding configs manually
# this way we can add plugin configs to the array, but we can keep them in seperate files
def add_plugin_config(json):
    global plugin_configs
    #plugins are getting reloaded, clear dict
    if json == "RESET":
        plugin_configs = {}
        return
    plugin_configs = {**plugin_configs, **json}
    refresh_site_config_data()

def init():
    for key in funcs.keys():
        funcs[key]()
    t = threading.Thread(target=auto_refresh)
    t.daemon = True
    t.start()
