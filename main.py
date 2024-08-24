from flask import Flask
import os
from flask import send_from_directory, request, make_response
import handle_users, csv, hashlib
import data_reader as dr
dr.init()
def create_app():
    app = Flask(__name__)
    return app

def serve_html_website(route):
    if not os.path.exists("./templates/" + route):
        return "", {"Refresh": "0; url=/404.html"}
    if route[-1] != "/" and os.path.isdir("./templates/" + route):
        return "", {"Refresh": "0; url=/404.html"}
    f = open("./templates/" + route)
    return f.read()

app = create_app()

#handle favicon
@app.route('/favicon.ico')
def favicon():
    perm_code = handle_users.check_site_perm('/favicon.ico', request.cookies.get("token"))
    if perm_code == "200":
        return send_from_directory(os.path.join(app.root_path, 'static'),
                            'favicon.ico', mimetype='image/vnd.microsoft.icon')
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"}

#handle index.html
@app.route("/")
def index():
    perm_code = handle_users.check_site_perm('/index.html', request.cookies.get("token"))
    if perm_code == "200":
        return serve_html_website("index.html")    
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"}

#handle signout
@app.route("/signout.html")
def signout():
    perm_code = handle_users.check_site_perm('/signout.html', request.cookies.get("token"))
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"}
    
    token = request.cookies.get("token")
    if token == None:
        return "Token is not set, you have to log in first! Redirecting...", {"Refresh": "2; url=./login.html"}
    handle_users.record_token(token.split("|")[0],token, 1)
    resp = make_response("Signed out successfully! Redirecting...")
    resp.set_cookie("token", "", max_age=0)
    return resp, {"Refresh": "2; url=./login.html"}
#handle css
@app.route("/css/<path:p>")
def css(p):
    perm_code = handle_users.check_site_perm("/css/"+p, request.cookies.get("token"))
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"}
    
    if not os.path.exists("./css/"+p):
        return "No such file"
    f = open("./css/"+p)
    return f.read()

#handle js
@app.route("/js/<path:p>")
def js(p):
    perm_code = handle_users.check_site_perm("/js/" + p, request.cookies.get("token"))
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"}
    
    if not os.path.exists("./js/"+p):
        return "alert('Missing JS file:" + p + "')"
    f = open("./js/"+p)
    perm_code = handle_users.check_site_perm("/js/" + p, request.cookies.get("token"))
    if perm_code == "200":
        return f.read()
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"}

#handle login_post
@app.route("/login.html", methods=['POST'])
def handle_login():
    perm_code = handle_users.check_site_perm("/login.html", request.cookies.get("token"))
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"}
    
    CookieToken = request.cookies.get("token")
    font_color, bg_color, response, token = handle_users.login(request.form)
    resp = make_response(serve_html_website("login.html").replace('<div id="response">', '<div id="response" style="background-color:' + bg_color+ ';color:' + font_color+ '">' + response))
    if token != 0:
        #If already signed in, sign that profile out before changing
        if CookieToken != None:
            if CookieToken.split("|")[0] != token.split("|")[0]:
                dr.refresh_tokens_data()
                handle_users.record_token(CookieToken.split("|")[0], CookieToken, 1)
        resp.set_cookie(key="token", value=str(token), expires=int(dr.site_config_data["TokenExpire"]), max_age=int(dr.site_config_data["TokenExpire"]))
        return resp, {"Refresh": "0; url=/"}
    return resp

#handle Adduser
@app.route("/admin/addUser.html", methods=["GET","POST"])
def AddUser():
    perm_code = handle_users.check_site_perm("/admin/addUser.html", request.cookies.get("token"))
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"}
    #handle post
    bg_color = "#FFFFFF"
    font_color = "#FFFFFF"
    response = ""
    if request.method == "POST":
        font_color, bg_color, response = handle_users.AddUser(request.form)
    role_options = ""
    group_options = ""
    for i in range(len(dr.roles_data)-1):
        role_options += f"<option value='{str(dr.roles_data[i+1][0])}'>{dr.roles_data[i+1][2]}</option>"
    for i in range(len(dr.groups_data)-1):
        group_options += f"<option value='{str(dr.groups_data[i+1][0])}'>{dr.groups_data[i+1][2]}</option>"    
    return serve_html_website("/admin/addUser.html").replace("ROLE_OPTIONS", role_options).replace("GROUP_OPTIONS", group_options).replace("RESPONSE", response).replace("FONTCOLOR", font_color).replace("BG_COLOR", bg_color)

