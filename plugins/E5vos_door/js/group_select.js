let group_select = document.getElementById("groups_select")
let group_display = document.getElementById("groups_display")
let group_post = document.getElementById("groups_post")
let group_names = {}


let group_ids = []

function read_names(){

    let group_html = group_select.innerHTML
    group_split = group_html.split("</option>")
    group_split.pop()
    group_split.forEach(element => {
            element = element.replace("\n", "")
            if (element != ""){
                let group_name = element.split(">")[1]
                let group_id = element.replace('">' + group_name, "").split('"')[1]
                group_names[group_id] = group_name
            }
    })
}

function remove_group(id){
    let group_name = group_names[id]
    let new_innerData = ""
    let display_split = group_display.innerHTML.split("</tr>")
    display_split.pop()
    display_split.forEach(line =>{
        if (line.split("<td>")[1].split("<button")[0] != group_name){
            new_innerData = new_innerData + line + "</tr>"
        }
    })
    group_display.innerHTML = new_innerData
    new_ids = []
    group_ids.forEach(cur_id => {
        if (cur_id != id){
            new_ids[new_ids.length] = cur_id
        }
    })
    group_ids = new_ids
    submit_value = ""
    group_ids.forEach(id => {submit_value += id + ";"})
    group_post.value = submit_value
}

function group_changed(){
    let group_id = group_select.value
    group_select.value = 0
    if (group_id == "0"){
        return
    }
    let SelectedAlready = 0
    group_ids.forEach(id => {
        if(id == group_id){
            SelectedAlready = 1
        }
    });
    if(!SelectedAlready){
        group_ids[group_ids.length] = group_id
        let group_name = group_names[group_id]
        group_display.innerHTML = group_display.innerHTML + "<tr><td>"+ group_name + "<button type='button' onclick='remove_group(" + group_id + ")'>X</button></td></tr>"
        submit_value = ""
        group_ids.forEach(id => {submit_value += id + ";"})
        submit_value[-1] = ""
        group_post.value = submit_value
    }
}

function addGroupManually(id){
    group_select.value = id
    group_changed()
}

group_select.addEventListener("change", group_changed)

read_names()