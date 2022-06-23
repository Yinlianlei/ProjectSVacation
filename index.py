from flask import Flask
from flask import render_template
from flask import make_response
from wsgiref.simple_server import make_server
import MySQLdb as sql
from py2neo import Graph,Node,Relationship
import json

from sqlalchemy import null

# declear and init mysql
db = null
neo = null
def initMysql():
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
            # new version of py2neo
            neo = Graph("http://localhost:7474", auth=(
                        data["neo4j"]['user'],
                        data["neo4j"]['password']))
        except Exception as e:
            print(e.with_traceback())

# execute sql
def command4mysql():
    with open("./static/base.sql",'r') as f:
        txt = f.read()
        global db
        cursor = db.cursor()
        try:
            for i in txt.split(';'):
                # 执行sql语句
                cursor.execute(i)
                # 提交到数据库执行
                db.commit()
        except Exception as e:
            # 如果发生错误则回滚
            print(i)
            db.rollback()

def command4neo():
    pass

def test4neo():
    #with open("./static/test.json","r") as f:
    #    data = json.load(f)
    #    node = []
    #    rel = []
    #    for i in data:
    #        node.append(Node('Person',name=i['name']))
    #        rel.append(i["relation"])
    #    
    #    #print(node,rel)
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

if __name__ == "__main__":
    initMysql()
    test4neo()
    #command4mysql()
    #server = make_server('127.0.0.1', 5000, app)
    #server.serve_forever()
    #app.run()
    

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