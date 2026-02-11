var sort_radio = document.getElementsByName("sort");
var users = document.getElementById("users_table")
//we can just make em constant they dont change
//defining them up here for prettiness and to not cause issues with non-existent variables 
var ID_sort = ""
var Name_sort = '<tr><td class="id_td" style="width:5%;height:3%;text-align:center;font-family:Helvetica">ID</td><td class="name_td" style="text-align:center;font-weight:bold;font-family:Helvetica">NAME</td></tr>\n'


function change_sort(){
    let val = ""
    for (i = 0; i < sort_radio.length; i++) {
        if (sort_radio[i].checked){
            val = sort_radio[i].value
        }
    }



    if (val == "ID"){
        users.innerHTML = ID_sort

    }else if (val == "Name"){
        users.innerHTML = Name_sort
    }
}


//<tr><td class="id_td">1</td><td class="name_td">Levi</td><td class="modify_td"><a href="/modifyuser/1">Modify</a></td><td class="del_td"><button onclick="delete_user(1,&quot;Levi&quot;)">Delete User</button></td>


/*
//first make an ID sort
for(var i=0;i<users_split.length;i++) {
    let id = users_split[i].split("</td>")[0].split(">")[2]
    table[id] = users_split[i] + "</tr>"
}

keys = Object.keys(table)
keys_sorted = keys.sort()

//resetting the table
table = {}
*/
//<tr><td class="id_td">1</td><td class="name_td">Levi</td><td class="modify_td"><a href="/modifyuser/1">Modify</a></td><td class="del_td"><button onclick="delete_user(1,&quot;Levi&quot;)">Delete User</button></td>

let users_split = users.innerHTML.split("</tr>")

for(var i=0;i<users_split.length;i++) {
    users_split[i] = users_split[i].replace("\n", "").trim()
}

//removing the empty string left by the split with pop() and header with shift()  
users_split.pop() // deletes last element
users_split.shift() // deletes first element

//used for temporarily storing the lines either using the ids/names as keys
var table = {}


//then make a Name sort
for(var i=0;i<users_split.length;i++) {
    let uname = users_split[i].split("</td>")[1].split(">")[1].toLowerCase()
    table[uname] = users_split[i] + "</tr>\n"
}

keys = Object.keys(table)
sorted = keys.sort()

sorted.forEach(element => {
    Name_sort = Name_sort + table[element]
})

//Table is already ID sorted, just take it
ID_sort = users.innerHTML

sort_radio.forEach(element => {
    element.addEventListener("change", change_sort)
})