from flask import Flask
import os,sqlite3,csv
def create_app():
    app = Flask(__name__)
    return app

def serve_html_website(route):
    if not os.path.exists("./templates/" + route):
        route = "404.html"
    f = open("./templates/" + route)
    return f.read()

app = create_app()
#handle index.html
@app.route("/")
def index():
    return serve_html_website("index.html")


#handle any other static site
@app.route('/<path:p>')
def hello(p):
    print(p)
    if p[-1] != "/" and "." not in p:
        p += "/"

    if p[-1] == "/":
        p += "index.html"
    return serve_html_website(p)


app.run(debug=True)