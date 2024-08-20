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
    delete_link.setAttribute("onclick" , "confirmed_delete('"+ id + "')")
}

canDelete = true
function confirmed_delete(id){
    if(!canDelete){
        alert("Wait for the page to refresh!")
    }
    canDelete = false
    fetch("/admin/remove_user", {
        method: "POST",
        body: JSON.stringify({
            userId: id.toString()
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    setTimeout(() => {
        location.reload()
    }, 500)
}

function change_button_disabled(){
    state = !delete_checkbox.checked
    delete_link.disabled = state
}

delete_checkbox.addEventListener("change", change_button_disabled)