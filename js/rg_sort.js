var sort_radio = document.getElementsByName("sort");
var data = document.getElementById("data_table")
//defining them up here for prettiness and to not cause issues with non-existent variables 
var ID_sort = '<tr><td>ID</td><td>Role Name</td><td>Role Description</td><td class="perm_lvl_field">Permission Level</td></tr>'
var Name_sort = '<tr><td>ID</td><td>Role Name</td><td>Role Description</td><td class="perm_lvl_field">Permission Level</td></tr>'
var Perm_sort = '<tr><td>ID</td><td>Role Name</td><td>Role Description</td><td class="perm_lvl_field">Permission Level</td></tr>'

function UpdateSorts(){
    let data_split = data.innerHTML.split("</tr>")
    console.log(data_split[1])
}

function change_sort(){
    let val = ""
    for (i = 0; i < sort_radio.length; i++) {
        if (sort_radio[i].checked){
            val = sort_radio[i].value
        }
    }


    if (val == "ID"){
        data.innerHTML = ID_sort

    }else if (val == "Name"){
        data.innerHTML = Name_sort
    }
    else if (val == "Perm_level"){
        data.innerHTML = Perm_sort
    }
}

UpdateSorts()

sort_radio.forEach(element => {
    element.addEventListener("change", change_sort)
})