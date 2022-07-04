import traceback
import pymysql

#用户注册数据库写入
def regimysql(user_pnum,user_sex,user_age,user_name,user_psd):
    """
    用户注册数据库写入
    :param user_pnum:
    :param user_sex:
    :param user_age:
    :param user_name:
    :param user_psd:
    :return:
    None:稍后重试
    "well":注册成功
    False:已注册
    """
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor=conn.cursor()
    content=[user_pnum,user_sex,user_age,user_name,user_psd]
    sql="insert into userinfo(user_pnum,user_sex,user_age,user_name,user_psd) values(%s,%s,%s,%s,%s)"
    try:
        cursor.executemany(sql,[content])
        conn.commit()
        result=cursor.fetchall()
        if len(result)==0:
            result='well'
            cursor.close() # 关闭游标
            conn.close() # 关闭连接

            return result
        else:
            return False

    except:#返回None

        traceback.print_exc()
        result=conn.rollback()
        return result


# regimysql(1234567890,1,2,"zeze","123qweasd")


#医生注册数据库写入
def regidocmysql(doctor_pnum,doctor_age,doctor_name,doctor_psd,doctor_field,doctor_level,doctor_worktime):
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor=conn.cursor()
    content=[doctor_pnum,doctor_age,doctor_name,doctor_psd,doctor_field,doctor_level,doctor_worktime]
    sql="insert into doctorinfo(doctor_pnum,doctor_age,doctor_name,doctor_psd,doctor_field,doctor_level,doctor_worktime) values(%s,%s,%s,%s,%s,%s,%s)"
    try:
        cursor.executemany(sql,[content])
        conn.commit()
        result=cursor.fetchall()
        if len(result)==0:
            result='well'
            cursor.close() # 关闭游标
            conn.close() # 关闭连接

            return result
        else:
            return False

    except:#返回None

        traceback.print_exc()
        result=conn.rollback()
        return result


# regidocmysql(15666666666,35,"张仲景","114514","心理学","主任医师",12)



#问答历史数据库写入
def histmysql(user_pnum,user_askhist):
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor=conn.cursor() # 创建游标对象

    content=[user_pnum,user_askhist]
    sql="insert into user_data(user_pnum,user_askhist) values(%s,%s)"
    try:
        cursor.executemany(sql,[content])
        conn.commit()
        result=cursor.fetchall()
        if len(result)==1:
            cursor.close() # 关闭游标
            conn.close() # 关闭连接
            print(result)
            return result
        else:
            return False

    except:
        traceback.print_exc()
        conn.rollback()

# histmysql("12345678901","我感觉有点头痛怎么办")


#问答历史数据库读取
def gethistmysql(user_pnum):
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor=conn.cursor() # 创建游标对象

    sql = 'select * from user_data where user_pnum = '+str(user_pnum)
    cursor.execute(sql)  # 执行sql语句
    data = cursor.fetchall()
    print(data)

    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接



















#数据库读取
def getmysql():
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cur = conn.cursor()  # 创建游标对象
    sql = 'select * from userinfo'
    cur.execute(sql)  # 执行sql语句
    data = cur.fetchall()
    print(data)
    cur.close()  # 关闭游标
    conn.close() # 关闭连接