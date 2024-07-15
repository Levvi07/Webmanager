import hashlib, csv, os
import data_reader as dr
from datetime import datetime,timedelta
dr.init()

def generate_token(userid, name):
    return str(userid) + "|" + name + "|" + str(os.urandom(15).hex())

def record_token(userid,token, signout=0):
    new_csv_data = [["ID","token","ValidUntil"]]
    for i in range(len(dr.tokens_data)-1):
        if dr.tokens_data[i+1][0] == str(userid):
            continue
        new_csv_data.append(dr.tokens_data[i+1])
    if signout:
        expiry = datetime.today() - timedelta(0,int(dr.site_config_data["TokenExpire"]))
    else:
        expiry = datetime.today() + timedelta(0,int(dr.site_config_data["TokenExpire"]))        
    new_csv_data.append([userid,token,expiry])
    f = open("./data/tokens.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_csv_data:
        writer.writerow(row)
    f.close()

def validate_token(token):
    #returns 1 or 0 depending on whether the token is valid or not
    expiry = ""
    for i in range(len(dr.tokens_data)-1):
        if dr.tokens_data[i+1][1] == token:
            expiry = dr.tokens_data[i+1][2]
    print(expiry)
    expiry_split = expiry.split(" ")
    date = expiry_split[0].split("-")
    time = expiry_split[1].split(":")
    expiry_datetime_obj = datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(time[2].split(".")[0]))
    if datetime.today() > expiry_datetime_obj:
        return 0
    else:
        return 1
    
def check_site_perm(site, token):
    #return 200 if user has access or 401 if user doesnt
    #perm levels
    # -1 = no one may access
    # 0 = only accessible by certain users and groups
    # 1+ = anyone with this perm level or one above it may access
    # not in the list = accessible to anyone

    # pair endpoints with line_numbers
    perm_indexes = {}
    for i in range(len(dr.site_perm_data)-1):
        key = dr.site_perm_data[i+1][0]
        if key[0] != "/":
            key = "/" + key
        perm_indexes[key] = i+1
    if site[0] != "/":
        site = "/" + site    

    isPresent = 0
    if site in perm_indexes.keys():
        isPresent = 1    
    for filter in perm_indexes.keys():
        if "*" in filter:
            if filter.replace("*", "") in site:
                isPresent = 1
                site = filter
    if not isPresent:
        return "200"
    if dr.site_perm_data[perm_indexes[site]][1] == "-1":
        return "401"
    
    if token != None:
        valid = validate_token(token)
        if valid:
            #token is valid, proceed with perm check
            userRoles = []
            userGroups = []
            userid = token.split("|")[0]
            for i in range(len(dr.user_perm_data)-1):
                if dr.user_perm_data[i+1][0] == userid:
                    userRoles=dr.user_perm_data[i+1][1].split(";")
                    userGroups=dr.user_perm_data[i+1][2].split(";")

            if dr.site_perm_data[perm_indexes[site]][1] == "0":
                HasAccess = 0
                site_access_roles = dr.site_perm_data[perm_indexes[site]][2].split(";")
                site_access_groups = dr.site_perm_data[perm_indexes[site]][3].split(";")
                for id in userRoles:
                    if id in site_access_roles:
                        HasAccess = 1
                for id in userGroups:
                    if id in site_access_groups:
                        HasAccess = 1     
                if HasAccess:
                    return "200"
                else:
                    return "401"
            if int(dr.site_perm_data[perm_indexes[site]][1]) > 0:
                role_pair = {}
                group_pair = {}
                #pair role ids, with permlevels
                for i in range(len(dr.roles_data)-1):
                    role_pair[dr.roles_data[i+1][0]] = dr.roles_data[i+1][1]
                #pair group ids, with permlevels
                for i in range(len(dr.groups_data)-1):
                    group_pair[dr.groups_data[i+1][0]] = dr.groups_data[i+1][1]
                #get highest perm_level of user
                permLevel = 0
                for id in userRoles:
                    if int(role_pair[id]) > permLevel:
                        permLevel = int(role_pair[id])
                for id in userGroups:
                    if int(group_pair[id]) > permLevel:
                        permLevel = int(group_pair[id])
                    
                required_perm = int(dr.site_perm_data[perm_indexes[site]][4])
                if permLevel >= required_perm:
                    return "200"
                else:
                    return "401"

        else:
            return "401"
    return "401"

def login(form_data:dict) -> str:
    name = form_data["username"].replace(" ", "")
    password = form_data["password"].replace(" ", "")
    DoesExist = 0
    userid = 0
    for i in range(len(dr.users_data)-1):
        if dr.users_data[i+1][1] == name:
            userid = int(dr.users_data[i+1][0])
            DoesExist = 1
    if not DoesExist:
        return "#000000", "#FF0000", "Username or password is wrong", 0
    pwd_hash = hashlib.md5(bytes(password, "UTF-8")).hexdigest()
    for i in range(len(dr.hash_data)-1):
        if int(dr.hash_data[i+1][0]) == userid:
            if dr.hash_data[i+1][1] == pwd_hash:
                token = generate_token(userid, name)
                record_token(userid,token)
                return "#000000", "#62cc31", "Login Succesful", token
            else:
                return "#000000", "#FF0000", "Username or password is wrong", 0