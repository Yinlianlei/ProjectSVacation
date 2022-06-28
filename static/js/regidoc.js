$(function(){

<!--        var year=new Date().getFullYear(); //获取当前年份-->
        var form5 = document.getElementById ('form5');//获取select下拉列表
        for ( var i = 10; i < 110; i++)//循环添加当前年份的每个年份依次添加到下拉列表
        {
           var option = document.createElement ('option');
           option.value = i;
           var txt = document.createTextNode (i);
           option.appendChild (txt);
           form5.appendChild (option);
        }

        var form5 = document.getElementById ('form8');//获取select下拉列表
        for ( var i = 1; i < 100; i++)//循环添加当前年份的每个年份依次添加到下拉列表
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
           document.getElementById("tishi").innerHTML="<br><font color='green'>两次密码输入一致</font>";
<!--           document.getElementById("submit").disabled = false;-->

       }else{
         document.getElementById("tishi").innerHTML="<br><font color='red'>两次输入密码不一致!</font>";
<!--           document.getElementById("submit").disabled = true;-->
       }
       }

      $(function() {
      $("#form9").on('click',function(){
       var form1 = $("#form1").val();
       var form2 = $("#form2").val();
       var form3 = $("#form3").val();
       var form4 = $("#form4").val();
       var form5 = $("#form5").val();
       var form6 = $("#form6").val();
       var form7 = $("#form7").val();
       var form8 = $("#form8").val();
<!--       var form5 = $("#man");-->
       if(form5.checked){
       form5 = 1;
       }
       else{
       form5 = 0;
       }

       if(form1.length!=11) {
         alert("注册失败，请正确填写11位手机号");
          return false
       }
       if(form2.length<2 || form2.length>4){
         alert("注册失败,名字最长4个字符");
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
       if(form6.length<2 || form6.length>16){
         alert("注册失败,擅长领域最长16个字符");
          return false
       }
       if(form7.length<2 || form7.length>16){
         alert("注册失败,医生职称最长16个字符");
          return false
       }

        $.post('./doctorregister.html',data={'tt1':form1,'tt2':form2,'tt3':form3,'tt5':form5,'tt6':form6,'tt7':form7,'tt8':form8},function(ret){
           if(ret==='wait'){
            alert("请稍后重试");}
           else if(ret==='already'){
            alert("用户已存在"); }
           else{

                 var second = confirm("注册成功立即登录");
                 if(second){
                      window.location.replace("./hello.html")
                  }
                  else{
                       alert("留在此页");
                  }
              }
                  })
       });
   });
