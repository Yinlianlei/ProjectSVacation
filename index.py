from crypt import methods
from flask import Flask,render_template,make_response,request
from wsgiref.simple_server import make_server
import MySQLdb as sql
from py2neo import Graph,Node,Relationship,Subgraph
import json
import numpy as np

from sqlalchemy import null

# declear and init mysql
db = null
neo = null

# 导航栏全局变量
navList = {"home":"/","login":"/login"}

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
            print(e.with_traceback())

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

def test4neo():
    #node1 = Node("Person",name="test1")
    #node2 = Node("Person",name="test2")
    #r = Relationship(node1,"wifi",node2)
    #neo.create(r)
    global neo
    # node
    # data = neo.run("MATCH (n) RETURN n LIMIT 25").to_table()
    # relationship
    data = neo.run("MATCH ()-[r]->() RETURN r LIMIT 20").data()
    print(data)
    
#create nodes.json
def processJson():
    with open('./static/medical.json','r') as f:
        testList = []
        try:
            for i in f.readlines():
                txt = json.loads(i)
                txt = txt['category']
                if txt == []:
                    continue
                if len(txt) == 1:
                    testList.append(txt[0])
                    continue
                elif len(txt) == 2:
                    testList.append(str(txt[1]))
                    continue
                testList.append(str(txt[1])+":"+str(txt[2]))
            testList = np.unique(testList)
            print(testList)
        except:
            print(i)

        nodes = {"疾病百科":[]}
        for i in testList:
            txt = i.split(":")
            if len(txt) == 1:
                nodes["疾病百科"].append({i:[]})
            else:
                nodes["疾病百科"].append({txt[0]:txt[1]})
        
        print(nodes)
        nodes = json.dumps(nodes,ensure_ascii=False)
        with open('./static/node.json','w') as f:
            f.write(nodes)

#add node dor neo4j
def addNode1(nodeList,relationList,rootNode,nodes,nodeName,method="-"):
    if nodeName not in nodes:
        return nodeList,relationList
    nodeSym = Node(nodeName,name=nodeName)
    for j in nodes[nodeName]:
        node = Node(nodeName[:4],name=j)
        relationList.append(Relationship(nodeSym,method,node))
        nodeList.append(node)
    nodeList.append(nodeSym)
    relationList.append(Relationship(rootNode,nodeName,nodeSym))
    return nodeList,relationList

def addNode2(nodeList,relationList,rootNode,nodes,nodeName,method="-"):
    if nodeName not in nodes:
        return nodeList,relationList
    node = [Node(nodeName,name=j) for j in nodes[nodeName]]
    for j in node:
        nodeList.append(j)
    for j in range(1,len(node)):
        relationList.append(Relationship(node[j-1],method,node[j]))
    relationList.append(Relationship(rootNode,nodeName,node[0]))
    return nodeList,relationList

def processNodes():
    with open("./static/medical.json",'r') as f:
        global neo
        nodes = f.read()
        #print(nodes)
        nodes = json.loads(nodes)
        #neo.create(nodeRoot)
        try:
            for i in nodes:
                createNode = []
                createRelation = []
                nodeDisser = Node("disser",name=i['name'])
                nodeLabelList = ["yibao_status",'get_prob','get_way','cure_lasttime','cured_prob','desc']
                for j in nodeLabelList:
                    if j in i:
                        nodeDisser.add_label(j)
                createNode.append(nodeDisser)

                nodePrevent = Node("preventNode",name="preventNode")
                for j in i['prevent'].split('\n'):
                    node = Node('prevent',method=j)
                    createRelation.append(Relationship(nodePrevent,"method",node))
                    createNode.append(node)
                createNode.append(nodePrevent)
                createRelation.append(Relationship(nodeDisser,"prevent",nodePrevent))

                createNode,createRelation = addNode2(createNode,createRelation,nodeDisser,i,'category')
                createNode,createRelation = addNode2(createNode,createRelation,nodeDisser,i,'cure_department')

                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'symptom')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'acompany')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'check')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'cure_way','method')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'do_eat')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'not_eat')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'recommand_eat')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'recommand_drug')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'drug_detail')
            
                sub = Subgraph(createNode,createRelation)
                t = neo.begin()
                t.create(sub)
                neo.commit(t)
        except Exception as e:
            print(e)
            print(i)
            

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
    #response.headers['user_type'] = 'doctor'
    #response.headers['user_id'] = '114514'

    # 设置cookie
    #response.set_cookie("user_type","doctor",path="/test/")
    #response.set_cookie("user_id","114514")

    return response

@app.route('/AI',methods=['POST','GET'])
def AI():
    global navList
    res = ""
    result = "waiting....."
    # 等待分词处理
    if request.method == 'POST':
        result = request.form['AI_question']
    if request.method == 'GET':
        pass

    response = make_response(render_template('AI.html', name="test consult",res=res,doctor="1.png",navList = navList,result=result))

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
    initSql()
    #command4neo()
    #processJson()
    #processNodes()
    #command4mysql()
    #test4neo()

    #execute4mysql("select * from userinfo")

    server = make_server('127.0.0.1', 5000, app)
    server.serve_forever()
    app.debug = True
    app.run()
    

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