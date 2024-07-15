from flask import Flask
import os,csv
from flask import send_from_directory, request, make_response
import handle_users, time
from datetime import datetime,timedelta
import data_reader as dr
dr.init()
def create_app():
    app = Flask(__name__)
    return app

def serve_html_website(route):
    if not os.path.exists("./templates/" + route):
        return "", {"Refresh": "0; url=/404.html"} 
    f = open("./templates/" + route)
    return f.read()

app = create_app()

#handle favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                            'favicon.ico', mimetype='image/vnd.microsoft.icon')

#handle index.html
@app.route("/")
def index():
    return serve_html_website("index.html")

#handle sign out
@app.route("/signout.html")
def signout():
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
    if not os.path.exists("./css/"+p):
        return "No such file"
    f = open("./css/"+p)
    return f.read()

#handle js
@app.route("/js/<path:p>")
def js(p):
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

#handle any other static site
@app.route('/<path:p>')
def static_sites(p):
    if p[-1] != "/" and "." not in p:
        p += "/"

    if p[-1] == "/":
        p += "index.html"
    perm_code = handle_users.check_site_perm(p, request.cookies.get("token"))
    if perm_code == "200":
        return serve_html_website(p)
    if perm_code == "401":
        return "", {"Refresh": "0; url=/401.html"} 


app.run(debug=True)