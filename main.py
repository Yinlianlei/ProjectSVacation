from flask import Flask, redirect, url_for, request,render_template,make_response
from sqlconn import *
from chat import ChatBotGraph
from echarts import selectDisease,initNeo
from sqlconn import *
from asr_json import *
# for chat
from flask_socketio import SocketIO,emit,join_room,leave_room

app = Flask(__name__)
socketio = SocketIO(app)

client_query = []
# the user and the doctor list
doctorSelectByUser = {}

handler = None
initNeo()


name_space = '/websocket'
# emit('my_response_message', broadcasted_data, broadcast=True, namespace=name_space)  #对name_space下的所有客户端发送消息

@socketio.on('connect', namespace=name_space)# 有客户端连接会触发该函数
def on_connect():
    # 建立连接 sid:连接对象ID
    client_id = request.sid
    client_query.append(client_id)
    # emit(event_name, broadcasted_data, broadcast=False, namespace=name_space, room=client_id)  #指定一个客户端发送消息
    # emit(event_name, broadcasted_data, broadcast=True, namespace=name_space)  #对name_space下的所有客户端发送消息
    print('有新连接,id=%s接加入, 当前连接数%d' % (client_id, len(client_query)))
    emit('connect', str(client_id), broadcast=False, namespace=name_space, room=client_id)

@socketio.on('disconnect', namespace=name_space)# 有客户端断开WebSocket会触发该函数
def on_disconnect():
    # 连接对象关闭 删除对象ID
    client_query.remove(request.sid)
    print('有连接,id=%s接退出, 当前连接数%d' % (request.sid, len(client_query)))

# on('消息订阅对象', '命名空间区分')
# 对信息进行分类处理
@socketio.on('message', namespace=name_space)
def on_message(message):
   """ 服务端接收消息 """
   message = eval(message)
   print('从id=%s客户端中收到消息，内容如下:' % request.sid)
   #print(message['msg'])
   #print(message['type'])
   client_id = message['room']

   #print(client_id)

   if message['type'] == 'user_c':
      userQuestionAdd(client_id,message['userId'],message['docId'])
      emit('my_response_message', message['msg'], broadcast=False, namespace=name_space, room=client_id)  #指定一个客户端发送消息
   elif message['type'] == 'user_q':
      emit('my_response_message', message['msg'], broadcast=False, namespace=name_space, room=client_id)  #指定一个客户端发送消息
   elif message['type'] == 'doctor_a':
      print(message['msg'])
      emit('my_response_message', message['msg'], broadcast=False, namespace=name_space, room=client_id)  #指定一个客户端发送消息
   
@socketio.on('doc_room', namespace=name_space)
def on_roomMessage(message):
   message = eval(message)
   client_id = message['userRoom']
   emit("doc_room",message['docRoom'], namespace=name_space, room=client_id)





@app.route('/user_graph/',methods=['POST', 'GET'])
def graph():
   navList = [
      {"name":'医药问答',"url":"/user_AIqa/"},
      {"name":'线上问诊',"url":"/user_docqa/"},
      {"name":'信息修改',"url":"/user_infochange/"},
      {"name":'我的收藏',"url":"/user_history/"},
      {"name":'意见反馈',"url":"/user_comment/"},
      {"name":'知识图谱',"url":"/user_graph/"}
   ]

   grap = selectDisease("")
   
   return make_response(render_template('user_graph.html', navList = navList,grap=grap))


#打开医生问答
@app.route('/user_docqa/<userid>',methods = ['POST', 'GET'])
def useraskdoc(userid):
   responseText = ""
   if request.method == 'GET':
      docList = getOnlineDoctor()
      responseText = docList
   if request.method == 'POST':
      print(request.form.get("msg"))
      return request.form
   
   return render_template('user_doctorqa.html',responseText=responseText)

#医生登录后打开问诊问答主网页
@app.route('/doctor_userqa/<userid>',methods = ['POST', 'GET'])
def doctouserqa(userid):
   docLogin(userid)
   if request.method == 'GET':
      responseText = docGetUserList(userid)
   if request.method == 'POST':
      pass
   
   return render_template('doctor_userqa.html',responseText=responseText)








