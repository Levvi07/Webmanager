from flask import Flask
import os,csv
from flask import send_from_directory, request, make_response
import handle_users
from datetime import datetime,timedelta
import data_reader as dr
dr.init()
def create_app():
    app = Flask(__name__)
    return app

def serve_html_website(route):
    if not os.path.exists("./templates/" + route):
        route = "404.html"
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
    return f.read()

#handle login_post
@app.route("/login.html", methods=['POST'])
def handle_login():
    font_color, bg_color, response, token = handle_users.login(request.form)
    resp = make_response(serve_html_website("login.html").replace('<div id="response">', '<div id="response" style="background-color:' + bg_color+ ';color:' + font_color+ '">' + response))
    if token != 0:
        resp.set_cookie(key="token", value=str(token), expires=datetime.today() + timedelta(0,int(dr.site_config_data["TokenExpire"])), max_age=datetime.today() + timedelta(0,int(dr.site_config_data["TokenExpire"])))
    print(token)
    return resp

#handle any other static site
@app.route('/<path:p>')
def static_sites(p):
    if p[-1] != "/" and "." not in p:
        p += "/"

    if p[-1] == "/":
        p += "index.html"
    return serve_html_website(p) + str(request.cookies)


app.run(debug=True)