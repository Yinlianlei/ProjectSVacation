windw_socket=null
room = null
userRoom = null
docId = null

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

function selectDoc(input){
    docId = input.id

    var myurl=location.href;
    myurl=myurl.split("/");

    if(windw_socket!=null){
        windw_socket.emit('message', '{"sourceRoom":"","room":\"'+userRoom+'\","type":"user_c","userId":\"'+myurl[4]+'\","docId":\"'+docId+'\","msg":"waiting"}');
    }
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

// send msg
function send_msg(userId,docId,msg){
    if(windw_socket!=null){
        //room = docRoomNum
        //console.log(room)
        windw_socket.emit('message', '{"sourceRoom":\"'+userRoom+'\","room":\"'+room+'\","type":"user_q","userId":\"'+userId+'\","docId":\"'+docId+'\","msg":\"'+msg+'\"}');
    }
}


function buttonLis(){
    // 成功发送
    var send_message=document.getElementById("chat_middle_item");  //获取框内信息
    //var domBtm=document.getElementById("button");   //点击按钮

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

    send_msg(myurl[4],docId.id,str);
}


function ws(){
	namespace = '/websocket';
	var websocket_url = location.protocol+'//' + document.domain + ':' + location.port + namespace;
	var socket=io.connect(websocket_url);
	// socket.emit('connect2', {'param':'value'});	//发送消息
	// socket.close()
	socket.on('connect',function(data){
		console.log('connecte:'+data);
        userRoom = data;
		//alert("建立连接成功")
		windw_socket=socket
	});
	socket.on('disconnect',function(data){
		//alert("连接已断开")
		console.log('disconnecte:'+data);
	});

    //监听返回值
	socket.on('my_response_message',function(data){
        var send_message=document.getElementById("chat_middle_item");  //获取框内信息
		console.log('my_response_message:'+data);
		//alert("收到服务端的回复:"+data)
        
        var txt =   "<div class=\"chat_left clearfix\">"+
                        "<div class=\"chat_left_item_1\">Doctor</div>"+
                        "<div class=\"chat_left_item_2\">"+
                            "<div class=\"chat_left_content\">"+
                                data
                            "</div>"+
                        "</div>"+
                    "</div>"

        var oLi=document.createElement("div");
        oLi.setAttribute("class","chat_left");
        oLi.innerHTML=txt;
        send_message.append(oLi);
	});

    socket.on("doc_room",function(data){
        console.log("docRoom:",data);
        room = data;
    })
}

function clos_con(){
    if(windw_socket!=null){
        windw_socket.close()
    }
}

window.onbeforeunload= function(event) {
    if (windw_socket!=null && !windw_socket.closed){
    	// confirm(windw_socket.closed)
    	windw_socket.close()
    }
}

window.onunload= function(event) {
    if (windw_socket!=null && !windw_socket.closed){
    	//confirm(windw_socket.closed)
    	windw_socket.close()
    }
}

