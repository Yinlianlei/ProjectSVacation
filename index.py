from flask import Flask
from flask import render_template
from flask import make_response
from wsgiref.simple_server import make_server
import MySQLdb as sql
import json

from sqlalchemy import null

# declear and init mysql
db = null
def initMysql():
    with open("./static/sql.json","r") as f:
        try:
            data = json.load(f)
            global db 
            db = sql.connect(data['host'],data['user'],data['password'],data['table'],charset='utf8')
        except Exception as e:
            print(e.with_traceback())


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
    server = make_server('127.0.0.1', 5000, app)
    server.serve_forever()
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