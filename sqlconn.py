import traceback
import pymysql

def userlog(user_pnum,user_pwd):
    """

    :param user_pnum:
    :param user_pwd:
    :return:
    None:稍后重试
    "well":密码正确登录成功
    False:密码错误请重试
    """
    conn = pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor = conn.cursor()
    sql = 'select user_psd from userinfo where user_pnum = '+str(user_pnum)
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if data[0][0]==str(user_pwd):
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return "well"
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return None

# print(userlog(12345678901,"123qweasd"))


# <editor-fold desc="问答历史数据库读取">
def gethistmysql(user_pnum):
    """

    :param user_pnum:
    :return:
    None:稍后重试
    """
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor=conn.cursor() # 创建游标对象

    sql = 'select user_askhist from user_data where user_pnum = '+str(user_pnum)
    try:
        cursor.execute(sql)  # 执行sql语句
        data = cursor.fetchall()
        res=[]
        for i in data[-5:]:
          res.append(i[0])
        # print('hhhhhhh')
        # print(len(res))
        if len(res)<=4:
            for i in range(5-len(res)):
                res.append('')
        # print(len(res))
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接
        return res
    except:  # 返回None

        traceback.print_exc()
        print(conn.rollback())
        return None

# gethistmysql("114514")
# </editor-fold>


# <editor-fold desc="用户评论写入数据库">
def commentmysql(comment_score,comment_content):
    """
    用户注册数据库写入
    :param user_pnum:
    :param user_sex:
    :param user_age:
    :param user_name:
    :param user_psd:
    :return:
    None:稍后重试
    "well":评论成功
    False:未知错误
    """
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor=conn.cursor()
    content=[comment_score,comment_content]
    sql="insert into user_comment(comment_score,comment_content) values(%s,%s)"
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
        conn.rollback()
        return False

# commentmysql(5,"希望可以加入会员")
# </editor-fold>

# <editor-fold desc="用户评论写入数据库">
def texttomysql(user_id,user_text):
    """
    用户注册数据库写入
    :param user_pnum:
    :param user_sex:
    :param user_age:
    :param user_name:
    :param user_psd:
    :return:
    None:稍后重试
    "well":评论成功
    False:未知错误
    """
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor=conn.cursor()
    content=[user_id,user_text]
    sql="insert into user_data(user_pnum,user_askhist) values(%s,%s)"
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
        conn.rollback()
        return False

# print(texttomysql(114514,"我最近有点口腔溃疡该怎么办"))
# </editor-fold>

# <editor-fold desc="用户注册写入数据库">
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
        conn.rollback()
        return None

# regimysql(1234567890,1,2,"zeze","123qweasd")
# </editor-fold>


# <editor-fold desc="管理员登录">
def adminlog(user_pnum,user_pwd):
    """

    :param user_pnum:
    :param user_pwd:
    :return:
    None:稍后重试
    "well":密码正确登录成功
    False:密码错误请重试
    """
    conn = pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor = conn.cursor()
    sql = 'select adm_psd from administrators where adm_id = '+str(user_pnum)
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if data[0][0]==str(user_pwd):
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return "well"
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return None

# print(userlog(12345678901,"123qweasd"))
# </editor-fold>


# <editor-fold desc="管理员登录">
def doclog(user_pnum,user_pwd):
    """

    :param user_pnum:
    :param user_pwd:
    :return:
    None:稍后重试
    "well":密码正确登录成功
    False:密码错误请重试
    """
    conn = pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor = conn.cursor()
    sql = 'select doctor_psd from doctorinfo where doctor_pnum = '+str(user_pnum)
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if data[0][0]==str(user_pwd):
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return "well"
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return None

# print(userlog(12345678901,"123qweasd"))
# </editor-fold>



# <editor-fold desc="获取用户性别数据">
def getUserData():
    """

    :param user_pnum:
    :param user_pwd:
    :return:
    None:稍后重试
    "well":密码正确登录成功
    False:密码错误请重试
    """
    conn = pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor = conn.cursor()
    sql = 'select sum(user_sex=0),sum(user_sex=1) from userinfo'
    try:
        cursor.execute(sql)
        conn.commit()
        res=''
        data = cursor.fetchall()
        # print(data)
        if len(data[0])!=0:
            res=res+str(int(data[0][0]))
            # print(res)
            res = res+','+ str(int(data[0][1]))

            # print(res)
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return res
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return False

# print(getUserData())
# </editor-fold>

