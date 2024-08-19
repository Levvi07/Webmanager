from flask import Flask
import os
from flask import send_from_directory, request, make_response
import handle_users
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
    perm_code = handle_users.check_site_perm("/admin/remove_user.html", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    users = ""
    for i in range(len(dr.users_data)-1):
        id = dr.users_data[i+1][0]
        users += f"<tr><td>{id}</td><td>{dr.users_data[i+1][1]}</td><td><a href='/modifyuser/{id}'>Modify</a></td><td><button onclick='delete_user({id},\"{dr.users_data[i+1][1]}\")'>Delete User</button></td></tr>"
    return serve_html_website("/admin/users.html").replace("USERS", users)    


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