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

function userAIqa(){
    var myurl=location.href;
    myurl=myurl.split("/");
    var message11=document.getElementById("chat_context_item");
    var form1=message11.value;
    $.post('/user_AIqa/'+myurl[4],data={'tt1':myurl[4],'tt2':form1},function(ret){
       alert("WTF????");
    });
}

function sendDocName(input){
    var userInputText = document.getElementById("chat_context_item");
    userInputText.value = input.innerHTML;
}

function buttonLis(){
    // 成功发送
    var send_message=document.getElementById("chat_middle_item");  //获取框内信息
    var domBtm=document.getElementById("button");   //点击按钮

    // 发送内容
    var message=document.getElementById("chat_context_item");
    //userAIqa();
    var str=message.value;
    
    var date=new Date();  //时间
    var hour=date.getHours();
    var mm=date.getMinutes();
    var time=hour+':'+mm;
            
    var ans='<div class="chat_right_item_1 clearfix">用户</div>'+
        '<div class="chat_right_item_2">'+
            '<div class="chat_right_time clearfix">'+time+'</div>'+
            '<div class="chat_right_content clearfix">'+str+'</div>'+
            '</div>';
    var oLi=document.createElement("div");
    oLi.setAttribute("class","chat_right");
    oLi.innerHTML=ans;
    send_message.append(oLi);
    message.value="";

    var myurl=location.href;
    myurl=myurl.split("/");

    var did = document.getElementsByName(str)[0].id

    $.post('/user_docqa/'+myurl[4],data={"uid":myurl[4],"did":did,"msg":"WDNMD"},function(res){
        console.log(res);
    })
}