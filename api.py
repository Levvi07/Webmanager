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
import csv

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
        return actions[action]()
    else:
        return "400 Bad Request; No such action"
    
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

@action("reload_plugins", 0, ["token"])
def reload_plugins():
    reload_plugins_func()
    return "rleoad"