# <editor-fold desc="获取用户年龄数据">
def getUserData1():
    """

    :param user_pnum:
    :param user_pwd:
    :return:
    None:稍后重试
    "well":密码正确登录成功
    False:密码错误请重试
    """
    conn = pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor = conn.cursor()
    sql = 'select sum(user_age<10),sum(user_age>=10 and user_age<20),sum(user_age>=20 and user_age<30),' \
          'sum(user_age>=30 and user_age<40),sum(user_age>=40 and user_age<50),' \
          'sum(user_age>=50 and user_age<60),sum(user_age>=60) from userinfo where user_sex=0' \


    sql1 = 'select sum(user_age<10),sum(user_age>=10 and user_age<20),sum(user_age>=20 and user_age<30),' \
          'sum(user_age>=30 and user_age<40),sum(user_age>=40 and user_age<50),' \
          'sum(user_age>=50 and user_age<60),sum(user_age>=60) from userinfo where user_sex=1' \


    try:
        cursor.execute(sql)
        conn.commit()
        res=''
        data = cursor.fetchall()

        cursor.execute(sql1)
        conn.commit()
        res1 = ''
        data1 = cursor.fetchall()
        # print(data)
        if len(data[0])!=0:
            res =str(int(data[0][0]))
            for i in range(1,7):
              res = res+','+ str(int(data[0][i]))

            res1 = str(int(data1[0][0]))
            for i in range(1,7):
              res1 = res1+','+ str(int(data1[0][i]))
            res=res+','+res1
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return res
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return False

# print(getUserData1())
# </editor-fold>

# <editor-fold desc="获取用户省份数据">
def getUserData2():
    """

    :param user_pnum:
    :param user_pwd:
    :return:
    None:稍后重试
    "well":密码正确登录成功
    False:密码错误请重试
    """
    conn = pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor = conn.cursor()
    sql = 'select sum(user_city="北京"),sum(user_city="天津"),sum(user_city="上海"),sum(user_city="重庆"),' \
          'sum(user_city="河北"),sum(user_city="河南"),sum(user_city="云南"),' \
          'sum(user_city="辽宁"),sum(user_city="黑龙江"),sum(user_city="湖南"),' \
          'sum(user_city="安徽"),sum(user_city="山东"),sum(user_city="新疆"),' \
          'sum(user_city="江苏"),sum(user_city="浙江"),sum(user_city="江西"),' \
          'sum(user_city="湖北"),sum(user_city="广西"),sum(user_city="甘肃"),' \
          'sum(user_city="山西"),sum(user_city="内蒙古"),sum(user_city="陕西"),' \
          'sum(user_city="吉林"),sum(user_city="福建"),sum(user_city="贵州"),' \
          'sum(user_city="广东"),sum(user_city="青海"),sum(user_city="西藏"),' \
          'sum(user_city="四川"),sum(user_city="宁夏"),sum(user_city="海南"),' \
          'sum(user_city="台湾"),sum(user_city="香港"),sum(user_city="澳门")' \
          'from userinfo' \

    try:
        cursor.execute(sql)
        conn.commit()
        res=''
        data = cursor.fetchall()

        # print(data)
        if len(data[0])!=0:
            res =str(int(data[0][0]))
            for i in range(1,34):
              res = res+','+ str(int(data[0][i]))


            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return res
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return False

# print(getUserData2())
# </editor-fold>

# <editor-fold desc="获取用户热搜数据">
def getUserData3():
    """

    :param user_pnum:
    :param user_pwd:
    :return:
    None:稍后重试
    "well":密码正确登录成功
    False:密码错误请重试
    """
    conn = pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor = conn.cursor()
    sql = 'select alluser_kw,kw_num from kw_Sta'
    try:
        cursor.execute(sql)
        conn.commit()
        res=''
        data = cursor.fetchall()
        # print(data)
        if len(data[0])!=0:
            res = str(data[0][0])+','+str(data[0][1])
            for i in range(1,len(data)):
                res=res+','+ str(data[i][0])+','+str(data[i][1])
            # res=res+str(int(data[0][0]))
            # # print(res)
            # res = res+','+ str(int(data[0][1]))

            # print(res)
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return res
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return False

# print(getUserData3())
# </editor-fold>



# <editor-fold desc="获取用户的总评分">
def getavgscore():
    """

    :param user_pnum:
    :param user_pwd:
    :return:
    None:稍后重试
    "well":密码正确登录成功
    False:密码错误请重试
    """
    conn = pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor = conn.cursor()
    sql = 'select avg(comment_score) from user_comment'
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        if len(data[0])!=0:
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return data[0][0]
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return False

# print(getavgscore())
# </editor-fold>

# <editor-fold desc="用户反馈数据库读取">
def getfeedkback():
    """

    :param user_pnum:
    :return:
    None:稍后重试
    """
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor=conn.cursor() # 创建游标对象

    sql = 'select comment_content from user_comment'
    try:
        cursor.execute(sql)  # 执行sql语句
        data = cursor.fetchall()
        res=[]
        for i in data[:5]:
          res.append(i[0])
        # print('hhhhhhh')
        # print(len(res))
        if len(res)<=4:
            for i in range(5-len(res)):
                res.append('')
        # print(len(res))
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接
        return res
    except:  # 返回None

        traceback.print_exc()
        print(conn.rollback())
        return False