#默认页面
@app.route('/')
def index():
    """
    默认为用户登录
    :return:
    用户登录页面
    """
    global handler
    if not isinstance(handler,ChatBotGraph):
         handler = ChatBotGraph()
    return render_template("user_log.html")     #render_template("index.html")#,tlist=result)



#用户登录
@app.route('/userlogin',methods = ['POST', 'GET'])
def userlogin():
   if request.method == 'POST':
      user_pnum = request.form.get('tt1')
      user_pwd = request.form.get('tt2')
      res=userlog(user_pnum, user_pwd)
      if res=='well':
         return res
         # return redirect(url_for("usermain",userid=str(user_pnum)))
      elif res==None:
         data = "error"
         return data
      else:
         data="tryagain"
         return data


#登录后打开用户AI问答主网页
@app.route('/user_AIqa/<userid>',methods = ['POST', 'GET'])
def usertoaiqa(userid):
   if request.method == 'GET':

      return render_template('user_AIqa.html')
   if request.method == 'POST':
      global handler
      user_id = request.form.get('tt1')
      user_text = request.form.get('tt2')
      res=texttomysql(user_id, user_text)

      res = handler.chat_main(user_text)

      #todo 和king对接
      #todo 第四张词云图
      #todo 用户导航栏
      #todo 医生问答的逻辑

      return res

   # if request.method == 'POST':
   #    print('hhh')

#打开用户收藏
@app.route('/user_history/<userid>',methods = ['POST', 'GET'])
def userhistory(userid):
   if request.method == 'GET':
      res=gethistmysql(userid)

      return render_template('user_history.html',user_history0=res[0]
                             ,user_history1=res[1],user_history2=res[2]
                             ,user_history3=res[3],user_history4=res[4])
   # if request.method == 'POST':
   #    print('hhh')

#意见反馈
@app.route('/user_comment/<userid>',methods = ['POST', 'GET'])
def usercomment(userid):
   if request.method == 'GET':
      return render_template('user_comment.html')
   if request.method == 'POST':
      comment_score = request.form.get('tt1')
      comment_content = request.form.get('tt2')
      res = commentmysql(comment_score, comment_content)
      if res=='well':
         data = "well"
      else:
         data="wait"
      return data


#打开信息修改
@app.route('/user_infochange/<userid>',methods = ['POST', 'GET'])
def userchangeinfo(userid):
   if request.method == 'GET':


      return render_template('user_info_modification.html')
   # if request.method == 'POST':
   #    print('hhh')


#用户注册
@app.route('/user_register',methods = ['POST', 'GET'])
def regis():
   # if request.method == 'GET':
   #    return render_template('register.html')
   if request.method == 'POST':
      user_pnum = request.form.get('tt1')
      user_name=request.form.get('tt2')
      user_psd = request.form.get('tt3')
      user_sex = request.form.get('tt5')
      user_age=request.form.get('tt6')
      res=regimysql(user_pnum, user_sex, user_age, user_name, user_psd)

      if res=='well':
         data = "well"
      elif res==None:
         data = "already"
      else:
         data="wait"
      return data


#管理员登录
@app.route('/adminlogin',methods = ['POST', 'GET'])
def admin_login():
   if request.method=='GET':
      return render_template("admin_log.html")

   if request.method == 'POST':
      user_id = request.form.get('tt1')
      user_pwd = request.form.get('tt2')
      res=adminlog(user_id,user_pwd)
      if res=='well':
         return res
         # return redirect(url_for("usermain",userid=str(user_pnum)))
      elif res==None:
         data = "error"
         return data
      else:
         data="tryagain"
         return data

#管理员登录成功打开用户管理界面
@app.route('/admin_users',methods = ['POST', 'GET'])
def adminUser():
   if request.method=='GET':
      return render_template("admin_users.html")


@app.route('/admin_feedback',methods = ['POST', 'GET'])
def adminFeedback():
   if request.method=='GET':
      res=round(getavgscore()*20,2)
      res1=getfeedkback()
      return render_template('admin_feedback.html', avg_score=res,userfb1=res1[0],
                 userfb2=res1[1],userfb3=res1[2],userfb4=res1[3],userfb5=res1[4])


