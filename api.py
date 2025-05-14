#basically make things more accessible without using the website
# 1. Expose endpoints
# 2. Take proper input
# 3. Write documentation !!!
# 4. Return standard codes, and data
# 5. serve tokens and all that (use the proper users, so we can just create an "api user" role)
# 6. limit access to API so we dont need to use the site_perms here
# 7. Permission levels: 0 none
#                       1 Read-only (can ask for data, cant modify it)
#                       2 Write/Read

# Data must be submitted in the correct form, in json
# correct arguments would be like:
# action -- what it does (login, adduser, etc.) Its gonna be a loooooooooooooong list
# token -- for auth, where its needed
# all other data -- only in the correct function, the api will return an HTTP code for insufficient data when enough data isnt given
from LLogger import *
import handle_users
import csv, json
from datetime import datetime, timedelta

#passed by main.py, used for reloading plugins
reload_plugins_func = ""

actions = {}
IsWriteAction = {}
#in theory this shouldnt be a problem as this is not async, and also metthods dont take longer than a few seconds
#there SHOULD be no case of two API calls overwriting each others' data
data = ""
request = ""
required_keys_list = {}
def action(name, rw=1, required_keys=[]):
    def decorator(f):
        required_keys_list[name] = required_keys
        actions[name] = f
        IsWriteAction[name] = rw
    return decorator

def handle(req):
    global data
    global request
    request = req
    #try to get json data
    try:
        data = request.json
    except:
        # bad request
        return "400 Bad Request; data must be supplied in json format"
    
    keys = data.keys()

    #check if action is supplied
    if "action" not in keys:
        return "400 Bad Request; action must be set"
    
    action = data["action"]

    if "token" not in keys and action != "login":
        return "400 Bad Request; token must be set"
    
    if action in actions:
        for rk in required_keys_list[action]:
            try:
                data[rk]
            except:
                return "400 Bad Request; Not enough data, refer to documentation"
        #we'll only need to return at the end, but we need to check for existence of action
        pass
    else:
        return "400 Bad Request; No such action"
    
    #verify token
    if action != "login":
        token = data["token"]
        id = token.split("|")[0]
        token_data = dr.tokens_data
        row_id = -1
        for i in range(len(token_data)-1):
            if str(token_data[i+1][0]) == str(id):
                row_id = i+1
        if row_id == -1:
            return "401 Unauthorized; Token doesn't exist!"
        if token_data[row_id][1] != token:
            return "401 Unauthorized; Token doesn't exist!"
        if datetime.strptime(token_data[row_id][2].split(".")[0], "%Y-%m-%d %H:%M:%S") - datetime.today() < timedelta(seconds=0):
            return "401 Unauthorized; Token expired!"

        #verify r/w perms
        rw_level = dr.user_perm_data[int(id)][3]
        needed_level = IsWriteAction[action]
        try:
            int(rw_level)
        except:
            #not a number
            return "500 Server Error; R/w permission level is not a number"
        if int(rw_level) >= int(needed_level):
            pass
        else:
            return "401 Unauthorized; Insufficient permissions"
    
    #return action at the end
    return actions[action]()
@action("login", 0, ["username", "password"])
def login():
    username = data["username"]
    password = data["password"]
    _,_,_,token = handle_users.login({"username":username, "password":password})
    if token == 0:
        MakeLog = 1
        if dr.site_config_data["NonExistentUserLogs"] == "0":
            names = []
            for i in range(len(dr.users_data)-1):
                names.append(dr.users_data[i+1][1])
            if username not in names:
                MakeLog = 0
        if MakeLog:
            CreateLog(text=f"Unsuccesful login attempt by `{username}` with password `{username}` from {request.remote_addr} through the API!", severity=1, category=f"/Users/{username}")
            new_ad_data = dr.auto_disable_data
            #increase the number of wrong attempts
            if username in new_ad_data.keys():
                new_ad_data[username] = str(int(new_ad_data[username]) + 1)
            else:
                new_ad_data[username] = "1"

            jsonobj = "{\n"
            clen = len(new_ad_data)
            keys = list(new_ad_data)
            for i in range(clen):
                jsonobj += f"\"{keys[i]}\":\"{new_ad_data[keys[i]]}\""
                if i != clen - 1:
                    jsonobj += ",\n"
                else:
                    jsonobj += "\n}"    
            f = open("./data/auto_disable.json", "w")
            f.write(jsonobj)
            f.close()

            try:
                attempt_limit = int(dr.site_config_data["AutoDisable"])
            except:
                attempt_limit = 0
                CreateLog("AutoDisable must be a number", 2, "SystemLogs/Configs")
            if int(new_ad_data[username]) >= attempt_limit:
                CreateLog(f"User `{username}` got disabled by Auto Disable system", 1, f"Users/{username}")
                CreateLog(f"User `{username}` got disabled by Auto Disable system", 1, f"SystemLogs/AutoDisable")
                #disabling user
                role_id = 0
                for i in range(len(dr.roles_data)-1):
                    if dr.roles_data[i+1][2] == "Disabled":
                        role_id=i+1

                user_id = 0
                for i in range(len(dr.users_data)-1):
                    if dr.users_data[i+1][1] == username:
                        user_id = i+1

                new_user_perms = dr.user_perm_data
                if role_id not in new_user_perms[user_id][1].split(";"):
                    new_user_perms[user_id][1] = new_user_perms[user_id][1] + f";{str(role_id)}"

                f = open("./data/user_perms.csv", "w", encoding="UTF-8", newline='')
                writer = csv.writer(f)
                for row in new_user_perms:
                    writer.writerow(row)
                f.close()
        return "401 Unauthorised; Incorrect Data!"
    else:
        CreateLog(text=f"User `{data['username']}` has logged in from {request.remote_addr} through the API!", severity=0, category=f"/Users/{username}")
        #reset unsuccesful login attempts if needed
        new_ad_data = dr.auto_disable_data
        #increase the number of wrong attempts
        new_ad_data[username] = "0"

        jsonobj = "{\n"
        clen = len(new_ad_data)
        keys = list(new_ad_data)
        for i in range(clen):
            jsonobj += f"\"{keys[i]}\":\"{new_ad_data[keys[i]]}\""
            if i != clen - 1:
                jsonobj += ",\n"
            else:
                jsonobj += "\n}"    
        f = open("./data/auto_disable.json", "w")
        f.write(jsonobj)
        f.close()
        return token

