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
                open_time = dr.plugin_configs["Door_open_time"]
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

@endpoint("/users/")
def users_page():
    global db
    users = db.get_users()
    dom_list = ""
    for i in range(len(users)):
        print(users[i])
        UUID = users[i][0]
        name = users[i][1]
        email = users[i][2]
        e5kod =users[i][3]
        comment =users[i][4]
        groups = users[i][5]
        enabled = users[i][6]
        created =users[i][7]
        lastused = users[i][8]
        dom_list += f"<tr id='{i+1}'>\n<td id='{i+1}_UUID'>{UUID}</td>\n<td id='{i+1}_name'>{name}</td>\n<td id='{i+1}_email'>{email}</td>\n<td id='{i+1}_e5kod'>{e5kod}</td>\n<td id='{i+1}_comment'>{comment}</td>\n<td id='{i+1}_groups'>{groups}</td>\n<td id='{i+1}_enabled'>{enabled}</td>\n<td id='{i+1}_created'>{created}</td>\n<td id='{i+1}_lastused'>{lastused}</td>\n<td id='{i+1}_modify'><a href='../modify_tag/{UUID}'>Modify</a></td>\n<td id='{i+1}_delete'><a href='../delete_tag/{UUID}'>Delete</a></td>\n</tr>\n"

    return serve_html_website("user_data.html").replace("TABLE", dom_list)

@endpoint("/css/*")
def css(p):
    pl_path = PluginData().path
    if pl_path[-1] != "/":
        pl_path += "/"  
    if not os.path.exists(f".{pl_path}css/{p}"):
        return "No such file"
    f = open(f".{pl_path}css/{p}")
    return f.read()

@endpoint("/modify_tag/*")
def modify_tag(p):
    global db
    user = db.get_single_user(p)
    enabled_data = user[6]
    enabled_data = int(enabled_data)
    website = serve_html_website("modify_tag.html")
    if enabled_data:
        website = website.replace("option value=\"1\"", "option value=\"1\" selected")
    else:
        webiste = website.replace("option value=\"0\"", "option value=\"0\" selected")
    website = website.replace("UUID_DATA", p).replace("NAME_DATA", user[1]).replace("EMAIL_DATA", user[2]).replace("E5KOD_DATA", user[3]).replace("COMMENT_DATA", user[4])
    
    #get groups
    group_options = ""
    groups = db.get_groups()
    for i in range(len(groups)):
        group_options += f"<option value={i+1}>{groups[i][1]}</option>\n"

    website = website.replace("GROUP_OPTIONS", group_options)
    return website

@endpoint("/modify_tag_function/groups/*")
def modify_groups(p,request):
        global db
        group_data = request.form["groups_post"]
        db.update_groups(p, group_data[:-1])
        return "Groups modified!", {"Refresh": "5; url=../../users/"}

@endpoint("/modify_tag_function/data/*")
def modify_data(p,request):
        global db
        name = request.form["name"]
        email = request.form["email"]
        e5kod = request.form["e5kod"]
        comment = request.form["comment"]
        enabled = request.form["enabled"]
        db.update_tag_data(p, name, email, e5kod, comment, enabled)
        return "Data modified!", {"Refresh": "5; url=../../users/"}

@endpoint("/delete_tag/*")
def delete_tag(p):
    global db
    db.delete_tag(p)
    return "Tag deleted!", {"Refresh": "5; url=../users/"}

@endpoint("/switch_groups/")
def switch_groups():
    global db
    website = serve_html_website("switch_groups.html")
    groups = db.get_groups()
    table = ""
    for i in range(len(groups)):
        table += f"<tr id={i+1}><td id='{i+1}ID'>{groups[i][0]}</td><td id='{i+1}name'>{groups[i][1]}</td><td id='{i+1}enabled'>{groups[i][2]}</td><td id='{i+1}link'><a href='../switch_group_function/{groups[i][0]}'>Switch</a></td></tr>\n"
    return website.replace("TABLE_REPLACE", table)

@endpoint("/switch_group_function/*")
def switch_function(p):
    global db
    groups = db.get_groups()
    id = int(p)
    enabled = int(groups[id-1][2])
    if enabled == 1:
        enabled = 0
    else:
        enabled = 1
    db.set_group_enabled(id, enabled)
    return "", {"Refresh": "0; url=../switch_groups/"}

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


@endpoint("/entries/")
def entries():
    global db
    website = serve_html_website("entries.html")
    entries = db.get_entries()
    table = ""
    users = db.get_users()
    user_pair = {}
    for l in range(len(users)):
        user_pair[users[l][0]] = users[l][1]
    print(user_pair)
    for i in range(len(entries)):
        try:
            username = user_pair[entries[i][1]]
        except:
            username = "NO USER ASSIGNED"
        table += f"<tr><td id='{i+1}ID'>{entries[i][0]}</td><td id='{i+1}UUID'>{entries[i][1]}</td><td id='{i+1}name'>{username}</td><td id='{i+1}succesful'>{entries[i][2]}</td><td id='{i+1}entry_time'>{entries[i][3]}</td></tr>\n"
    website = website.replace("TABLE", table)
    return website
