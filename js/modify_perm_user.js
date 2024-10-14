let user_select = document.getElementById("users_select")
let user_display = document.getElementById("users_display")
let user_post = document.getElementById("users_post")
let user_names = {}


let user_ids = []

function read_names(){
    let user_html = user_select.innerHTML
    user_split = user_html.split("</option>")
    user_split.pop()
    user_split.forEach(element => {
            element = element.replace("\n", "")
            if (element != ""){
                let user_name = element.split(">")[1]
                let user_id = element.replace('">' + user_name, "").split('"')[1]
                user_names[user_id] = user_name
            }
    })
}

function remove_user(id){
    let user_name = user_names[id]
    let new_innerData = ""
    let display_split = user_display.innerHTML.split("</tr>")
    display_split.pop()
    display_split.forEach(line =>{
        if (line.split("<td>")[1].split("<button")[0] != user_name){
            new_innerData = new_innerData + line + "</tr>"
        }
    })
    user_display.innerHTML = new_innerData
    new_ids = []
    user_ids.forEach(cur_id => {
        if (cur_id != id){
            new_ids[new_ids.length] = cur_id
        }
    })
    user_ids = new_ids
    submit_value = ""
    user_ids.forEach(id => {submit_value += id + ";"})
    user_post.value = submit_value
}

function user_changed(){
    let user_id = user_select.value
    user_select.value = 0
    if (user_id == "0"){
        return
    }
    let SelectedAlready = 0
    user_ids.forEach(id => {
        if(id == user_id){
            SelectedAlready = 1
        }
    });
    if(!SelectedAlready){
        user_ids[user_ids.length] = user_id
        let user_name = user_names[user_id]
        user_display.innerHTML = user_display.innerHTML + "<tr><td>"+ user_name + "<button type='button' onclick='remove_user(" + user_id + ")'>X</button></td></tr>"
        submit_value = ""
        user_ids.forEach(id => {submit_value += id + ";"})
        submit_value[-1] = ""
        user_post.value = submit_value
    }
}

function addUserManually(id){
    user_select.value = id
    user_changed()
}


user_select.addEventListener("change", user_changed)

read_names()