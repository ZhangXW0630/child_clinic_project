# -*- coding:utf-8 -*-#
import  MySQLdb as pymysql
import time
import datetime
import math




def insert_patient_user(phone,password):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8' )
    cursor = db.cursor()
    cursor.execute("INSERT INTO 家长用户表 (user_phone, user_password) VALUES ('%s','%s')" % (phone, password)
                   )
    db.commit()
    db.close()

def insert_doctor_user(phone,password):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute("INSERT INTO 医生用户表 (user_phone, user_password) VALUES ('%s','%s')" % (phone, password)
                   )
    db.commit()
    db.close()

def query_doctor_user(phone,password):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute("INSERT INTO 医生用户表 (user_phone, user_password) VALUES ('%s','%s')" % (phone, password)
                   )
    db.commit()
    db.close()
def query_patient_user(phone,password):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT id,user_name,user_phone,user_password FROM 家长用户表  where user_phone='%s' and user_password='%s'" % (phone, password)
                   )
    results = cursor.fetchall()
    db.close()
    if len(results)==1:
        for res in results:
            temp_dict=dict()
            temp_dict['status']='success'
            temp_dict['id']=res[0]
            temp_dict['name'] = res[1]
            temp_dict['phone']=res[2]
            temp_dict['password'] = res[3]
            return temp_dict
    else:
        temp_dict=dict()
        temp_dict['status']='fail'
        return temp_dict


def query_isexist(uid):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM 健康检查表  where uid='%s'" % (uid)
        )
    results = cursor.fetchall()
    db.close()
    if len(results) == 1:
        for res in results:
            temp_dict = dict()
            temp_dict['status'] = 'success'
            temp_dict['name'] = res[2]
            temp_dict['sex'] = res[3]
            temp_dict['birth'] = res[4].strftime("%Y-%m-%d")
            b=res[4].strftime("%Y-%m-%d").split('-')
            temp_dict['year'] = b[0]
            temp_dict['month'] = b[1]
            temp_dict['day'] = b[2]
            temp_dict['fathername'] = res[5]
            temp_dict['fatherage'] = res[6]
            temp_dict['fatherunit'] = res[7]
            temp_dict['fatherwork'] = res[8]
            temp_dict['mothername'] = res[9]
            temp_dict['motherage'] = res[10]
            temp_dict['motherunit'] = res[11]
            temp_dict['motherwork'] = res[12]
            temp_dict['motherhealth'] = res[13]
            temp_dict['contraceptivesituation'] = res[14]
            temp_dict['contraceptivename'] = res[15]
            temp_dict['tai'] = res[16]
            temp_dict['chan'] = res[17]
            temp_dict['special'] = res[18]
            temp_dict['yunzhou'] = res[19]
            temp_dict['intrapartumsituation'] = res[20]
            temp_dict['drugallergy'] = res[21]
            temp_dict['birthweight'] = res[22]
            temp_dict['birthheight'] = res[23]
            temp_dict['address'] = res[24]
            temp_dict['zipcode'] = res[25]
            temp_dict['contactnumber'] = res[26]
            temp_dict['visitorigin'] = res[27]
            temp_dict['livingstatus'] = res[28]
            temp_dict['temp'] = res[29]
            temp_dict['belong'] = res[30]

            return temp_dict
    else:
        temp_dict = dict()
        temp_dict['status'] = 'fail'
        return temp_dict

def query_isexist_inquery(uid):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM 询问记录表  where uid='%s'" % (uid)
        )
    results = cursor.fetchall()
    db.close()
    if len(results) == 1:
        for res in results:
            temp_dict = dict()
            temp_dict['status'] = 'success'
            temp_dict['times'] = res[2]
            temp_dict['date'] = res[3]
            temp_dict['age'] = res[4]
            temp_dict['weight'] = res[5]
            temp_dict['height'] = res[6]
            temp_dict['howmany'] = res[7]
            temp_dict['howtimes'] = res[8]
            temp_dict['duanmuru'] = res[9]
            temp_dict['milk'] = res[10]
            temp_dict['milkpowed'] = res[11]
            temp_dict['riceflour'] = res[12]
            temp_dict['foor'] = res[13]
            temp_dict['congee'] = res[14]
            temp_dict['rice'] = res[15]
            temp_dict['meat'] = res[16]
            temp_dict['yolk'] = res[17]
            temp_dict['bean'] = res[18]
            temp_dict['vegetables'] = res[19]
            temp_dict['fruits'] = res[20]
            temp_dict['ADname'] = res[21]
            temp_dict['ADhowmany'] = res[22]
            temp_dict['GAname'] = res[23]
            temp_dict['GAbao'] = res[24]
            temp_dict['GApian'] = res[25]
            temp_dict['other'] = res[26]


            return temp_dict
    else:
        temp_dict = dict()
        temp_dict['status'] = 'fail'
        return temp_dict

