
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




//$(function() {
//       $("#fankuibt").on('click',function(){
//          var form1 = $("#comment_score1").val();
//          alert("111");
//          alert(form1);
//          var form2 = $("#comment_content").val();
//          alert(form2);
//          $.post('/userlogin',data={'tt1':form1,'tt2':form2},function(ret){
//
//            if(ret==='tryagain'){
//              alert("密码错误请重新输入");}
//            else if(ret==='error'){
//              alert("请稍后重试"); }
//            else{
//              window.location.href="./user_history/"+form1;
//            }
//          })
//       });
//});