@app.route('/admin_doctors',methods = ['POST', 'GET'])
def adminDoctors():
   if request.method=='GET':
      return render_template("admin_doctors.html")
   if request.method=='POST':
      doctor_id = request.form.get('tt1')
      res=admingetdoctor(doctor_id)
      return res





@app.route('/get_userdata',methods = ['POST', 'GET'])
def userData():
   if request.method=='GET':
      return render_template("admin_doctors.html")
   if request.method=='POST':
      # 性别数据
      data=getUserData()
      # 年龄数据
      data1=getUserData1()
      # 省份数据
      data2=getUserData2()
      # 热搜数据
      data3 = getUserData3()
      data=data+','+data1+','+data2+','+data3
      return data





#医生登录
@app.route('/doclogin',methods = ['POST', 'GET'])
def doc_login():
   if request.method=='GET':
      return render_template("doctor_log.html")

   if request.method == 'POST':
      user_id = request.form.get('tt1')
      user_pwd = request.form.get('tt2')
      res=doclog(user_id,user_pwd)
      if res=='well':
         return res
         # return redirect(url_for("usermain",userid=str(user_pnum)))
      elif res==None:
         data = "error"
         return data
      else:
         data="tryagain"
         return data

#打开医生信息修改网页
@app.route('/doctor_infochange/<userid>',methods = ['POST', 'GET'])
def docinfochange(userid):
   if request.method == 'GET':

      return render_template('doctor_info_modification.html')

#打开医生坐诊统计网页
@app.route('/doctor_Staqa/<userid>',methods = ['POST', 'GET'])
def docqasta(userid):
   if request.method == 'GET':

      return render_template('doctor_staqa.html')



@app.route('/doctorregister.html',methods = ['POST', 'GET'])
def regisdoc():
   if request.method == 'GET':
      return render_template('doctorregister.html')
   if request.method == 'POST':
      doctor_pnum = request.form.get('tt1')
      doctor_name=request.form.get('tt2')
      doctor_psd = request.form.get('tt3')
      doctor_age = request.form.get('tt5')
      doctor_field=request.form.get('tt6')
      doctor_level = request.form.get('tt7')
      doctor_worktime = request.form.get('tt8')
      res=regidocmysql(doctor_pnum, doctor_age, doctor_name, doctor_psd, doctor_field, doctor_level, doctor_worktime)
      # res=regimysql(user_pnum, user_sex, user_age, user_name, user_psd)

      if res=='well':
         data = "well"
      elif res==None:
         data = "already"
      else:
         data="wait"
      return data

#接收录音
@app.route('/get_speech',methods = ['POST', 'GET'])
def speechget():
   if request.method == 'GET':

      return render_template('doctor_staqa.html')
   if request.method == 'POST':
      speech=request.files['upfile']
      # speech = request.form.get('upfile')
      # speech=speech.encode("utf-8")
      # print(type(speech))
      pdf_byte = speech.stream.read()
      # print(type(pdf_byte))
      # print(pdf_byte)
      res=speechresult(pdf_byte)
      # print(speech)
      return res


# @app.route('/hello.html', methods=['GET', 'POST'])
# def hello_world():
#       if request.method == 'GET':
#          # args = request.args
#          # name = args.get('name')
#          # return render_template('hello.html', name=name)
#          return render_template('hello.html')
#
#       if request.method == "POST":
#          print("POST请求")
#          arges = request.form.get("tt1")
#          print(arges)
#          return "PPP"



   # else:
   #    user_id = request.args.get('tt1')
   #    user_pwd = str(request.args.get('tt2'))
   #    myresult='hhhhhh'
   #    if user_pwd == '12345':
   #       myresult='welcome '+ user_id
   #    return render_template("loginsuccess.html",ttt=myresult)



if __name__ == '__main__':
   socketio.run(app, host='127.0.0.1', port=5000, debug=False)
   #app.run(debug = True)