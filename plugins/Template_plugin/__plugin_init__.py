#--------------------------------------------------------------

## IMPORTANT ##

# This file is a standardised file for all plugins
# This file MUST exist in the root folder of the plugin otherwise it wont work
# Use the page decorator for defining your endpoints
# The data in the PluginData class is not compulsory, but advisable, EXCEPT the name field, which must not be empty

# only edit onwards from the "EDIT FROM HERE" flag as the first part is just operative and changing it might break your plugin
#---------------------------------------------------------------
class PluginData():
    name = "TemplatePlugin"
    version = "1.0"
    description = "A template plugin"
    path = "/plugins/Template_plugin/"
    


import os
def serve_html_website(route):
    if not os.path.exists("./templates/" + route):
        return "", {"Refresh": "0; url=/404.html"}
    if route[-1] != "/" and os.path.isdir("./templates/" + route):
        return "", {"Refresh": "0; url=/404.html"}
    pl_path = PluginData().path
    if pl_path[-1] != "/":
        pl_path += "/"
    f = open(f"./{pl_path}templates/{route}")
    return f.read()

def load_site(endpoint):
    print("endp", endpoint)
    if endpoint in pages.keys():
        print("Returned a normal site")
        return pages[endpoint]()
    else:
        endp_split = endpoint.split("/")
        for k in pages.keys():
            print(repr(k))
        print("------------")
        for i in range(len(endp_split)):
            #i+1 ig [0:i+1]
            print(repr("/".join(endp_split[0:i+1]) + "/*"),  "p:", "/".join(endp_split[i+1:len(endp_split)]))
            if "/".join(endp_split[0:i+1]) + "/*" in pages.keys():
                return pages["/".join(endp_split[0:i+1]) + "/*"]("/".join(endp_split[i+1:len(endp_split)]))
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

import json
import data_reader as dr
@endpoint("/")
def index():
    return serve_html_website("index.html").replace("CONFIG", )

@endpoint("/admin/")
def adminpage():
    return serve_html_website("SecondSite.html")

@endpoint("/css/*")
def css(p):
    print("Returned a css file")
    pl_path = PluginData().path
    if pl_path[-1] != "/":
        pl_path += "/"
    print("css_pl_path",  f".{pl_path}css/{p}")    
    if not os.path.exists(f".{pl_path}css/{p}"):
        return "No such file"
    f = open(f".{pl_path}css/{p}")
    return f.read()

#handle js
@endpoint("/js/*")
def js(p):
    print("returned some js")
    pl_path = PluginData().path
    if pl_path[-1] != "/":
        pl_path += "/"    
    if not os.path.exists(f".{pl_path}js/{p}"):
        return "alert('Missing JS file:" + f".{pl_path}js/{p}" + "')"
    f = open(f".{pl_path}js/{p}")
    return f.read()