@action("signout", 0, ["token"])
def signout():
    token = data["token"]
    ret = handle_users.record_token(token.split("|")[0], token, 1)
    CreateLog(text=f"{token.split('|')[1]} has logged out, through the API!", severity=0, category=f"/Users/{token.split('|')[1]}")
    return ret

@action("reload_plugins", 1, ["token"])
def reload_plugins():
    reload_plugins_func()
    return "200 OK"

@action("get_user", 0, ["token"])
def get_user():
    #if set to other than None we filter for it
    filtervalue = {"ID":None, "name":None, "email":None, "full_name":None, "groups":None, "roles":None, "description":None, "IsLoggedIn":None, "API_access":None}
    for k in filtervalue.keys():
        if k in data:
            filtervalue[k] = str(data[k])

    #Get all the required data sets
    users = dr.users_data
    user_perms = dr.user_perm_data
    #combine data sets
    users_combined = []
    for i in range(len(users)-1):
        #determine whether user is logged in or not
        id = i+1
        token_data = dr.tokens_data
        row_id = -1
        isloggedin = -1
        for j in range(len(token_data)-1):
            if str(token_data[j+1][0]) == str(id):
                row_id = j+1
        if row_id == -1:
            isloggedin = "0"
        else:
            if datetime.strptime(token_data[row_id][2].split(".")[0], "%Y-%m-%d %H:%M:%S") - datetime.today() < timedelta(seconds=0):
                isloggedin = "0"
            if datetime.strptime(token_data[row_id][2].split(".")[0], "%Y-%m-%d %H:%M:%S") - datetime.today() > timedelta(seconds=0):
                isloggedin = "1"
            
        users_combined.append({
            "ID":i+1, 
            "name":users[i+1][1], 
            "email":users[i+1][2], 
            "full_name":users[i+1][3], 
            "groups":user_perms[i+1][2], 
            "roles":user_perms[i+1][1], 
            "description":users[i+1][4], 
            "IsLoggedIn":isloggedin, 
            "API_access":user_perms[i+1][3]
            })
    ret_value = []
    #filter rows
    for user in users_combined:
        for k in filtervalue:
            to_return = 1
            if filtervalue[k] != None:
                if k == "groups" or k == "roles":
                    # ";" + user[k] + ";" is necessary because, we need to check that there's a ; before and after the number
                    # to ensure we only search for that exact number. ==> 33 and 3 would both trigger for a 3 BUT
                    # in "12;5;65;4" we can search for ";5;" so only the correct one triggers.
                    # adding the extra ; at the beginning and end of user[k] is necessary so those trigger correctly too
                    if ";" + filtervalue[k] + ";" not in ";" + user[k] + ";":
                        to_return = 0
                        break
                else:
                    if str(user[k]) != str(filtervalue[k]):
                        to_return = 0
                        break
        if to_return:
            ret_value.append(user)
        
    #return
    return ret_value

