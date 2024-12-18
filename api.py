#basically make things more accessible without using the website
# 1. Expose endpoints
# 2. Take proper input
# 3. Write documentation !!!
# 4. Return standard codes, and data
# 5. serve tokens and all that (use the proper users, so we can just create an "api user" role)
# 6. limit access to API so we dont need to use the site_perms here
# 7. Permission levels: none
#                       Read-only (can ask for data, cant modify it)
#                       Write/Read

# Data must be submitted in the correct form, in json
# correct arguments would be like:
# action -- what it does (login, adduser, etc.) Its gonna be a loooooooooooooong list
# token -- for auth, where its needed
# all other data -- only in the correct function, the api will return an HTTP code for insufficient data when enough data isnt given
from LLogger import *
import handle_users

def handle(request):
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
    # determmine action
    try:
        token = data["token"]
    except KeyError:
        pass
    
    if action == "login":
        try:
            username = data["username"]
            password = data["password"]
        except:
            return "400 Bad Request; Not enough data, refer to documentation"
        
        _,_,_,token = handle_users.login({"username":username, "password":password})
        return token
        

    print(data)
    return data
