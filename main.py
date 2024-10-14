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
        users += f"<tr><td class='id_td'>{id}</td><td class='name_td'>{dr.users_data[i+1][1]}</td><td class='modify_td'><a href='/admin/modifyUser/{id}'>Modify</a></td><td class='del_td'><button onclick='delete_user({id},\"{dr.users_data[i+1][1]}\")'>Delete User</button></td></tr>"
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
        alert = "Data Changed, Logging out"
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
                    print("username used already")
                    alert = "Username already in use!"
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

#Handle admin user modify
@app.route("/admin/modifyUser/<path:p>", methods=["GET","POST"])
def admin_user_page(p):
    alert = ""
    perm_code = handle_users.check_site_perm("/admin/modifyUser/"+p, request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    id = int(p)
    #update data if its possible
    if request.method == "POST":
        alert = ""
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
                    print("username used already")
                    alert = "Username already in use!"
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
        elif rtype == "pwd":
            new_hash_data = dr.hash_data
            pass1 = request.form["password1"]
            pass2 = request.form["password2"]
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
        elif rtype == "roles":
            ids = request.form["roles_post"]
            new_user_perms = dr.user_perm_data
            new_user_perms[id][1] = ids[:-1]
            f = open("./data/user_perms.csv", "w", encoding="UTF-8", newline='')
            writer = csv.writer(f)
            for row in new_user_perms:
                writer.writerow(row)
            f.close()
        elif rtype == "groups":
            ids = request.form["groups_post"]
            new_user_perms = dr.user_perm_data
            new_user_perms[id][2] = ids[:-1]
            f = open("./data/user_perms.csv", "w", encoding="UTF-8", newline='')
            writer = csv.writer(f)
            for row in new_user_perms:
                writer.writerow(row)
            f.close()    

    try:
        username = dr.users_data[id][1]
    except IndexError:
        return "", {"Refresh": "0; url=/404.html"}
    email = dr.users_data[id][2]
    full_name = dr.users_data[id][3]
    description = dr.users_data[id][4]
    role_options = ""
    group_options = ""
    for i in range(len(dr.roles_data)-1):
        role_options += f"<option value='{str(dr.roles_data[i+1][0])}'>{dr.roles_data[i+1][2]}</option>"
    for i in range(len(dr.groups_data)-1):
        group_options += f"<option value='{str(dr.groups_data[i+1][0])}'>{dr.groups_data[i+1][2]}</option>" 
    ret = serve_html_website("/admin/modifyUser.html").replace("#DESCRIPTION#", description).replace("#EMAIL#", email).replace("#USERNAME#", username).replace("#FULL_NAME#", full_name).replace("ROLE_OPTIONS", role_options).replace("GROUP_OPTIONS", group_options)
    if alert != "":
        ret += "<script>alert('"+ alert +"')</script>"
    #get roles and groups of user, inject them trough js
    user_roles = dr.user_perm_data[id][1].split(";")
    print(user_roles)
    user_groups = dr.user_perm_data[id][2].split(";")
    ret += "<script>"
    for role_id in user_roles:
        if role_id != "":
            ret += f"addRoleManually({role_id});"
    for group_id in user_groups:
        if group_id != "":
            ret += f"addGroupManually({group_id});"        
    ret += "</script>"        
    return ret
    
#role manager
@app.route("/admin/role_manager.html")
def role_manager():
    perm_code = handle_users.check_site_perm("/admin/role_manager.html", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}

    #<tr><td id="ID">1</td><td id="role_name"><input type="text"></td><td id="role_desc"><input type="text"></td><td id="perm_level"><input class="perm_lvl_field" type="number"></td><td id="del_btn"><button onclick="delete_role(1)">Delete</button></td></tr>    
    role_lines = ""
    for i in range(len(dr.roles_data)-1):
        row = dr.roles_data[i+1]
        role_lines += f'<tr><td id="ID" name="r{str(row[0])}_id">{str(row[0])}</td><td id="role_name"><input type="text" value="{row[2]}" name="r{str(row[0])}_name"></td><td id="role_desc"><input type="text" value="{row[3]}" name="r{str(row[0])}_desc"></td><td id="perm_level"><input class="perm_lvl_field" type="number" value="{row[1]}" name="r{str(row[0])}_perm"></td><td id="del_btn"><button onclick="location.href=\'/admin/deleteRole/{row[0]}\'" type="button">Delete</button></td></tr>'

    return serve_html_website("/admin/role_manager.html").replace("ROLES", role_lines)

@app.route("/admin/deleteRole/<path:id>")
def deleteRole(id):
    perm_code = handle_users.check_site_perm("/admin/deleteRole/" + str(id), request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    
    #delete role
    new_role_data = dr.roles_data
    new_role_data.pop(int(id))

    #delete role from users who have it
    new_user_data = dr.user_perm_data
    for i in range(len(new_user_data)-1):
        #[i+1][1] for roles, [i+1][2] for groups
        if id in new_user_data[i+1][1].split(";"):
            roles = new_user_data[i+1][1].split(";")
            roles.pop(roles.index(id))
            new_user_data[i+1][1] = roles

    #record the old, and new indexes of roles, so we can reassing roles for users later (to avoid a role's id shifting)
    index_pairs = {}
    #reindex existing roles
    ind = 1
    for i in range(len(new_role_data)-1):
        index_pairs[new_role_data[i+1][0]] = ind
        new_role_data[i+1][0] = ind
        ind += 1

    print(index_pairs)

    #replace user perm role indexes with new ones
    for i in range(len(new_user_data)-1):
        #[i+1][1] for roles, [i+1][2] for groups
        roles = new_user_data[i+1][1]
        print("roles: ", roles)
        if type(roles) != list:
            roles = roles.split(";")
        new_roles = ""
        for r in roles:
            new_roles += str(index_pairs[r]) + ";"
        new_roles = new_roles[:-1]
        new_user_data[i+1][1] = new_roles    
        print("nroles: ", new_roles)

    f = open("./data/user_perms.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_user_data:
        writer.writerow(row)
    f.close()

    f = open("./data/roles.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_role_data:
        writer.writerow(row)
    f.close()            

    return "Refreshing!", {"Refresh": "5; url=/admin/role_manager.html"}

@app.route("/admin/changeRoles", methods=["POST"])
def changeRoles():
    perm_code = handle_users.check_site_perm("/admin/changeRoles", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    
    form = request.form
    n_of_errors = 0
    existing_role_names = []
    errors = ""
    new_roles = dr.roles_data

    for s in form:
        id = int(s.split("_")[0].replace("r", ""))
        rtype = s.split("_")[1]
        if rtype == "desc":
            new_roles[id][3] = form[s]
        if rtype == "perm":
            new_roles[id][1] = form[s]
        if rtype == "name":
            existing_role_names.append(form[s])
            if form[s] in existing_role_names:
                if existing_role_names.count(form[s]) == 1:
                    new_roles[id][2] = form[s]
                else:
                    n_of_errors += 1
                    errors += "Name Already Taken: " + form[s] + "<br>"
            else:
                new_roles[id][2] = form[s]


    if n_of_errors == 0:
        f = open("./data/roles.csv", "w", encoding="UTF-8", newline='')
        writer = csv.writer(f)
        for row in new_roles:
            writer.writerow(row)
        f.close()
        return "No Errors! Changes saved successfully!, redirecting in 4 seconds...", {"Refresh":"4;url=/admin/role_manager.html"}
    elif n_of_errors <= 3:
        return errors + "3 or less errors, redirecting in 10 seconds...", {"Refresh":"10;url=/admin/role_manager.html"}
    else:
        return errors + "more than 3 errors, no redirection <br> <a href='/admin/role_manager.html'>Go Back To Role Manager Page</a>"    

#group manager
@app.route("/admin/group_manager.html")
def group_manager():
    perm_code = handle_users.check_site_perm("/admin/group_manager.html", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}

    #<tr><td id="ID">1</td><td id="role_name"><input type="text"></td><td id="role_desc"><input type="text"></td><td id="perm_level"><input class="perm_lvl_field" type="number"></td><td id="del_btn"><button onclick="delete_role(1)">Delete</button></td></tr>    
    group_lines = ""
    for i in range(len(dr.groups_data)-1):
        row = dr.groups_data[i+1]
        group_lines += f'<tr><td id="ID" name="r{str(row[0])}_id">{str(row[0])}</td><td id="group_name"><input type="text" value="{row[2]}" name="r{str(row[0])}_name"></td><td id="group_desc"><input type="text" value="{row[3]}" name="r{str(row[0])}_desc"></td><td id="perm_level"><input class="perm_lvl_field" type="number" value="{row[1]}" name="r{str(row[0])}_perm"></td><td id="del_btn"><button onclick="location.href=\'/admin/deleteGroup/{row[0]}\'" type="button">Delete</button></td></tr>'

    return serve_html_website("/admin/group_manager.html").replace("GROUPS", group_lines)

#delete group
@app.route("/admin/deleteGroup/<path:id>")
def deleteGroup(id):
    perm_code = handle_users.check_site_perm("/admin/deleteGroup/" + str(id), request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    
    #delete group
    new_group_data = dr.groups_data
    new_group_data.pop(int(id))

    #delete group from users who have it
    new_user_data = dr.user_perm_data
    for i in range(len(new_user_data)-1):
        #[i+1][1] for roles, [i+1][2] for groups
        if id in new_user_data[i+1][2].split(";"):
            groups = new_user_data[i+1][2].split(";")
            groups.pop(groups.index(id))
            new_user_data[i+1][2] = groups

    #record the old, and new indexes of roles, so we can reassing roles for users later (to avoid a role's id shifting)
    index_pairs = {}
    #reindex existing roles
    ind = 1
    for i in range(len(new_group_data)-1):
        index_pairs[new_group_data[i+1][0]] = ind
        new_group_data[i+1][0] = ind
        ind += 1

    print(index_pairs)

    #replace user perm group indexes with new ones
    for i in range(len(new_user_data)-1):
        #[i+1][1] for roles, [i+1][2] for groups
        groups = new_user_data[i+1][2]
        if type(groups) != list:
            groups = groups.split(";")
        new_groups = ""
        for r in groups:
            new_groups += str(index_pairs[r]) + ";"
        new_groups = new_groups[:-1]
        new_user_data[i+1][2] = new_groups

    f = open("./data/user_perms.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_user_data:
        writer.writerow(row)
    f.close()

    f = open("./data/groups.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_group_data:
        writer.writerow(row)
    f.close() 

    return "Refreshing!", {"Refresh": "5; url=/admin/group_manager.html"}    

#change groups
@app.route("/admin/changeGroups", methods=["POST"])
def changeGroups():
    perm_code = handle_users.check_site_perm("/admin/changeGroups", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    
    form = request.form
    n_of_errors = 0
    existing_group_names = []
    errors = ""
    new_groups = dr.groups_data

    for s in form:
        id = int(s.split("_")[0].replace("r", ""))
        rtype = s.split("_")[1]
        if rtype == "desc":
            new_groups[id][3] = form[s]
        if rtype == "perm":
            new_groups[id][1] = form[s]
        if rtype == "name":
            existing_group_names.append(form[s])
            if form[s] in existing_group_names:
                if existing_group_names.count(form[s]) == 1:
                    new_groups[id][2] = form[s]
                else:
                    n_of_errors += 1
                    errors += "Name Already Taken: " + form[s] + "<br>"
            else:
                new_groups[id][2] = form[s]


    if n_of_errors == 0:
        f = open("./data/groups.csv", "w", encoding="UTF-8", newline='')
        writer = csv.writer(f)
        for row in new_groups:
            writer.writerow(row)
        f.close()
        return "No Errors! Changes saved successfully!, redirecting in 4 seconds...", {"Refresh":"4;url=/admin/group_manager.html"}
    elif n_of_errors <= 3:
        return errors + "3 or less errors, redirecting in 10 seconds...", {"Refresh":"10;url=/admin/group_manager.html"}
    else:
        return errors + "more than 3 errors, no redirection <br> <a href='/admin/group_manager.html'>Go Back To Role Manager Page</a>"

#add role post
@app.route("/admin/add_role.html", methods=["POST"])
def add_role_post():
    perm_code = handle_users.check_site_perm("/admin/add_role.html", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    form = request.form
    name = form["name"]
    desc = form["desc"]
    perm = form["perm_level"]

    #if no perm is specified we just block the role
    if perm == "":
        perm = "-1"

    new_roles = dr.roles_data
    existing_names = []

    for i in range(len(new_roles)-1):
        existing_names.append(new_roles[i+1][2])

    if name in existing_names:
        return "Name is Already Taken! Redirecting in 5...", {"Refresh":"5;url=/admin/add_role.html"}
    
    id = len(new_roles)

    new_row = [str(id), str(perm), name, desc]
    new_roles.append(new_row)
    f = open("./data/roles.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_roles:
        writer.writerow(row)
    f.close()
    return "Role Added! Redirecting in 5...", {"Refresh":"5;url=/admin/add_role.html"}

#add group post
@app.route("/admin/add_group.html", methods=["POST"])
def add_group_post():
    perm_code = handle_users.check_site_perm("/admin/add_group.html", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    form = request.form
    name = form["name"]
    desc = form["desc"]
    perm = form["perm_level"]

    #if no perm is specified we just block the role
    if perm == "":
        perm = "-1"

    new_groups = dr.groups_data
    existing_names = []

    for i in range(len(new_groups)-1):
        existing_names.append(new_groups[i+1][2])

    if name in existing_names:
        return "Name is Already Taken! Redirecting in 5...", {"Refresh":"5;url=/admin/add_group.html"}
    
    id = len(new_groups)

    new_row = [str(id), str(perm), name, desc]
    new_groups.append(new_row)
    f = open("./data/groups.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_groups:
        writer.writerow(row)
    f.close()
    return "group Added! Redirecting in 5...", {"Refresh":"5;url=/admin/add_group.html"}    

#handle site perms list page
@app.route("/admin/site_perms.html")
def site_perms():
    perm_code = handle_users.check_site_perm("/admin/site_perms.html", request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    perms = ""
    for i in range(len(dr.site_perm_data)-1):
        endpoint = dr.site_perm_data[i+1][0]
        #ENDPOINTS MUST START WITH /
        perms += f"<tr><td class='endpoint_td'>{endpoint}</td><td class='al_td'>{dr.site_perm_data[i+1][1]}</td><td class='modify_td'><a href='/admin/modify_site_perm/{endpoint[1:]}'>Modify</a></td><td class='del_td'><button onclick=\"location.href=\'/admin/delete_site_perm/{endpoint[1:]}\'\">Delete Rule</button></td></tr>"
    return serve_html_website("/admin/site_perms.html").replace("PERMS", perms)

#delete site perm rule
@app.route("/admin/delete_site_perm/<path:p>")
def delete_site_perm(p):
    perm_code = handle_users.check_site_perm("/admin/delete_site_perm/" + p, request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}
    new_site_perms = [dr.site_perm_data[0]]
    for i in range(len(dr.site_perm_data)-1):
        if dr.site_perm_data[i+1][0] != "/" + p:
            new_site_perms.append(dr.site_perm_data[i+1])
    
    f = open("./data/site_perms.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_site_perms:
        writer.writerow(row)
    f.close()
    return "Changes Made! Refreshing...", {"Refresh":"6;url=/admin/site_perms.html"}        

#Modify site permissions
@app.route("/admin/modify_site_perm/<path:p>")
def modify_site_perm(p):
    perm_code = handle_users.check_site_perm("/admin/modify_site_perm/" + p, request.cookies.get("token"))
    if perm_code == "401":
        print("not allowed")
        return "", {"Refresh": "0; url=/401.html"}

    row = ""
    for i in range(len(dr.site_perm_data)-1):
        if dr.site_perm_data[i+1][0] == "/" + p:
            row = dr.site_perm_data[i+1]
    if row == "":
        return "Rule doesnt exist!", {"Refresh":"6;url=/admin/site_perms.html"}
    accessLevel = row[1]
    roleIDs = row[2]
    groupIDs = row[3]
    userIDs = row[4]
    pl = row[5]
    role_pair = {}
    group_pair = {}
    user_pair = {}
    roles = ""
    groups = ""
    users = ""
    al = "<option value='-1'>Disabled</option><option value='0'>Role/Group/User limit</option><option value='1'>Access set by perm level</option>"
    al = al.replace(f"value='{accessLevel}'",f"value='{accessLevel}' selected")

    for i in range(len(dr.roles_data)-1):
        role_pair[dr.roles_data[i+1][0]] = dr.roles_data[i+1][2]

    for i in range(len(dr.groups_data)-1):
        group_pair[dr.groups_data[i+1][0]] = dr.groups_data[i+1][2]

    for i in range(len(dr.users_data)-1):
        user_pair[dr.users_data[i+1][0]] = dr.users_data[i+1][1]

    for id in role_pair.keys():
        roles += f"<option value='{id}'>{role_pair[id]}</option>"
    for id in group_pair.keys():
        groups += f"<option value='{id}'>{group_pair[id]}</option>"
    for id in user_pair.keys():
        users += f"<option value='{id}'>{user_pair[id]}</option>"
    users += f"<option value='-1'>Per User Pages</option>"

    manual_adds = "<script>"
    #rendering already used groups roles etc
    for id in roleIDs.split(";"):
        if id == "":continue
        manual_adds += f"addRoleManually({id});"
    for id in groupIDs.split(";"):
        if id == "":continue
        manual_adds += f"addGroupManually({id});"
    for id in userIDs.split(";"):
        if id == "":continue
        manual_adds += f"addUserManually({id});"

    manual_adds += "</script>"
    return serve_html_website("/admin/modify_site_perm.html").replace("ENDPOINT", "/" + p).replace("ROLES", roles).replace("GROUPS", groups).replace("USERS", users).replace("PERMLEVEL", pl).replace("ACCESSLEVEL", al) + manual_adds
    

@app.route("/admin/modify_perm/", methods=["POST"])
def modify_perm():
    form = request.form
    endpoint = form["endpoint"]
    AL = form["AL"]
    #truncating of extra ;
    roles = form["roles_post"][:-1]
    groups = form["groups_post"][:-1]
    users = form["users_post"][:-1]
    perm_level = form["perm_level"]
    
    new_perms = dr.site_perm_data
    print(new_perms)
    for i in range(len(new_perms)-1):
        if new_perms[i+1][0] == endpoint:
            new_perms[i+1][1] = AL
            new_perms[i+1][2] = roles
            new_perms[i+1][3] = groups
            new_perms[i+1][4] = users
            new_perms[i+1][5] = perm_level
    f = open("./data/site_perms.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(f)
    for row in new_perms:
        writer.writerow(row)
    f.close()
    return "Rule modified!"


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