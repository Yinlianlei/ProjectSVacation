function registerChange(){
    var target1 = document.getElementById("password_see_not");
    var target2 = document.getElementById("password_see");

    if(target1.style.display == "none"){
        target1.style.display = "inline";
        target2.style.display = "none";
    }else{
        target1.style.display = "none";
        target2.style.display = "inline";
    }
}