function loginChange(){
    var target1 = document.getElementById("password_see_not");
    var target2 = document.getElementById("password_see");
    var pwd = document.getElementById("passwordInput");

    if(target1.style.display == "none"){
        target1.style.display = "inline";
        target2.style.display = "none";
        pwd.type = "password"
    }else{
        target1.style.display = "none";
        target2.style.display = "inline";
        pwd.type = "text"
    }
}