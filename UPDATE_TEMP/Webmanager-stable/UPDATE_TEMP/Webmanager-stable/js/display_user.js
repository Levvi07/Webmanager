cookies = document.cookie
if(cookies != ""){
    let id = cookies.split("|")[0].replace("token=", "");
    let name = cookies.split("|")[1];
    document.getElementById("user_button").innerHTML = name;
    document.getElementById("user_button").href = "/user/" + id
}else{
    document.getElementById("user_button").href = "/login.html"
}