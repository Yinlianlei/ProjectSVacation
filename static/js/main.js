            var recorder;
            var audio = document.querySelector('audio');  
              
            function startRecording() {  
               if(recorder){
                   recorder.start();
                   return;
               }
               
                HZRecorder.get(function (rec) {  
                    recorder = rec;  
                    recorder.start();  
                },{error:showError});  
            }  
              
              
            function obtainRecord(){



                 if(!recorder){
                    showError("请先录音");
                    return;
                }
               var record = recorder.getBlob();
               if(record.duration!==0){

               downloadRecord(record.blob);
               }else{
                   showError("请先录音")
               }
            };  

            function downloadRecord(record){
//               alert(record)
            var form=new FormData();
            form.append("upfile",record,"recorder.mp3"); //和普通form表单并无二致，后端接收到upfile参数的文件，文件名为recorder.mp3

            //直接用ajax上传
            var xhr=new XMLHttpRequest();
            xhr.open("POST","/get_speech");//这个假地址在控制台network中能看到请求数据和格式，请求结果无关紧要


            xhr.onreadystatechange=function(){
                if(xhr.readyState==4){

//                     alert(xhr.responseText);

                     var speechtext=document.getElementById('chat_context_item');
                     speechtext.value=speechtext.value+xhr.responseText;
//                     audioData.buffer=[];
//                     startRecording();
//                     recorder.clear();
//                     stopRecord();

//                    alert(xhr.status==200?"上传成功":"测试请先打开浏览器控制台，然后重新录音，在network选项卡里面就能看到上传请求数据和格式了");
                }
            }
            xhr.send(form);


//            var speechtext=document.getElementById('chat_context_item');
//            speechtext=s


//              var save_link = document.createElementNS('http://www.w3.org/1999/xhtml', 'a')
//                save_link.href = URL.createObjectURL(record);
//
//                save_link.download = "needvoice";
//                fake_click(save_link);
            }

       
            function fake_click(obj) {
            var ev = document.createEvent('MouseEvents');
            ev.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            obj.dispatchEvent(ev);
            }

                 function getStr(){
              var now=new Date;
              var str= now.toDateString();
            }
            function clearRecord(){
                recorder&&recorder.clear();
            };

            function stopRecord(){
                recorder&&recorder.stop();  
            };  
            var msg={};
            //发送音频片段
            var msgId=1;
            function send(){
                if(!recorder){
                    showError("请先录音");
                    return;
                }

               var data=recorder.getBlob();
               if(data.duration==0){
                     showError("请先录音");
                    return;
               }
                msg[msgId]=data;
                recorder.clear();
                console.log(data);
                var dur=data.duration/10;
                 var str="<div class='warper'><div id="+msgId+" class='voiceItem'>"+dur+"s</div></div>"
                $(".messages").append(str);
                msgId++;
            }
            
            $(document).on("click",".voiceItem",function(){
                var id=$(this)[0].id;
                var data=msg[id];
                playRecord(data.blob);
            })

            var ct;
            function showError(msg){
                $(".error").html(msg);
                clearTimeout(ct);
                ct=setTimeout(function() {
                    $(".error").html("")
                }, 3000);
            }


            function playRecord(blob){  
                if(!recorder){
                    showError("请先录音");
                    return;
                }
                 recorder.play(audio,blob);  
            };  
              
            /* 视频 */  
            function scamera() {  
                var videoElement = document.getElementById('video1');  
                var canvasObj = document.getElementById('canvas1');  
                var context1 = canvasObj.getContext('2d');  
                context1.fillStyle = "#ffffff";  
                context1.fillRect(0, 0, 320, 240);  
                context1.drawImage(videoElement, 0, 0, 320, 240);  
            };  
              
            function playVideo(){  
                var videoElement1 = document.getElementById('video1');  
                var videoElement2 = document.getElementById('video2');  
                videoElement2.setAttribute("src", videoElement1);  
            };  