def insert_patient_healthstatus_table(ad):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute("INSERT INTO 健康检查表 (uid,`name`, sex,birth,"
                   "fathername,fatherage,fatherunit,fatherwork,mothername,"
                   "motherage,motherunit,motherwork,motherhealth,contraceptivesituation,contraceptivename,tai,chan,special,yunzhou,intrapartumsituation,drugallergy,birthweight,birthheight,address,zipcode,contactnumber,visitorigin,livingstatus,temp,belong)" 
                   "VALUES ('%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                   %(int(ad['uid'][0]),ad['name'][0], ad['sex'][0],ad['birth'],ad['fathername'][0],ad['fatherage'][0],ad['fatherunit'][0],ad['fatherwork'][0],ad['mothername'][0],ad['motherage'][0],ad['motherunit'][0],ad['motherwork'][0],ad['motherhealth'][0],ad['contraceptivesituation'][0],ad['contraceptivename'][0],ad['tai'][0],ad['chan'][0],ad['special'][0],ad['yunzhou'][0],ad['intrapartumsituation'][0],ad['drugallergy'][0],ad['birthweight'][0],ad['birthheight'][0],ad['address'][0],ad['zipcode'][0],ad['contactnumber'][0],ad['visitorigin'][0],ad['livingstatus'][0],ad['temp'][0],ad['belong'][0]))
    db.commit()
    db.close()

def insert_patient_inquirystatus_table(ad):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute("INSERT INTO 询问记录表 (uid,times,data,age,"
                   "weight,height,breastmilksituation,breastmilkfrequency,alwaysbreastmilk,"
                   "milk,milkpowder,riceflour,noodle,congee,rice,meatorfish,egg,beanproducts,vegetables,fruit,VADname,VADfrequence,caname,capowder,caslice,remark)"
                   "VALUES ('%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                   % (
                   int(ad['uid'][0]), ad['times'][0],ad['date'][0], ad['age'][0], ad['weight'][0], ad['height'][0],
                   ad['howmany'][0], ad['howtimes'][0], ad['duanmuru'][0], ad['milk'][0],
                   ad['milkpowed'][0], ad['riceflour'][0], ad['food'][0], ad['congee'][0],
                   ad['rice'][0], ad['meat'][0], ad['yolk'][0], ad['bean'][0],ad['vegetables'][0],
                   ad['fruits'][0], ad['ADname'][0], ad['ADhowmany'][0], ad['GAname'][0],ad['GAbao'][0],ad['GApian'][0],
                   ad['other'][0]))
    db.commit()
    db.close()

def query_patientsinquiry_table(uid,times):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM 询问记录表  where uid='%s' and times='%s'" % (uid,times)
    )
    results = cursor.fetchall()
    db.close()
    if len(results) == 1:
        for res in results:
            temp_dict = dict()
            temp_dict['status'] = 'success'
            temp_dict['times'] = res[2]
            temp_dict['date'] = res[3].strftime("%Y-%m-%d")
            temp_dict['age'] = res[4]
            temp_dict['weight'] = res[5]
            temp_dict['height'] = res[6]
            temp_dict['howmany'] = res[7]
            temp_dict['howtimes'] = res[8]
            temp_dict['duanmuru'] = res[9]
            temp_dict['milk'] = res[10]
            temp_dict['milkpowed'] = res[11]
            temp_dict['riceflour'] = res[12]
            temp_dict['food'] = res[13]
            temp_dict['congee'] = res[14]
            temp_dict['rice'] = res[15]
            temp_dict['meat'] = res[16]
            temp_dict['yolk'] = res[17]
            temp_dict['bean'] = res[18]
            temp_dict['vegetables'] = res[19]
            temp_dict['fruits'] = res[20]
            temp_dict['ADname'] = res[21]
            temp_dict['ADhowmany'] = res[22]
            temp_dict['GAname'] = res[23]
            temp_dict['GAbao'] = res[24]
            temp_dict['GApian'] = res[25]
            temp_dict['other'] = res[26]
            # temp_dict['belong']=res[28]
            return temp_dict
    else:
        temp_dict = dict()
        temp_dict['status'] = 'fail'
        return temp_dict

#获取标准数据
def query_current_times(uid):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM 询问记录表  where uid='%s'" % (uid)
    )
    results = cursor.fetchall()
    db.close()
    if len(results) == 1:
        for res in results:
            temp_dict = dict()
            temp_dict['times']=int(res[2])+1
    else:
        temp_dict = dict()
        temp_dict['times']=1
    return temp_dict
def get_standard_date():
    pass

def get_advice(uid):


    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        "SELECT birth FROM 健康检查表  where uid='%s'" % (uid)
    )
    results = cursor.fetchall()
    if len(results) == 1:
        for res in results:
            age=math.ceil((((datetime.date.today() - res[0]).total_seconds())/2592000))
    else:
        age="0"
    cursor.execute(
        "SELECT * FROM  各月龄喂养建议知识库 where age='%s'" % (age)
    )
    results = cursor.fetchall()
    db.close()
    if len(results) == 1:
        for res in results:
            temp_dict = dict()
            temp_dict['age']=age
            temp_dict['status']="success"
            temp_dict['hint']=res[2]
            temp_dict['feedadvice']=res[3]
            temp_dict['mealadvice']=res[4]
            temp_dict['problem']=res[5]
    else:
        temp_dict = dict()
        temp_dict['status'] = "fail"
    return temp_dict


def get_growthstandard():


    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    # cursor.execute(
    #     "SELECT birth FROM 健康检查表  where uid='%s'" % (uid)
    # )
    # results = cursor.fetchall()
    # if len(results) == 1:
    #     for res in results:
    #         age=math.ceil((((datetime.date.today() - res[0]).total_seconds())/2592000))
    # else:
    #     age="0"
    cursor.execute(
        "SELECT * FROM 男年龄身高 "
    )
    results = cursor.fetchall()
    db.close()
    if len(results) > 0:
        temp_dict1 = []
        for res in results:
            temp_dict = dict()
            temp_dict['age']=res[0]
            temp_dict['status']="success"
            temp_dict['P3']=res[1]
            temp_dict['P10']=res[2]
            temp_dict['P50']=res[3]
            temp_dict['P85']=res[4]
            temp_dict['P97'] = res[5]
            temp_dict1.append(temp_dict)

    else:
        temp_dict = dict()
        temp_dict['status'] = "fail"
    print (temp_dict1)
    return temp_dict1