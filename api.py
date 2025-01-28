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

actions = {}
IsWriteAction = {}
#in theory this shouldnt be a problem as this is not async, and also metthods dont take longer than a few seconds
#there SHOULD be no case of two API calls overwriting each others' data
data = ""
request = ""

def action(name, rw=1):
    def decorator(f):
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
        return actions[action]()
    else:
        return "400 Bad Request; No such action"

@action("login", 0)
def login():
    try:
            username = data["username"]
            password = data["password"]
    except:
            return "400 Bad Request; Not enough data, refer to documentation"
        
    _,_,_,token = handle_users.login({"username":username, "password":password})
    if token == 0:
        CreateLog(text=f"Unsuccesful login attempt by `{username}` with password `{username}` from {request.remote_addr} through the API!", severity=1, category=f"/Users/{username}")
        return "401 Unauthorised; Incorrect Data!"
    else:
        CreateLog(text=f"User `{data["username"]}` has logged in from {request.remote_addr} through the API!", severity=0, category=f"/Users/{username}")
        return token

@action("signout", 0)
def signout():
    try:
            token = data["token"]
    except:
            return "400 Bad Request; Not enough data, refer to documentation"
    handle_users.record_token(token.split("|")[0],token, 1)
    CreateLog(text=f"{token.split("|")[1]} has logged out, through the API!", severity=0, category=f"/Users/{token.split("|")[1]}")
    return "200 OK"