@app.route("/admin/remove_user", methods=["POST"])
def remove_user():
    perm_code = handle_users.check_site_perm("/admin/remove_user.html", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "401", {"Refresh": "0; url=/401.html"}
    id = request.json["userId"]
    handle_users.remove_user(int(id))
    print(id)
    return "asd"

@app.route("/admin/users.html")
def users():
    perm_code = handle_users.check_site_perm("/admin/users.html", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    users = ""
    for i in range(len(dr.users_data)-1):
        id = dr.users_data[i+1][0]
        users += f"<tr><td class='id_td'>{id}</td><td class='name_td'>{dr.users_data[i+1][1]}</td><td class='modify_td'><a href='/modifyuser/{id}'>Modify</a></td><td class='del_td'><button onclick='delete_user({id},\"{dr.users_data[i+1][1]}\")'>Delete User</button></td></tr>"
    return serve_html_website("/admin/users.html").replace("USERS", users)    

#Handle user pages
@app.route("/user/<path:p>", methods=["GET","POST"])
def user_page(p):
    alert = ""
    perm_code = handle_users.check_site_perm("/user/"+p, request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    id = int(p)
    #update data if its possible
    if request.method == "POST":
        #get data type set by form variable
        rtype = request.form["rtype"]
        if rtype == "uname":
            username = request.form["username"]
            email = request.form["email"]
            full_name = request.form["full_name"]
            description = request.form["description"]
            new_users_data = dr.users_data
            if username != dr.users_data[id][1]:
                #username changed
                usernames = []
                for i in range(len(dr.users_data)-1):
                    usernames.append(dr.users_data[i+1][1])
                if username not in usernames:
                    new_users_data[id][1] = username
                else:
                    #insert alert message if the name is still in use
                    alert += "Username already in use!"
            if email != dr.users_data[id][2]:
                new_users_data[id][2] = email
            if full_name != dr.users_data[id][3]:
                new_users_data[id][3] = full_name
            if description != dr.users_data[id][4]:
                new_users_data[id][4] = description
            f = open("./data/users.csv", "w", encoding="UTF-8", newline='')
            writer = csv.writer(f)
            for row in new_users_data:
                writer.writerow(row)
            f.close()
            alert = "Data Changed, Logging out"
        elif rtype == "pwd":
            new_hash_data = dr.hash_data
            c_pass = request.form["current_pass"]
            pass1 = request.form["password1"]
            pass2 = request.form["password2"]
            if hashlib.md5(bytes(c_pass, "UTF-8")).hexdigest() != dr.hash_data[id][1]:
                alert = "Current Password is Invalid!"
            else:
                if pass1 != pass2:
                    alert = "Passwords do not match!"
                else:
                    new_hash_data[id][1] = hashlib.md5(bytes(pass1, "UTF-8")).hexdigest()
                    alert = "Data Changed, Logging out"
            f = open("./data/pwd_hashes.csv", "w", encoding="UTF-8", newline='')
            writer = csv.writer(f)
            for row in new_hash_data:
                writer.writerow(row)
            f.close()              


    username = dr.users_data[id][1]
    email = dr.users_data[id][2]
    full_name = dr.users_data[id][3]
    description = dr.users_data[id][4]
    ret = serve_html_website("/user/index.html").replace("#DESCRIPTION#", description).replace("#EMAIL#", email).replace("#USERNAME#", username).replace("#FULL_NAME#", full_name)
    if alert != "":
        ret += "<script>alert('"+ alert +"')</script>"
    if alert == "Data Changed, Logging out":
        return "Data Changed, Logging out!", {"Refresh":"2; url=/signout.html"}
    else:
        return ret

#handle any other static site
@app.route('/<path:p>')
def static_sites(p):
    if p[-1] == "/":
        p += "index.html"
    perm_code = handle_users.check_site_perm(p, request.cookies.get("token"))
    if perm_code == "200":
        return serve_html_website(p)
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"}


app.run(debug=True)