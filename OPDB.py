# -*- coding:utf-8 -*-#
import  MySQLdb as pymysql
import datetime




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
            temp_dict['name'] = res[1]
            temp_dict['sex'] = res[2]
            temp_dict['birth'] = res[3].strftime("%Y-%m-%d")
            b=res[3].strftime("%Y-%m-%d").split('-')
            temp_dict['year'] = b[0]
            temp_dict['month'] = b[1]
            temp_dict['day'] = b[2]
            temp_dict['fathername'] = res[4]
            temp_dict['fatherage'] = res[5]
            temp_dict['fatherunit'] = res[6]
            temp_dict['fatherwork'] = res[7]
            temp_dict['mothername'] = res[8]
            temp_dict['motherage'] = res[9]
            temp_dict['motherunit'] = res[10]
            temp_dict['motherwork'] = res[11]
            temp_dict['motherhealth'] = res[12]
            temp_dict['contraceptivesituation'] = res[13]
            temp_dict['contraceptivename'] = res[14]
            temp_dict['tai'] = res[15]
            temp_dict['chan'] = res[16]
            temp_dict['special'] = res[17]
            temp_dict['yunzhou'] = res[18]
            temp_dict['intrapartumsituation'] = res[19]
            temp_dict['drugallergy'] = res[20]
            temp_dict['birthweight'] = res[21]
            temp_dict['birthheight'] = res[22]
            temp_dict['address'] = res[23]
            temp_dict['zipcode'] = res[24]
            temp_dict['contactnumber'] = res[25]
            temp_dict['visitorigin'] = res[26]
            temp_dict['livingstatus'] = res[27]
            temp_dict['temp'] = res[28]
            temp_dict['belong'] = res[29]

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

    db.commit()
    db.close()

def query_patientsinquiry_table(times,uid):
    db = pymysql.connect("10.10.108.232", "root", "123456", "sh_db", charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM 健康检查表  where uid='%s' and times='%s'" % (uid,times)
    )
    results = cursor.fetchall()
    db.close()
    if len(results) == 1:
        for res in results:
            pass

#获取标准数据

def get_standard_date():
    pass