# print(getfeedkback())
# </editor-fold>

# <editor-fold desc="获取医生信息">
def admingetdoctor(doctor_id):
    """

    :param user_pnum:
    :param user_pwd:
    :return:
    None:稍后重试
    "well":密码正确登录成功
    False:密码错误请重试
    """
    conn = pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cursor = conn.cursor()
    sql = 'select doctor_pnum,doctor_name,doctor_age,doctor_field,' \
          'doctor_level,doctor_worktime,online_time,consult_num from doctorinfo where doctor_id = '+str(doctor_id)
    try:
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        res=''
        # print(data)
        if len(data[0])!=0:
            res='姓名：'+str(data[0][1])+'\n'+'手机号：'+str(data[0][0])+'\n'+'年龄：'+str(data[0][2])+'岁\n' \
            +'从医时间：' + str(data[0][5]) + '年\n' +'擅长领域：' + str(data[0][3]) + '\n' \
            + '职称：' + str(data[0][4]) + '\n' +'在线问诊总时长：' + str(data[0][6]) + '小时\n'+'在线问诊次数：' + str(data[0][7]) + '次'
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
            return res
        else:
            return False

    except:  # 返回None

        traceback.print_exc()
        conn.rollback()
        return False
# print(admingetdoctor(1))
# </editor-fold>



# <editor-fold desc="医生注册写入数据库">
def regidocmysql(doctor_pnum,doctor_age,doctor_name,doctor_psd,doctor_field,doctor_level,doctor_worktime):
    """
    医生注册写入数据库
    :param doctor_pnum:
    :param doctor_age:
    :param doctor_name:
    :param doctor_psd:
    :param doctor_field:
    :param doctor_level:
    :param doctor_worktime:
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
# </editor-fold>






# <editor-fold desc="问答历史写入数据库">
def histmysql(user_pnum,user_askhist):
    """

    :param user_pnum:
    :param user_askhist:
    :return:
    同上
    """
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
# </editor-fold>

def getOnlineDoctor():
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cur = conn.cursor()  # 创建游标对象
    sql = "select doctor_name,doctor_level,doctor_worktime,online_time,consult_num,doctor_pnum from doctorinfo where doctor_pnum in (select doc_phoneId from qaOnlineDoctor where `status` = 1);"
    cur.execute(sql)  # 执行sql语句
    data = cur.fetchall()
    cur.close()  # 关闭游标
    conn.close() # 关闭连接
    return data

# for doctor login and change status
def docLogin(input):
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cur = conn.cursor()  # 创建游标对象
    sql = 'update qaOnlineDoctor set `status` = 1 where doc_phoneId = \"'+input+"\";"
    #print(sql)
    cur.execute(sql)  # 执行sql语句
    cur.close()  # 关闭游标
    conn.close() # 关闭连接

# for doctor logout and change status
def docLogout(input):
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cur = conn.cursor()  # 创建游标对象
    sql = 'update qaOnlineDoctor set `status` = 0 where doc_phoneId = \"'+input+"\";"
    cur.execute(sql)  # 执行sql语句
    data = cur.fetchall()
    print(data)
    cur.close()  # 关闭游标
    conn.close() # 关闭连接

def userQuestionAdd(room,inputUid,inputDid):
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cur = conn.cursor()  # 创建游标对象
    content=[room,inputUid,inputDid]
    sql = 'insert into qaOnline values (0,now(),%s,%s,%s,2);'
    try:
        cur.executemany(sql,[content])
        conn.commit()
        result=cur.fetchall()
        if len(result)==1:
            cur.close() # 关闭游标
            conn.close() # 关闭连接
            print(result)
            return result
        else:
            return False

    except:
        traceback.print_exc()
        conn.rollback()

def docGetUserList(inputDid):
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cur = conn.cursor()  # 创建游标对象
    sql = 'select uid,did,userRoom from qaOnline where did = \"'+inputDid+'\" and `status` = 2'
    cur.execute(sql)  # 执行sql语句
    data = cur.fetchall()
    cur.close()  # 关闭游标
    conn.close() # 关闭连接
    return data

def docUserInfoChange(inputDid):
    conn=pymysql.connect(
        host="47.98.226.235",
        port=3306,
        user="flask",
        password="123456",
        db='flask'
    )
    cur = conn.cursor()  # 创建游标对象
    sql = 'update qaOnline set docRoom = \"'+inputDid+'\" where uid = '
    cur.execute(sql)  # 执行sql语句
    data = cur.fetchall()
    cur.close()  # 关闭游标
    conn.close() # 关闭连接













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