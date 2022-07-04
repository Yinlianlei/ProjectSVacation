from flask import Flask,render_template,make_response,request
from wsgiref.simple_server import make_server
import MySQLdb as sql
from py2neo import Graph
from pyecharts.charts import Graph as Graph2
from pyecharts import options as opts
import pandas as pd
import json
import numpy as np
import os
import re
import jieba

# declear and init mysql
db = ""
neo = ""

# 导航栏全局变量
navList = {"home":"/","login":"/login"}

# symptom
symptom = []
disease = []

def initSql():
    with open("./static/sql.json","r") as f:
        try:
            data = json.load(f)
            global db 
            global neo
            db = sql.connect(data["mysql"]['host'],
                            data["mysql"]['user'],
                            data["mysql"]['password'],
                            data["mysql"]['table'],
                            charset='utf8')
        except Exception as e:
            print(e.with_traceback())

def initNeo():
    with open("./static/sql.json","r") as f:
        try:
            data = json.load(f)
            global neo
            # new version of py2neo
            neo = Graph("http://localhost:7474", auth=(
                        data["neo4j"]['user'],
                        data["neo4j"]['password']))
        except Exception as e:
            print(e)

def initSymptom():
    global symptom
    global disease
    with open("./dict/symptom.txt") as f:
        a = f.readlines()
        for i in a:
            symptom.append(str(i).split('\n')[0])
    symptom = np.array(symptom)
    with open("./dict/disease.txt") as f:
        a = f.readlines()
        for i in a:
            disease.append(str(i).split('\n')[0])
    disease = np.array(disease)

# execute sql
def command4mysql():
    #txt = "insert into userinfo values(1,114514,0,8,'bobo','114514','hn')"
    txt = "select * from userinfo"
    global db
    cursor = db.cursor()
    try:
        for i in txt.split(';'):
            # 执行sql语句
            cursor.execute(i)
            print(cursor.fetchall())
            # 提交到数据库执行
            db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        print(i)
        db.rollback()

def execute4mysql(command):
    try:
        global db
        cursor = db.cursor()
        for i in command.split(';'):
            # 执行sql语句
            cursor.execute(i)
            method = i.split(' ')[0].lower()
            if method == "select":
                for j in cursor.fetchall():
                    print(j)
            # 提交到数据库执行
            db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        print(i)
        db.rollback()

# get info from symptom
#input: info of disease
#return: list[]
def getDiseaseFromSymptom(symptom):
    global neo
    txt = "MATCH (n:Symptom)-[r]-(m:Disease) WHERE n.name = "
    if len(symptom) == 0:
        return
    elif isinstance(symptom,str):
        txt += "\"" + symptom + "\""
    else:
        txt += "\"" + symptom[0] + "\""
        for i in symptom[1:]:
            txt += " AND n.name = \"" + i + "\""

    txt += " RETURN m LIMIT 250"

    data = neo.run(txt).to_data_frame()

    dataDict = []
    if len(data) == 0:
        return dataDict

    for i in data['m']:
        dataDict.append(dict(i)['name'])

    return dataDict

# get disease
# input: symptom of disease
# return: dict(information of Dosease)
def getInfoOfDisease(Disease):
    global neo
    data = neo.run("MATCH (n)-[r]-(m:Disease{name:\""+Disease+"\"}) RETURN n,r LIMIT 250").to_data_frame()
    dataDict = {}
    #print(data)
    for i in range(len(data['n'])):
        dataDict[dict(data.iloc[i,0])['name']] = dict(data.iloc[i,1])['name']

    return dataDict

