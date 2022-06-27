from flask import Flask, request, json, Response, render_template
from flask_sqlalchemy import SQLAlchemy
import config
import pymysql
import traceback

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

user_pnum = 12345678901

# 连接数据库
conn = pymysql.connect(
    host="47.98.226.235",
    port=3306,
    user="flask",
    password="123456",
    db='flask'
)
cur = conn.cursor()  # 生成游标对象

#历史记录查询
sql = "select user_askhist from `user_data` where user_pnum " + "=" + str(user_pnum)  # SQL语句
print(sql)
cur.execute(sql)  # 执行SQL语句
data = cur.fetchall()  # 通过fetchall方法获得数据
for i in data[:5]:  # 输出前5条数据
    print(i)
cur.close()  # 关闭游标
conn.close()  # 关闭连接


@app.route('/')
def history():
    return render_template("history.html", data1=str(data[0])[2:-3], data2=str(data[1])[2:-3], data3=str(data[2])[2:-3], data4=str(data[3])[2:-3],
                           data5=str(data[4])[2:-3])  # 加入变量传递

if __name__ == "__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)
