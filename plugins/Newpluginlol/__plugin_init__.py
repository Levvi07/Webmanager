#--------------------------------------------------------------

## IMPORTANT ##

# This file is a standardised file for all plugins
# This file MUST exist in the root folder of the plugin otherwise it wont work
# Use the page decorator for defining your endpoints
# The data in the PluginData class is not compulsory, but advisable, EXCEPT the name field, which must not be empty

# only edit onwards from the "EDIT FROM HERE" flag as the first part is just operative and changing it might break your plugin
#---------------------------------------------------------------
class PluginData():
    name = "NewPluginLol"
    version = "1.3cv"
    description = "This is a template plugin"
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

import json
import data_reader as dr
@endpoint("/")
def index(request):
    return serve_html_website("index.html").replace("CONFIG", str(dr.site_config_data)).replace("REQUEST", str(request.form))

@endpoint("/admin/")
def adminpage():
    return serve_html_website("SecondSite.html")

@endpoint("/css/*")
def css(p):
    pl_path = PluginData().path
    if pl_path[-1] != "/":
        pl_path += "/"  
    if not os.path.exists(f".{pl_path}css/{p}"):
        return "No such file"
    f = open(f".{pl_path}css/{p}")
    return f.read()

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