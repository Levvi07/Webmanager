confirm_popup = document.getElementById("popup")
delete_link = document.getElementById("delete_link")
delete_checkbox = document.getElementById("delete_checkbox")
confirm_text = document.getElementById("confirm_text")
function delete_user(id, name){
    activate = 0
    delete_checkbox.checked = false
    confirm_text.innerHTML = "Are you sure you want to delete the following user?: " + name
    confirm_popup.style.display = "block"
    delete_link.disabled = true
    delete_link.onclick = "confirmed_delete('"+ id + "')"
}

function confirmed_delete(id){
    console.log(id)
}

function change_button_disabled(){
    state = !delete_checkbox.checked
    delete_link.disabled = state
}

delete_checkbox.addEventListener("change", change_button_disabled)