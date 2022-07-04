$(function(){


        var form5 = document.getElementById ('form5');//获取select下拉列表
        for ( var i = 10; i < 110; i++)//循环添加当前年份的每个年份依次添加到下拉列表
        {
           var option = document.createElement ('option');
           option.value = i;
           var txt = document.createTextNode (i);
           option.appendChild (txt);
           form5.appendChild (option);
        }
});


function checkpassword() {
        var password = document.getElementById("form3").value;
        var repassword = document.getElementById("form4").value;

        if(password == repassword) {
           document.getElementById("tishi").innerHTML="<font color='green'>两次密码输入一致</font>";


       }else{
         document.getElementById("tishi").innerHTML="<font color='red'>两次输入密码不一致!</font>";

       }
}



$(function() {
   $("#form6").on('click',function(){

       var form1 = $("#form1").val();

       var form2 = $("#form2").val();
       var form3 = $("#form3").val();
       var form4 = $("#form4").val();

       var form5 = $("#form45").val();
//       alert(form5)
       var form6 = $("#form5").val();


       if(form1.length!=11) {
         alert("注册失败，请正确填写11位手机号");
          return false
       }
       if(form2.length<3 || form2.length>10){
         alert("注册失败,昵称最长10个字符");
          return false
       }
       if(form3!=form4) {
         alert("注册失败，两次密码不一致");
          return false
       }
       if(form3.length<6 || form3.length>16){
         alert("注册失败,密码长度需6-16位");
          return false
       }
       if(form4.length<6 || form4.length>16){
         alert("注册失败,密码长度需6-16位");
          return false
       }

        $.post('/user_register',data={'tt1':form1,'tt2':form2,'tt3':form3,'tt5':form5,'tt6':form6},function(ret){
           if(ret==='wait'){
            alert("请稍后重试");}
           else if(ret==='already'){
            alert("用户已存在"); }
           else{
           alert("前去登录")
//                 var second = confirm("注册成功立即登录");
//                 if(second){
//                      window.location.replace("./hello.html")}
//                 else{
//                       alert("留在此页"); }
           }
        })
   });

});


function herfChange0(){
    var myurl=location.href;
    myurl=myurl.split("/");

   window.location.href="../user_AIqa/"+myurl[4];
}

function herfChange1(){
    var myurl=location.href;
    myurl=myurl.split("/");

   window.location.href="../user_docqa/"+myurl[4];
}

function herfChange2(){
    var myurl=location.href;
    myurl=myurl.split("/");
   window.location.href="../user_infochange/"+myurl[4];
}
function herfChange3(){
    var myurl=location.href;
    myurl=myurl.split("/");
   window.location.href="../user_history/"+myurl[4];
}

function herfChange4(){
    var myurl=location.href;
    myurl=myurl.split("/");
   window.location.href="../user_comment/"+myurl[4];
}
