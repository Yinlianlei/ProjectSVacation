windw_socket=null
userRoom = null
docRoom = null
userId = null
docId = null

function flush2(){
    
}

function flush(){
    window.location.reload();
}

function herfChange1(){
    var myurl=location.href;
    myurl=myurl.split("/");

   window.location.href="../doctor_userqa/"+myurl[4];
}

function herfChange2(){
    var myurl=location.href;
    myurl=myurl.split("/");
   window.location.href="../doctor_Staqa/"+myurl[4];
}
function herfChange3(){
    var myurl=location.href;
    myurl=myurl.split("/");
   window.location.href="../doctor_infochange/"+myurl[4];
}
function selectUserName(input){
    var target = document.getElementById(input.name+"_room");
    var targetRoom = target.innerText;
    userRoom = targetRoom
    if(windw_socket!=null){
        //room == UserRoomNum
        send_room();
        docId = input.id
        userId = input.name
        windw_socket.emit('message', '{"sourceRoom":\"'+docRoom+'\","room":\"'+docRoom+'\","type":"doctor_a","userId":\"'+input.name+'\","docId":\"'+input.id+'\","msg":"meesage send!"}');
        windw_socket.emit('message', '{"sourceRoom":\"'+docRoom+'\","room":\"'+targetRoom+'\","type":"doctor_a","userId":\"'+input.name+'\","docId":\"'+input.id+'\","msg":"Dc.Yin had join this room"}');
    }else{
        console.log("NULL!")
    }
}

function send_room(){
    if(windw_socket!=null){
        windw_socket.emit("doc_room",'{"docRoom":\"'+docRoom+'\","userRoom":\"'+userRoom+'\"}');
    }
}

function send_msg(msg){
    if(windw_socket!=null){
        windw_socket.emit('message', '{"sourceRoom":\"'+docRoom+'\","room":\"'+userRoom+'\","type":"doctor_a","userId":\"'+userId+'\","docId":\"'+docId+'\","msg":\"'+msg+'\"}');
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
            
    var ans='<div class="chat_right_item_1 clearfix">Doctor</div>'+
            '<div class="chat_right_item_2">'+
            '<div class="chat_right_time clearfix">'+time+'</div>'+
            '<div class="chat_right_content clearfix">'+str+'</div>'+
            '</div>';
    var oLi=document.createElement("div");
    oLi.setAttribute("class","chat_right");
    oLi.innerHTML=ans;
    send_message.append(oLi);
    message.value="";

    send_msg(str);
}

function dc(){
	namespace = '/websocket';
	var websocket_url = location.protocol+'//' + document.domain + ':' + location.port + namespace;
	var socket=io.connect(websocket_url);
	// socket.emit('connect2', {'param':'value'});	//发送消息
	// socket.close()room
	socket.on('connect',function(data){
		//console.log('connecte:'+data);
        docRoom = data;
		//alert("建立连接成功")
		windw_socket=socket
	});

	socket.on('disconnect',function(data){
		//alert("连接已断开")
		//console.log('disconnecte:'+data);
        if(windw_socket!=null){
            windw_socket.emit('message', '{"sourceRoom":\"'+docRoom+'\","room":\"'+userRoom+'\","type":"doctor_a","userId":\"'+userId+'\","docId":\"'+docId+'\","msg":\"window has close\"}');
        }
	});

    //监听返回值
	socket.on('my_response_message',function(data){
        var send_message=document.getElementById("chat_middle_item");  //获取框内信息
		//console.log('my_response_message:'+data);
		//alert("收到服务端的回复:"+data)
        
        var txt =   "<div class=\"chat_left clearfix\">"+
                        "<div class=\"chat_left_item_1\">User</div>"+
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

    socket.on("command",function(data){
        if(data == "flush"){
            setTimeout(function(){
                windw_socket.emit('message', '{"sourceRoom":\"'+docRoom+'\","room":\"'+docRoom+'\","type":"doctor_a","userId":\"'+input.name+'\","docId":\"'+input.id+'\","msg":"三秒后刷新"}');
                clos_con()
                flush()
            },3000);
        }
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