def process4echarts(root,data):
    category = ["病症"]
    for i in data:
        if data[i] not in category:
            category.append(data[i])
    rootNode = {"name":root , "symbolSize": 30,"category":0}
    nodes = [{"name":i,"symbolSize": 30,"category":category.index(data[i])} for i in data]

    category = [{"name":i} for i in category]

    nodes.insert(0,rootNode)
    links = [
        {"source": root, "target": i,"value":data[i]} for i in data
    ]

    c = (
        Graph2()
        .add("", nodes, links,category, repulsion=8000,
            #linestyle_opts=opts.LineStyleOpts(color="red"),
            label_opts=opts.LabelOpts(position="right"),
            edge_label=opts.LabelOpts(
                is_show=True, position="middle", formatter="{c}"
            )
            
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=root+"-知识图谱"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"))
    )
    c.width = "600px"
    c.height = "600px"
    return c.render_embed()


# function for login
def mysql4login(phone,pwd):
    try:
        global db
        cursor = db.cursor()
        # 执行sql语句
        command = "select user_pnum,user_psd from userinfo where user_pnum = "+phone+" and user_psd = "+pwd+";"
        cursor.execute(command)
        re = cursor.fetchall()
        if(len(re) != 1):
            return -1
        print(re[0])
        # 提交到数据库执行
        db.commit()
        return 0
    except Exception as e:
        # 如果发生错误则回滚
        print(e)
        db.rollback()

# load dict for jieba
def cutLoad():
    for i,j,k in os.walk('./dict/'):
        for l in k:
            jieba.load_userdict("./dict/"+l)

# use cut
def cutString(input):
    result = jieba.lcut_for_search(input)
    return result

#for page   
app = Flask(__name__)

@app.route('/')
def index():
    # html response success, maybe need a 404 page
    response = make_response(render_template('index.html', name="test index"))

    # set headers
    #response.headers['user_type'] = 'doctor'
    #response.headers['user_id'] = '114514'

    # set cookie    cookieId value path
    response.set_cookie("user_type","doctor",path="/test/")
    response.set_cookie("user_id","114514")


    return response     #render_template("index.html")#,tlist=result)

#GET
@app.route('/login/',methods=['GET','POST'])
def test():
    response = make_response(render_template('login.html', name="test post"))
    return response

#POST from register
@app.route('/response/',methods=['POST'])
def response():
    res = ""
    if request.method == 'POST':
        phone = request.form['user']
        pwd = request.form['password']
        if mysql4login(phone,pwd) == 0:
            res = "login success"
        else:
            res = "login failed"

    response = make_response(render_template('response.html', name="test response",res=res))
    
    return response

# Question & answer
@app.route('/consult',methods=['POST','GET'])
def consult():
    global navList
    res = ""
    if request.method == 'POST':
        print(request.form['question_text'])
    if request.method == 'GET':
        pass

    response = make_response(render_template('consult.html', name="test consult",res=res,doctor="1.png",navList = navList))
    # 设置响应头

@app.route('/AI',methods=['POST','GET'])
def AI():
    global navList,symptom,disease

    res = []
    sym = []#存储病症
    dis = []#存储病
    data = ""
    ree = ""
    result = "waiting....."
    # 等待分词处理
    if request.method == 'POST':
        result = request.form['AI_question']
        result = cutString(result)
        for i in result:
            for j in disease:
                temp = re.findall("{0}+".format(i),j)
                if temp != []:
                    dis.append(temp)
            for j in symptom:
                temp = re.findall("{0}+".format(i),j)
                if temp != []:
                    dis.append(temp)

        print(len(dis),len(sym))

        # Disease
        if len(dis) == 1:
            data = getInfoOfDisease(dis[0])
            ree = process4echarts(dis[0],data)
        elif len(dis) > 1:
            result = dis

        # Symptom
        if len(sym) == 1:
            sym = getDiseaseFromSymptom(sym)
        elif len(sym) > 1:
            dis = getDiseaseFromSymptom(sym)
            if len(dis) == 0:
                tempList = []
                for i in sym:
                    temp = getDiseaseFromSymptom(i)
                    print(temp)
                    tempList.append(temp)
                dis = tempList


    if request.method == 'GET':
        pass

    

    response = make_response(render_template('AI.html', 
                                        name="test consult",
                                        res=res,
                                        doctor="1.png",
                                        navList = navList,
                                        result=result,
                                        sym=sym,
                                        dis=dis,
                                        ree=ree)
                            )

    return response


'''
# template for page
@app.route('/',methods=['POST','GET'])
def test():
    global navList
    res = ""
    # html的响应方式，POST和GET，此处大写html必须大写
    # 具体参数获取方式看request
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass

    response = make_response(render_template('文件.html',navList = navList,name="test for template"))#后面接上传递给html的变量 #name="test consult",res=res,doctor="1.png"))
    
    response.

    return response
'''


if __name__ == "__main__":
    #initSql()
    initNeo()
    initSymptom()

    #data = getInfoOfDisease("减压病")
    #print(data)
    #data = getDiseaseFromSymptom("瘙痒")
    #print(data)

    #data = getDiseaseFromSymptom('低烧')
    #print(data)

    server = make_server('127.0.0.1', 5000, app)
    server.serve_forever()
    app.debug = True
    app.run()


    
    #cutLoad()
    #command4neo()
    #processJson()
    #processNodes()
    #command4mysql()
    #test4neo()

    #execute4mysql("select * from userinfo")

    
    

'''
# test for mysql select from sql
def testSql():
    global db
    cursor = db.cursor()
    cursor.execute("show tables;")
    result = cursor.fetchall()
    
    for i in result:
        print(i)

'''