@action("add_user", 1, ["token", "name", "email", "full_name", "password"])
def add_user():
    name = data["name"]
    email = data["email"]
    full_name = data["full_name"]
    password = data["password"]

    try:
        description = data["description"]
    except:
        description = ""
    
    try:
        API_access = data["API_access"]
    except:
        API_access = -1
    
    try:
        groups = data["groups"]
        if type(groups) != list:
            return "400 Bad Request; Groups MUST be an array"
    except:
        groups = []

    try:
        roles = data["roles"]
        if type(roles) != list:
            return "400 Bad Request; Groups MUST be an array"
    except:
        roles = []

    roles_data = dr.roles_data[1:]
    groups_data = dr.groups_data[1:]
    for i in range(len(roles)):
        #checking if role exists
        if roles[i] > len(roles_data):
            return "400 Bad Request; non-existent role:" + str(roles[i])
        roles[i] = str(roles[i])
    for i in range(len(groups)):
        #checking if group exists
        if groups[i] > len(groups_data):
            return "400 Bad Request; non-existent group:" + str(groups[i])
        groups[i] = str(groups[i])

    roles = ";".join(roles) + ";"
    groups = ";".join(groups) + ";"
    #passing it in the same structure a form is, because thats how I made the function
    # We also need to use the same names as the page. Also password1 and 2 are just the same here
    form = {"fullname":full_name, "username":name, "password1":password, "password2":password, "email":email, "description":description, "roles_post":roles, "groups_post":groups, "API_select":str(API_access)}
    _,_,msg = handle_users.AddUser(form)
    if msg != "User added succesfully":
        return "400 Bad Request;" + msg
    else:
        return "200 OK;" + msg
    
@action("remove_user", 1, ["token", "ID"])
def remove_user():
    ID = data["ID"]
    #check that user exists
    if int(ID) > len(dr.users_data[1:]):
        return "400 Bad Request; Non-existent user"
    handle_users.remove_user(int(ID))
    return "200 OK; User removed"

