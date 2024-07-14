import hashlib, csv
import data_reader as dr
from datetime import datetime,timedelta
dr.init()

def generate_token(userid):
    return 123

def record_token(userid,token):
    new_csv_data = [["ID","token","ValidUntil"]]
    for i in range(len(dr.tokens_data)-1):
        if dr.tokens_data[i+1][0] == userid:
            continue
        new_csv_data.append(dr.tokens_data[i+1])
    new_csv_data.append([userid,token,datetime.today() + timedelta(0,int(dr.site_config_data["TokenExpire"]))])
    f = open("./data/tokens.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_csv_data:
        writer.writerow(row)
    f.close()

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
        return "#000000", "#FF0000", "Username is wrong", 0
    pwd_hash = hashlib.md5(bytes(password, "UTF-8")).hexdigest()
    for i in range(len(dr.hash_data)-1):
        if int(dr.hash_data[i+1][0]) == userid:
            if dr.hash_data[i+1][1] == pwd_hash:
                token = generate_token(userid)
                record_token(userid,token)
                return "#000000", "#62cc31", "Login Succesful", token
            else:
                return "#000000", "#FF0000", "Password is wrong", 0
