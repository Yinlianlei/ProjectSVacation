
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

$(function() {
       $("#usertologin").on('click',function(){
          var form1 = $("#user_pnum").val();
          var form2 = $("#passwordInput").val();
          $.post('/userlogin',data={'tt1':form1,'tt2':form2},function(ret){

            if(ret==='tryagain'){
              alert("密码错误请重新输入");}
            else if(ret==='error'){
              alert("请稍后重试"); }
            else{
              window.location.href="./user_AIqa/"+form1;
            }
          })
       });
});

//$.post('/userlogin',data={'tt1':114514,'tt2':114511},function(ret){
//
//            if(ret==='tryagain'){
//              alert("密码错误请重新输入");}
//            else if(ret==='error'){
//              alert("请稍后重试"); }
//            else{
//              window.location.href="./user_history/"+form1;
//            }
//          });