@action("modify_user", 1, ["token", "ID"])
def modify_user():
    ID = data["ID"]
    #check that user exists
    if int(ID) > len(dr.users_data[1:]):
        return "400 Bad Request; Non-existent user"
    
    #filtering set values
    filtervalue = {"name":None, "email":None, "full_name":None, "description":None, "groups":None, "roles":None, "API_access":None}
    

    for v in filtervalue:
        if v in data:
            filtervalue[v] = data[v]

    if filtervalue["groups"] != None:
        if type(filtervalue["groups"]) != list:
            return "400 Bad Request; Groups MUST be an array"
        
        groups_data = dr.groups_data[1:]
        for i in range(len(filtervalue["groups"])):
            #checking if group exists
            if filtervalue["groups"][i] > len(groups_data):
                return "400 Bad Request; non-existent group:" + str(filtervalue["groups"][i])
            filtervalue["groups"][i] = str(filtervalue["groups"][i])
        
        filtervalue["groups"] = ";".join(filtervalue["groups"])
    
    if filtervalue["roles"] != None:
        if type(filtervalue["roles"]) != list:
            return "400 Bad Request; Roles MUST be an array"
        
        roles_data = dr.roles_data[1:]
        for i in range(len(filtervalue["roles"])):
            #checking if role exists
            if filtervalue["roles"][i] > len(roles_data):
                return "400 Bad Request; non-existent role:" + str(filtervalue["roles"][i])
            filtervalue["roles"][i] = str(filtervalue["roles"][i])

        filtervalue["roles"] = ";".join(filtervalue["roles"])
    
    #make sure name isnt used already
    if filtervalue["name"] != None:
        usernames = []
        for i in range(len(dr.users_data)-1):
            usernames.append(dr.users_data[i+1][1])
        
        if filtervalue["name"] in usernames:
            return "409 Conflict; Username already in use"

    user_ids = {"name":1, "email":2, "full_name":3, "description":4}
    perm_ids = {"groups":2, "roles":1, "API_access":3}

    new_users_data = dr.users_data
    new_users_perm_data = dr.user_perm_data
    
    #actually saving those values
    #first users.csv
    for k in user_ids:
        if filtervalue[k] != None:
            new_users_data[int(ID)][user_ids[k]] = filtervalue[k]
    
    #then user_perms.csv
    for k in perm_ids:
        if filtervalue[k] != None:
            new_users_perm_data[int(ID)][perm_ids[k]] = filtervalue[k]

    #writing data

    f = open("./data/users.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_users_data:
        writer.writerow(row)
    f.close()  

    f = open("./data/user_perms.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_users_perm_data:
        writer.writerow(row)
    f.close()

    return "200 OK; User modified"

@action("get_role", 0, ["token"])
def get_role_data():
    #if set to other than None we filter for it
    filtervalue = {"ID":None, "name":None, "perm_level":None, "description":None}
    for k in filtervalue.keys():
        if k in data:
            filtervalue[k] = str(data[k])

    #Get all the required data sets
    roles = dr.roles_data
    ret_value = []
    
    #sanitising perm_level
    if filtervalue["perm_level"] != None:
                perm_level = filtervalue["perm_level"]
                pm = ""
                if perm_level[-1] == "-" or perm_level[-1] == "+":
                    pm = perm_level[-1]
                    perm_level = perm_level[:-1]
                
                #make sure its ok
                try:
                    int(perm_level)
                except:
                    return "400 Bad Request; perm_level must be a number, or a number followed either by a + or a - sign (Refer to documentation)"

    #filter rows

    for i in range(len(roles)-1):
            #testing for definite values
            if filtervalue["description"] != None:
                if roles[i+1][3] != filtervalue["description"]:
                    continue

            if filtervalue["name"] != None:
                if roles[i+1][2] != filtervalue["name"]:
                    continue
            
            if filtervalue["ID"] != None:
                if str(roles[i+1][0]) != str(filtervalue["ID"]):
                    continue
                
            # here we need some weird negation cause of the way filtering works
            # pm = ""  ==>   int(roles[i+1][1]) != int(perm_level)
            # pm = "+"  ==>   int(roles[i+1][1]) < int(perm_level)
            # pm = "-"  ==>   int(roles[i+1][1]) > int(perm_level) 
            if filtervalue["perm_level"] != None:
                if pm == "":
                    if int(roles[i+1][1]) != int(perm_level):
                        continue
                elif pm == "-":
                    if int(roles[i+1][1]) > int(perm_level):
                        continue
                elif pm == "+":
                    if int(roles[i+1][1]) < int(perm_level):
                        continue
        
            return_json = {
                "ID":str(roles[i+1][0]),
                "perm_level":str(roles[i+1][1]),
                "name":roles[i+1][2],
                "description":roles[i+1][3]
            }
            ret_value.append(return_json)

    #return
    return ret_value


@action("add_role", 1, ["token", "name"])
def add_role():
    #check that name doesnt exist already
    name = data["name"]
    for i in range(len(dr.roles_data)-1):
        if dr.roles_data[i+1][2].lower() == name.lower():
            return "400 Bad Request; Role already exists"
        
    if "perm_level" in data:
        perm_level = data["perm_level"]
        try:
            perm_level = int(perm_level)
        except:
            return "400 Bad Request; perm_level must be an integer"
    else: perm_level = -1

    if "description" in data:
        description = data["description"]
    else: description = ""

    new_roles_data = dr.roles_data
    new_roles_data.append([int(new_roles_data[-1][0])+1, perm_level, name, description])

    #writing data
    f = open("./data/roles.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_roles_data:
        writer.writerow(row)
    f.close()

    return "200 OK"


@action("remove_role", 1, ["token", "ID"])
def remove_role():
    ID = data["ID"]
    try:
        ID = int(ID)
    except:
        return "400 Bad Request; ID must be an integer"
    
    new_roles_data = dr.roles_data
    if ID > len(new_roles_data)-1:
        return "400 Bad Request; Role does not exist"
    new_roles_data.pop(ID)

    #reorganising IDs
    for i in range(len(new_roles_data)-ID):
        new_roles_data[i+ID][0] = ID+i
        

    #writing data
    f = open("./data/roles.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_roles_data:
        writer.writerow(row)
    f.close()

    return "200 OK"

@action("modify_role", 1, ["token", "ID"])
def modify_role():
    ID = data["ID"]
    try:
        ID = int(ID)
    except:
        return "400 Bad Request; ID must be an integer"
    
    new_roles_data = dr.roles_data
    if ID > len(new_roles_data)-1:
        return "400 Bad Request; Role does not exist"
    
    if "name" in data:
        new_roles_data[ID][2] = data["name"]
    
    if "description" in data:
        new_roles_data[ID][3] = data["description"]

    if "perm_level" in data:
        try:
            int(data["perm_level"])
        except:
            return "400 Bad Request; perm_level must be an integer"
        
        new_roles_data[ID][1] = int(data["perm_level"])

    #writing data
    f = open("./data/roles.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_roles_data:
        writer.writerow(row)
    f.close()

    return "200 OK"


@action("get_group", 0, ["token"])
def get_group_data():
    #if set to other than None we filter for it
    filtervalue = {"ID":None, "name":None, "perm_level":None, "description":None}
    for k in filtervalue.keys():
        if k in data:
            filtervalue[k] = str(data[k])

    #Get all the required data sets
    groups = dr.groups_data
    ret_value = []
    
    #sanitising perm_level
    if filtervalue["perm_level"] != None:
                perm_level = filtervalue["perm_level"]
                pm = ""
                if perm_level[-1] == "-" or perm_level[-1] == "+":
                    pm = perm_level[-1]
                    perm_level = perm_level[:-1]
                
                #make sure its ok
                try:
                    int(perm_level)
                except:
                    return "400 Bad Request; perm_level must be a number, or a number followed either by a + or a - sign (Refer to documentation)"

    #filter rows
    for i in range(len(groups)-1):
            #testing for definite values
            if filtervalue["description"] != None:
                if groups[i+1][3] != filtervalue["description"]:
                    continue

            if filtervalue["name"] != None:
                if groups[i+1][2] != filtervalue["name"]:
                    continue
            
            if filtervalue["ID"] != None:
                if str(groups[i+1][0]) != str(filtervalue["ID"]):
                    continue
                
            # here we need some weird negation cause of the way filtering works
            # pm = ""  ==>   int(roles[i+1][1]) != int(perm_level)
            # pm = "+"  ==>   int(roles[i+1][1]) < int(perm_level)
            # pm = "-"  ==>   int(roles[i+1][1]) > int(perm_level) 
            if filtervalue["perm_level"] != None:
                if pm == "":
                    if int(groups[i+1][1]) != int(perm_level):
                        continue
                elif pm == "-":
                    if int(groups[i+1][1]) > int(perm_level):
                        continue
                elif pm == "+":
                    if int(groups[i+1][1]) < int(perm_level):
                        continue
        
            return_json = {
                "ID":str(groups[i+1][0]),
                "perm_level":str(groups[i+1][1]),
                "name":groups[i+1][2],
                "description":groups[i+1][3]
            }
            ret_value.append(return_json)

    #return
    return ret_value


@action("add_group", 1, ["token", "name"])
def add_group():
    #check that name doesnt exist already
    name = data["name"]
    for i in range(len(dr.groups_data)-1):
        if dr.groups_data[i+1][2].lower() == name.lower():
            return "400 Bad Request; Group already exists"
        
    if "perm_level" in data:
        perm_level = data["perm_level"]
        try:
            perm_level = int(perm_level)
        except:
            return "400 Bad Request; perm_level must be an integer"
    else: perm_level = -1

    if "description" in data:
        description = data["description"]
    else: description = ""

    new_groups_data = dr.groups_data
    new_groups_data.append([int(new_groups_data[-1][0])+1, perm_level, name, description])

    #writing data
    f = open("./data/groups.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_groups_data:
        writer.writerow(row)
    f.close()

    return "200 OK"


@action("remove_group", 1, ["token", "ID"])
def remove_group():
    ID = data["ID"]
    try:
        ID = int(ID)
    except:
        return "400 Bad Request; ID must be an integer"
    
    new_groups_data = dr.groups_data
    if ID > len(new_groups_data)-1:
        return "400 Bad Request; Group does not exist"
    new_groups_data.pop(ID)

    #reorganising IDs
    for i in range(len(new_groups_data)-ID):
        new_groups_data[i+ID][0] = ID+i
        

    #writing data
    f = open("./data/groups.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_groups_data:
        writer.writerow(row)
    f.close()

    return "200 OK"


@action("modify_group", 1, ["token", "ID"])
def modify_group():
    ID = data["ID"]
    try:
        ID = int(ID)
    except:
        return "400 Bad Request; ID must be an integer"
    
    new_groups_data = dr.groups_data
    if ID > len(new_groups_data)-1:
        return "400 Bad Request; Group does not exist"
    
    if "name" in data:
        new_groups_data[ID][2] = data["name"]
    
    if "description" in data:
        new_groups_data[ID][3] = data["description"]

    if "perm_level" in data:
        try:
            int(data["perm_level"])
        except:
            return "400 Bad Request; perm_level must be an integer"
        
        new_groups_data[ID][1] = int(data["perm_level"])

    #writing data
    f = open("./data/groups.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_groups_data:
        writer.writerow(row)
    f.close()
    return "200 OK"


@action("get_access_rule", 0, ["token", "endpoint"])
def get_access_rule():
    r_arr = {}
    for r in dr.site_perm_data:
        if r[0] == data["endpoint"]:
            r_arr = {
                "endpoint":r[0],
                "access_level":r[1],
                "access_roles_id":r[2],
                "access_groups_id":r[3],
                "access_users_id":r[4],
                "perm_level":r[5]
            }

    if r_arr == {}:
        return "400 Bad Request; No such endpoint"
    else:
        return r_arr
    

@action("create_access_rule", 1, ["token", "endpoint", "access_level", "perm_level"])
def create_access_rule():
    r_arr = dr.site_perm_data
    new_rule = []
    # append data one at a time, after validating data
    # endpoint,access_level,access_roles_id,access_groups_id,access_users_id,perm_level
    if data["endpoint"] == "":
        return "400 Bad Request; Endpoint must not be empty!"
    if data["endpoint"][0] != "/":
        return "400 Bad Request; Endpoint must start with /"
    DoesExist = 0
    for i in range(len(dr.site_perm_data)-1):
        if dr.site_perm_data[i+1][0] == data["endpoint"]:
            DoesExist = 1
    if DoesExist:
        return "400 Bad Request; A rule for this endpoint is already in place!" 
    
    new_rule.append(data["endpoint"])

    try:
        data["access_level"] = int(data["access_level"])
        new_rule.append(data["access_level"])
    except:
        return "400 Bad Request; access_level must be an integer"

    if "access_roles_id" in data:
        if type(data["access_roles_id"]) != list:
            return "400 Bad Request; access_roles_id must be a list"
        else:
            for i in range(len(data["access_roles_id"])):
                data["access_roles_id"][i] = str(data["access_roles_id"][i])
            new_rule.append(";".join(data["access_roles_id"]))
    else:
        new_rule.append("")

    if "access_groups_id" in data:
        if type(data["access_groups_id"]) != list:
            return "400 Bad Request; access_groups_id must be a list"
        else:
            for i in range(len(data["access_groups_id"])):
                data["access_groups_id"][i] = str(data["access_groups_id"][i])
            new_rule.append(";".join(data["access_groups_id"]))
    else:
        new_rule.append("")

    if "access_users_id" in data:
        if type(data["access_users_id"]) != list:
            return "400 Bad Request; access_users_id must be a list"
        else:
            for i in range(len(data["access_users_id"])):
                data["access_users_id"][i] = str(data["access_users_id"][i])
            new_rule.append(";".join(data["access_users_id"]))
    else:
        new_rule.append("")

    try:
        data["perm_level"] = int(data["perm_level"])
        new_rule.append(data["perm_level"])
    except:
        return "400 Bad Request; perm_level must be an integer"
    
    r_arr.append(new_rule)
    #writing data
    f = open("./data/site_perms.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in r_arr:
        writer.writerow(row)
    f.close()
    return "200 OK"


@action("remove_access_rule", 1, ["token", "endpoint"])
def remove_access_rule():
    r_arr = []
    for r in dr.site_perm_data:
        if r[0] != data["endpoint"]:
            r_arr.append(r)
    
    if r_arr == dr.site_perm_data:
        return "400 Bad Request; No such endpoint"
    else:
        #writing data
        f = open("./data/site_perms.csv", "w", encoding="UTF-8", newline='')
        writer = csv.writer(f)
        for row in r_arr:
            writer.writerow(row)
        f.close()
        return "200 OK"
    

@action("modify_access_rule", 1, ["token", "endpoint"])
def modify_access_rule():
    r_arr = dr.site_perm_data
    modified_rule = []
    # append data one at a time, after validating data
    # endpoint,access_level,access_roles_id,access_groups_id,access_users_id,perm_level
    DoesExist = 0
    for i in range(len(dr.site_perm_data)-1):
        if dr.site_perm_data[i+1][0] == data["endpoint"]:
            DoesExist = 1
    if not DoesExist:
        return "400 Bad Request; A rule for this endpoint does not exist!" 
    
    for r in r_arr:
        if r[0] == data["endpoint"]:
            modified_rule = r

    if "access_level" in data:
        try:
            data["access_level"] = int(data["access_level"])
            modified_rule[1] = data["access_level"]
        except:
            return "400 Bad Request; access_level must be an integer"

    if "access_roles_id" in data:
        if type(data["access_roles_id"]) != list:
            return "400 Bad Request; access_roles_id must be a list"
        else:
            for i in range(len(data["access_roles_id"])):
                data["access_roles_id"][i] = str(data["access_roles_id"][i])
            modified_rule[2] = ";".join(data["access_roles_id"])

    if "access_groups_id" in data:
        if type(data["access_groups_id"]) != list:
            return "400 Bad Request; access_groups_id must be a list"
        else:
            for i in range(len(data["access_groups_id"])):
                data["access_groups_id"][i] = str(data["access_groups_id"][i])
            modified_rule[3] = ";".join(data["access_groups_id"])

    if "access_users_id" in data:
        if type(data["access_users_id"]) != list:
            return "400 Bad Request; access_users_id must be a list"
        else:
            for i in range(len(data["access_users_id"])):
                data["access_users_id"][i] = str(data["access_users_id"][i])
            modified_rule[4] = ";".join(data["access_users_id"])

    if "perm_level" in data:
        try:
            data["perm_level"] = int(data["perm_level"])
            modified_rule[5] = data["perm_level"]
        except:
            return "400 Bad Request; perm_level must be an integer"
    
    for i in range(len(r_arr)):
        if r_arr[i][0] == data["endpoint"]:
            r_arr[i] = modified_rule

    #writing data
    f = open("./data/site_perms.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in r_arr:
        writer.writerow(row)
    f.close()
    return "200 OK"


@action("get_config", 0, ["token"])
def get_config():
    config_file = open("./data/site_configs.json")
    config_data = config_file.read()
    config_file.close()
    config_data = json.loads(config_data)
    if "config" not in data:
        return config_data
    else:
        r_obj = {}
        if type(data["config"]) != list:
            return "400 Bad Request; config must be a list"
        
        for k in data["config"]:
            try:
                r_obj[k] = config_data[k]
            except:
                return "400 Bad Request; config contains a config name that doesn't exist"
        
        return r_obj


@action("get_active_config", 0, ["token"])
def get_active_config():
    if "config" not in data:
        return dr.site_config_data
    else:
        r_obj = {}
        if type(data["config"]) != list:
            return "400 Bad Request; config must be a list"
        
        for k in data["config"]:
            try:
                r_obj[k] = dr.site_config_data[k]
            except:
                return "400 Bad Request; config contains a config name that doesn't exist"
        
        return r_obj
    


@action("add_config", 1, ["token", "key", "value"])
def add_config():
    k = data["key"]
    v = data["value"]

    if " " in k:
        return "400 Bad Request; Key must not contain spaces!"
    
    config_file = open("./data/site_configs.json")
    config_data = config_file.read()
    config_file.close()
    config_data = json.loads(config_data)

    if k in config_data.keys():
        return "400 Bad Request; Key already exists!"

    config_data[k] = v

    #converting to the correct format with \n -s or the delete wont be happy
    jsonobj = "{\n"
    clen = len(config_data)
    keys = list(config_data)
    for i in range(clen):
        jsonobj += f"\"{keys[i]}\":\"{config_data[keys[i]]}\""
        if i != clen - 1:
            jsonobj += ",\n"
        else:
            jsonobj += "\n}"    
    f = open("./data/site_configs.json", "w")
    f.write(jsonobj)
    f.close()
    return "200 OK"

@action("remove_config", 1, ["token", "key"])
def remove_config():
    config_file = open("./data/site_configs.json")
    config_data = config_file.read()
    config_file.close()
    config_data = json.loads(config_data)

    if data["key"] not in config_data.keys():
        return "400 Bad Request; Key doesn't exist!"
    
    new_config_data = {}
    for k in config_data.keys():
        if k != data["key"]:
            new_config_data[k] = config_data[k]

    #converting to the correct format with \n -s or the delete wont be happy
    jsonobj = "{\n"
    clen = len(new_config_data)
    keys = list(new_config_data)
    for i in range(clen):
        jsonobj += f"\"{keys[i]}\":\"{new_config_data[keys[i]]}\""
        if i != clen - 1:
            jsonobj += ",\n"
        else:
            jsonobj += "\n}"    
    f = open("./data/site_configs.json", "w")
    f.write(jsonobj)
    f.close()
    return "200 OK"

@action("change_config", 1, ["token", "key", "value"])
def change_config():
    config_file = open("./data/site_configs.json")
    config_data = config_file.read()
    config_file.close()
    config_data = json.loads(config_data)
    r_obj = {}
    for k in config_data:
            if k == data["key"]:
                r_obj[data["key"]] = data["value"]
            else:
                r_obj[k] = config_data[k]

    #converting to the correct format with \n -s or the delete wont be happy
    jsonobj = "{\n"
    clen = len(r_obj)
    keys = list(r_obj)
    for i in range(clen):
        jsonobj += f"\"{keys[i]}\":\"{r_obj[keys[i]]}\""
        if i != clen - 1:
            jsonobj += ",\n"
        else:
            jsonobj += "\n}"    
    f = open("./data/site_configs.json", "w")
    f.write(jsonobj)
    f.close()
    return "200 OK"

@action("get_pl_list", 0, ["token"])
def get_pl_list():
    pl_list = os.listdir("./plugins")
    pl_list.remove("__pycache__")
    pl_list.remove("__init__.py")
    
    return pl_list

@action("get_pl", 0, ["token", "name"])
def get_pl():
    r_obj = {}
    pl_list = os.listdir("./plugins")
    pl_list.remove("__pycache__")
    pl_list.remove("__init__.py")
    for n in data["name"]:
        if n not in pl_list:
            r_obj[n] = "Plugin doesn't exist!"
            continue
        else:
            r_obj[n] = {}
        
        #Plugin_data
        cur_data = {}
        try:
            pl_data = open("./plugins/" + n + "/__plugin_init__.py")
            pl_data = pl_data.read().split("PluginData():")[1].split("import os")[0]
            pl_split = pl_data.split("\n")
            print(pl_data.split("\n"))
            name_line = pl_split[1]
            version_line = pl_split[2]
            desc_line = pl_split[3]
            path_line = pl_split[4]
            cur_data["name"] = name_line.split("=", 1)[1].replace("\"", "").strip()
            cur_data["version"] = version_line.split("=", 1)[1].replace("\"", "").strip()
            cur_data["description"] = desc_line.split("=", 1)[1].replace("\"", "").strip()
            cur_data["path"] = path_line.split("=", 1)[1].replace("\"", "").strip()
            #cur_data["path"] = path_line.split("path", 1)[1].replace("=", "").replace("\"", "").strip().split("\n")[0]
        except Exception as e:
            print(e)
            cur_data = "No data, missing __plugin_init__.py"
        finally:
            r_obj[n]["plugin_data"] = cur_data

        #enabled status
        cur_data = {}
        try:
            for i in range(len(dr.plugin_enabled_data)-1):
                if dr.plugin_enabled_data[i+1][0] == n:
                    cur_data = dr.plugin_enabled_data[i+1][1]
        except Exception as e:
            print(e)
            cur_data = "Enabled status is not set"
        finally:
            r_obj[n]["enabled"] = cur_data


        #plugin configs
        cur_data = {}
        try:
            pl_data = open("./plugins/" + n + "/__plugin_configs__.json")
            cur_data = json.loads(pl_data.read())
            pl_data.close()
        except Exception as e:
            print(e)
            cur_data = "No Config file present for this plugin"
        finally:
            r_obj[n]["plugin_config"] = cur_data


    return r_obj



@action("change_pl_status", 1, ["token", "name"])
def change_pl_status():
    if type(data["name"]) != str:
        return "400 Bad Request; name must be a string"
    en_data = dr.plugin_enabled_data
    for i in range(len(en_data)-1):
        if en_data[i+1][0] == data["name"]:
            if "enabled" in data:
                if str(data["enabled"]) != "0" and str(data["enabled"]) != "1":
                    return "400 Bad Request; enabled must be either 0, 1, or left empty"
                en_data[i+1][1] = str(data["enabled"])
            else:
                en_data[i+1][1] = str(int(not int(en_data[i+1][1])))
            break
    
    f = open("./data/plugin_enabled.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in en_data:
        writer.writerow(row)
    f.close()

    return "200 OK"


@action("add_pl_config", 1, ["token", "name", "key", "value"])
def add_pl_config():
    k = data["key"]
    v = data["value"]
    name = data["name"]

    if type(name) != str:
        return "400 Bad Request; name must be a string"

    if name not in os.listdir("./plugins"):
        return "400 Bad Request; Plugin doesn't exist"
    if " " in k:
        return "400 Bad Request; Key must not contain spaces!"
    
    try:
        config_file = open(f"./plugins/{name}/__plugin_configs__.json")
    except:
        config_file = open(f"./plugins/{name}/__plugin_configs__.json", "x")
        config_file.write("{}")
        config_file.close()
        config_file = open(f"./plugins/{name}/__plugin_configs__.json")
    config_data = config_file.read()
    config_file.close()
    config_data = json.loads(config_data)

    if k in config_data.keys():
        return "400 Bad Request; Key already exists!"

    config_data[k] = v

    #converting to the correct format with \n -s or the delete wont be happy
    jsonobj = "{\n"
    clen = len(config_data)
    keys = list(config_data)
    for i in range(clen):
        jsonobj += f"\"{keys[i]}\":\"{config_data[keys[i]]}\""
        if i != clen - 1:
            jsonobj += ",\n"
        else:
            jsonobj += "\n}"    
    f = open(f"./plugins/{name}/__plugin_configs__.json", "w")
    f.write(jsonobj)
    f.close()
    return "200 OK"


@action("remove_pl_config", 1, ["token", "key", "name"])
def remove_pl_config():
    name = data["name"]
    if type(name) != str:
        return "400 Bad Request; name must be a string"

    if name not in os.listdir("./plugins"):
        return "400 Bad Request; Plugin doesn't exist"
    config_file = open(f"./plugins/{name}/__plugin_configs__.json")
    config_data = config_file.read()
    config_file.close()
    config_data = json.loads(config_data)

    if data["key"] not in config_data.keys():
        return "400 Bad Request; Key doesn't exist!"
    
    new_config_data = {}
    for k in config_data.keys():
        if k != data["key"]:
            new_config_data[k] = config_data[k]

    #converting to the correct format with \n -s or the delete wont be happy
    jsonobj = "{\n"
    clen = len(new_config_data)
    keys = list(new_config_data)
    for i in range(clen):
        jsonobj += f"\"{keys[i]}\":\"{new_config_data[keys[i]]}\""
        if i != clen - 1:
            jsonobj += ",\n"
        else:
            jsonobj += "\n}"    
    f = open(f"./plugins/{name}/__plugin_configs__.json", "w")
    f.write(jsonobj)
    f.close()
    return "200 OK"

@action("change_pl_config", 1, ["token", "key", "value", "name"])
def change_pl_config():
    name = data["name"]
    if type(name) != str:
        return "400 Bad Request; name must be a string"

    if name not in os.listdir("./plugins"):
        return "400 Bad Request; Plugin doesn't exist"
    config_file = open(f"./plugins/{name}/__plugin_configs__.json")
    config_data = config_file.read()
    config_file.close()
    config_data = json.loads(config_data)
    r_obj = {}
    for k in config_data:
            if k == data["key"]:
                r_obj[data["key"]] = data["value"]
            else:
                r_obj[k] = config_data[k]

    #converting to the correct format with \n -s or the delete wont be happy
    jsonobj = "{\n"
    clen = len(r_obj)
    keys = list(r_obj)
    for i in range(clen):
        jsonobj += f"\"{keys[i]}\":\"{r_obj[keys[i]]}\""
        if i != clen - 1:
            jsonobj += ",\n"
        else:
            jsonobj += "\n}"    
    f = open(f"./plugins/{name}/__plugin_configs__.json", "w")
    f.write(jsonobj)
    f.close()
    return "200 OK"