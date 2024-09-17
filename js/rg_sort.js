var sort_radio = document.getElementsByName("sort");
var data = document.getElementById("data_table")
//defining them up here for prettiness and to not cause issues with non-existent variables 
var ID_sort = ''
var Name_sort = ''
var Perm_sort = ''

function UpdateSorts(){
    let data_split = data.innerHTML.split("</tr>")
    id_obj = {}
    for(i=0; i<data_split.length-1; i++){
        id_obj[data_split[i].split("</td>")[0].split(">")[2]] = data_split[i] + "</tr>\n"
    }
    keys = Object.keys(id_obj)
    sorted = keys.sort(function(a, b){return a - b})
    
    sorted.forEach(element => {
        ID_sort += id_obj[element]
    })

    name_obj = {}
    name_index = 1
    for(i=0; i<data_split.length-1; i++){
        key = data_split[i].split('value="')[1].split('">')[0].toLowerCase() + "_0"
        if(key in name_obj){
            key = key.replace('"_0', "")
            key += "_" + name_index.toString()
            name_index++
        }
        name_obj[key] = data_split[i] + "</tr>\n"
    }
    keys = Object.keys(name_obj)
    sorted = keys.sort()
    
    sorted.forEach(element => {
        Name_sort += name_obj[element]
    })

    perm_obj = {}
    perm_index = 1
    allLvLs = []
    for(i=0; i<data_split.length-1; i++){
        key = data_split[i].split('type="number" ')[1].split(">")[0].replace("value=", "").replaceAll("\"", "").toLowerCase() + "_0"
        if(key in perm_obj){
            key = key.replace("_0", "")
            key += "_" + perm_index.toString()
            perm_index++
        }

        if (allLvLs.indexOf(parseInt(key.split("_")[0])) == -1){
            allLvLs.push(parseInt(key.split("_")[0]))
        }
        perm_obj[key] = data_split[i] + "</tr>\n"
    }

    keys = Object.keys(perm_obj)
    for(i=0; i<allLvLs.length; i++){
        max = Math.max(...allLvLs)
        keys.forEach(element => {
            console.log(element.split("_")[0])
            if (parseInt(element.split("_")[0]) == max){
                Perm_sort += perm_obj[element]
            }
        })
        allLvLs[allLvLs.indexOf(max)] = -10
    }
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