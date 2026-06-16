#--------------------------------------------------------------

## IMPORTANT ##

# This file is a standardised file for all plugins
# This file MUST exist in the root folder of the plugin otherwise it wont work
# Use the page decorator for defining your endpoints
# The data in the PluginData class is not compulsory, but advisable, EXCEPT the name, and path fields, which must not be empty

# only edit onwards from the "EDIT FROM HERE" flag as the first part is just operative and changing it might break your plugin
#---------------------------------------------------------------
class PluginData():
    name = "E5vosDoor"
    version = "1.0"
    description = "This plugin controls our door in the EAM"
    path = "/plugins/E5vos_door/"



import os
def serve_html_website(route):
    if not os.path.exists("." + PluginData().path + "templates/" + route):
        return "", {"Refresh": "0; url=/404.html"}
    if route[-1] != "/" and os.path.isdir("." + PluginData().path + "templates/" + route):
        return "", {"Refresh": "0; url=/404.html"}
    pl_path = PluginData().path
    if pl_path[-1] != "/":
        pl_path += "/"
    f = open(f"./{pl_path}templates/{route}", encoding="UTF-8")
    return f.read()


import inspect
def load_site(endpoint, request):
    # storing request in a global variable so you dont have to use **kwargs and shit, just store it in a local variable upon execution
    # the function will only pass the request to the function if it has an argument named "request"
    if endpoint in pages.keys():
        args = inspect.getfullargspec(pages[endpoint])
        if "request" in args.args:
            return pages[endpoint](request=request)
        else:
            return pages[endpoint]()
    else:
        endp_split = endpoint.split("/")
        for i in range(len(endp_split)):
            #i+1 ig [0:i+1]
            if "/".join(endp_split[0:i+1]) + "/*" in pages.keys():
                args = inspect.getfullargspec(pages["/".join(endp_split[0:i+1]) + "/*"])
                if "request" in args.args:
                    return pages["/".join(endp_split[0:i+1]) + "/*"](p="/".join(endp_split[i+1:len(endp_split)]), request=request)
                else:
                    return pages["/".join(endp_split[0:i+1]) + "/*"](p="/".join(endp_split[i+1:len(endp_split)]))
    return "", {"Refresh":"0;url=/404.html"}        
    

#store endpoint:function references here
pages = {}


# decorator for defining pages
def endpoint(name):
    def decorator(f):
        pages[name] = f
    return decorator




# EDIT FROM HERE #
# You may use the @endpoint(endpoint) decorator to define a webpage function
# an asterisk does the same thing, as what <path:p> does in flask

import data_reader as dr
from plugins.E5vos_door.subroutines import database
from plugins.E5vos_door.subroutines import pico
from dotenv import load_dotenv
import threading
import time
load_dotenv()
#---Variables---#
db = None
card_name = ""
card_email = ""
card_e5kod = ""
card_message = ""
#---Functions---#
def ReloadDB():
    global db
    if db != None:
        db.Close()
    source = dr.site_config_data["DB_IP"]
    user = dr.site_config_data["DB_username"]
    passwd = os.getenv("PASSWORD")
    db_name = dr.site_config_data["DB_db"]
    table = dr.site_config_data["DB_Table"]
    port = dr.site_config_data["DB_port"]
    entry_table = dr.site_config_data["DB_entry"]
    db = database.Database(source, port, user, passwd, db_name, table, entry_table)
    db.Connect()

ReloadDB()

def Validate(UUID):
    global db
    valid = db.Validate(UUID)
    if valid:
        print("Valid")
        #open door, get time from config otherwise assume 10 seconds
        return 1
    else:
        print("Invalid")
        return 0

def save_card(UUID):
    global db
    global card_name
    global card_email
    global card_e5kod
    global card_message
    
    db.Add(UUID, card_name, card_email, card_e5kod, card_message)

    card_name = ""
    card_email = ""
    card_e5kod = ""
    card_message = ""

    print("NEW CARD ADDED!")

ctr = pico.Pico()
register_new_card = 0
def Listen():
    global register_new_card
    while 1:
        UUID = ctr.Listen()
        if UUID != "" and not UUID.startswith("[MESSAGE]"):
            if register_new_card:
                register_new_card = 0
                save_card(UUID)
                continue
            print("UUID", UUID)
            val = Validate(UUID)
            if val:
                open_time = dr.site_config_data["Door_open_time"]
                try:
                    open_time = int(open_time)
                except:
                    open_time = 15
                ctr.Open(open_time)
            else:
                ctr.Open(-1)
        elif UUID != "" and UUID.startswith("[MESSAGE]"):
            print(UUID)

t = threading.Thread(target=Listen)
t.daemon = True
t.start()

#---Endpoints---#

@endpoint("/")
def index(request):
    return serve_html_website("index.html").replace("CONFIG", str(dr.site_config_data)).replace("REQUEST", str(request.form))

@endpoint("/register_new/")
def register_new():
    return serve_html_website("register_new.html")

@endpoint("/new_card/")
def new_card(request):
    global register_new_card
    global card_name
    global card_email
    global card_e5kod
    global card_message
    card_name = request.form["name"]
    card_email = request.form["email"]
    card_e5kod = request.form["e5kod"]
    card_message = request.form["comment"]
    register_new_card = 1
    return "Tap new card...", {"Refresh":"6;url=../register_new/"} 


@endpoint("/css/*")
def css(p):
    pl_path = PluginData().path
    if pl_path[-1] != "/":
        pl_path += "/"  
    if not os.path.exists(f".{pl_path}css/{p}"):
        return "No such file"
    f = open(f".{pl_path}css/{p}")
    return f.read()

@endpoint("/reloadDB/")
def dbtest():
    ReloadDB()
    return "Reloaded"

#handle js
@endpoint("/js/*")
def js(p):
    pl_path = PluginData().path
    if pl_path[-1] != "/":
        pl_path += "/"    
    if not os.path.exists(f".{pl_path}js/{p}"):
        return "alert('Missing JS file:" + f".{pl_path}js/{p}" + "')"
    f = open(f".{pl_path}js/{p}")
    return f.read()

