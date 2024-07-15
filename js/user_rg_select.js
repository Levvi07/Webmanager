let role_select = document.getElementById("roles_select")
let group_select = document.getElementById("groups_select")
let role_display = document.getElementById("roles_display")
let role_names = {}
let group_names = {}


let role_ids = []
let group_ids = []

function remove_role(){

}

function remove_group(){

}

function role_changed(){
    role_id = role_select.value
    SelectedAlready = 0
    role_ids.forEach(id => {
        if(id == role_id){
            SelectedAlready = 1
        }
    });
    if(!SelectedAlready){
        alert ("not_selected")
        role_ids += role_id
        alert(role_ids)
    }
    role_display.innerHTML = "<tr><td>Hello</td></tr> <tr><td>Hello2</td></tr>"
}

function group_changed(){
    group_id = group_select.value
}

role_select.addEventListener("change", role_changed)
group_select.addEventListener("change", group_changed)