# encoding:utf-8
from MySQLdb import connect
import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def conn():
    conn_cx = connect(host='127.0.0.1', user='root', passwd='123456', db='robot_db', port=3306, charset="utf8")
    return conn_cx

cases_key = [u'caseID', u'caseFirstID', u'caseSecondID', u"patientID",u"doctorID",u"isFinish",u"category",
             u'disease_zy',u'disease_xy', u'first_symptom', u'second_symptom', u'look', u'listen',
            u'question', u'pulse', u'onset_time',u'case_date',  u'medicine_history',   u'therapy_history', u'bianzheng', u'zhifa',
            u'zhuxue', u'peixue', u'jiajianxue', u'xiaoyanxue', u"therapy",
             u'name', u'sex', u'age', u'job', u'height', u'weight', u'address', u'telephone', u'anamnesis', u'family_history']
default_cases_dict = {u'caseFirstID':1, u'caseSecondID':0, u"patientID":0,u"doctorID":0,u"isFinish":0,u"category":1,
             u'disease_zy':u"",u'disease_xy':u"", u'first_symptom':u"", u'second_symptom':u"", u'look':u"", u'listen':u"",
            u'question':u"", u'pulse':u"", u'onset_time':u"",u'case_date':u"",  u'medicine_history':u"",   u'therapy_history':u"", u'bianzheng':u"", u'zhifa':u"",
            u'zhuxue':u"", u'peixue':u"", u'jiajianxue':u"", u'xiaoyanxue':u"", u"therapy":u"",
            u'name':u"", u'sex':u"", u'age':u"", u'job':u"", u'height':u"", u'weight':u"", u'address':u"", u'telephone':u"", u'anamnesis':u"", u'family_history':u""}
cases_num_count = 7
cases_str_count = 19

doctor_key = [u'doctorID', u'name', u'sex', u'age', u'telephone', u'identityCardNum', u'indication', u'department',                 u"remen_dict", u"tigejiancha_dict"]
patient_key = [u'patientID', u'name', u'sex', u'age', u'telephone', u'identityCardNum', u'socialSecurityNum',u'height',u'weight',u'job',u'address',u'family_history']



DCRelation_key = [u'relationId', u'caseId', u'caseSecondID', u'doctorID', u'doctorRole', u'doctorComment', u'caseFirstID', u'comment_time']
medicine_key = [u'medicineID', u'medicineSystemID']
treatment_key = [u'treatmentSystemID', u'treatmentID']
appendix_key = [u'appendixID', u'caseFirstID', u'caseSecondID', u'name', u'type', u'path', u'abstract', u'upload_time']
CARelation_key = [u'CARelationID', u'caseFirstID', u'caseSecondID', u'name', u'type', u'info', u'assayID']
dianxuan_key = [u"dianxuanID",u"doctorID",u"category",u"remen_dict",u"tigejiancha_dict"]


def search_user(user_phone, user_password, user_type):
    """
    查找用户是否再数据库中
    :param user_phone: 用户手机号
    :param user_password: 用户密码
    :param user_type: 用户类型
    :return:
    """
    con = conn()
    try:
        cur = con.cursor()
        if user_type == 0:
            search_sql = u"select patientID, name from patient where telephone = '{}' and name = '{}'".format(
                user_phone, user_password)
        else:
            search_sql = u"select doctorID, name from doctor where telephone = '{}' and d_password = '{}'".format(
                user_phone, user_password)
        print search_sql
        cur.execute(search_sql)
        res = cur.fetchone()
        if res is None:
            print u"用户不存在"
            return [-1, u"not in", -1]
        print u"search user success! "
        return [res[0], res[1], 1]
    except Exception, e:
        print u"search user error {}".format(e.message)
    finally:
        # pass
        con.close()

def select_id_by_phone(phone):
    """
    根据用户手机号查询其id
    :param phone: str
    :return:
    """
    con = conn()
    try:
        cursor = con.cursor()
        sql1 = u"select * from patient where p_phone = '{}'".format(phone)
        cursor.execute(sql1)
        res1 = cursor.fetchone()
        if res1 is not None and len(res1) != 0:
            cursor.close()
            print res1[0]
            return res1[0]
        sql2 = u"select * from doctor where d_phone = '{}'".format(phone)
        cursor.execute(sql2)
        res2 = cursor.fetchone()
        if res2 is not None and len(res2) != 0:
            cursor.close()
            print res2[0]
            return res2[0]
        cursor.close()
        return -1
    except Exception, e:
        print e
    finally:
        # pass
        con.close()

def query_code(create_id, content):
    """
    查询用户数输入的邀请码是否有效
    :param create_id:
    :param content:
    :return:
    """
    con = conn()
    sselect_sql = "SELECT * FROM Invitation_code WHERE create_user ={} and code_content = '{}' and flag = 0".format(
        create_id, content)
    try:
        cursor = con.cursor()
        cursor.execute(sselect_sql)
        results = cursor.fetchall()
        if len(results) > 0:
            flag = 0
        else:
            flag = 1
        cursor.close()
        return flag
    except Exception, e:
        print e
    finally:
        # pass
        con.close()
####################################################################
def create_logs():
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS logs;")
    cursor.execute("create table logs(logID INT auto_increment primary key, hostname VARCHAR (200),TYPE INT)"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()

def create_cases():
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS cases;")
    cursor.execute("create table cases(caseID INT auto_increment primary key, caseFirstID INT, caseSecondID INT DEFAULT 0,"
                   "patientID INT DEFAULT 0,doctorID INT DEFAULT 0 ,isFinish INT DEFAULT 0,category INT DEFAULT 0,"
                   "disease_zy VARCHAR(100),disease_xy VARCHAR(100), first_symptom VARCHAR(2000),second_symptom VARCHAR(2000),"
                   "look VARCHAR(200),listen varchar(200),question varchar(200),pulse varchar(200),"
                   "onset_time varchar(20),case_date VARCHAR(20) ,medicine_history varchar(2000),therapy_history varchar(2000),"
                   "bianzheng varchar(2000),zhifa varchar(2000),"
                   "zhuxue VARCHAR(200),peixue varchar(200),jiajianxue varchar(200),xiaoyanxue varchar(200),"
                   "therapy VARCHAR(2000))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()

#插入数据
def insert_cases(case_dict):
    caseFirstID = int(case_dict.get(u'caseFirstID',0))
    if caseFirstID==0:
        caseFirstID = query_maxFirstID()+1
        caseSecondID = 1
    else:
        caseSecondID = query_maxSecondID(case_dict)+1
    case_dict[u"caseFirstID"] = caseFirstID
    case_dict[u"caseSecondID"] = caseSecondID
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    input_dict = default_cases_dict
    input_dict.update(case_dict)
    print 'input_dict:', input_dict
    # values = [input_dict.get(k) for k in cases_key[1:]]
    # sql = "insert into cases("+u",".join(cases_key[1:])+") values("+u",".join(["{}"]*(cases_num_count-1)+["'{}'"]*cases_str_count)+");"
    input_dict_keys = input_dict.keys()
    input_dict_keys.remove(u'caseID')
    values = [input_dict[k] for k in input_dict_keys]
    print '--------------', len(input_dict_keys), len(values)
    sql = "insert into cases("+u",".join(input_dict_keys)+") values("+u",".join(['"{}"']*(len(values)))+");"
    sql = sql.format(*values)
    print 'sql command:', sql
    # print sql
    try:
        cursor_insert.execute(sql)
        con_insert.commit()
        cursor_insert.close()
    except Exception, e:
        print e
        con_insert.rollback()
    finally:
        con_insert.close()
    caseID = query_cases({u'caseFirstID':caseFirstID,u'caseSecondID':caseSecondID})[0][u'caseID']
    return [caseID,caseFirstID,caseSecondID]

def query_maxFirstID():
    query_cx = conn()
    query_sql = "select MAX(caseFirstID) from cases;"
    maxFirstID = 0
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        # print results
        if results[0][0] is not None:
            maxFirstID = results[0][0]
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return maxFirstID

#query insert update delete
def query_maxSecondID(case_dict):
    query_cx = conn()
    query_sql = "select MAX(caseSecondID) from cases where caseFirstID = {};".format(case_dict.get(u'caseFirstID', 1))
    maxSecondID = 0
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        if results[0][0] is not None:
            maxSecondID = results[0][0] + 1
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return maxSecondID

def query_cases(cases_dict):
    key_list = cases_dict.keys()
    patient_dict = {key: cases_dict[key] for key in key_list if key in cases_key}
    query_cx = conn()
    str_query = []
    for key, value in patient_dict.items():
        # if value != "" and key not in [u"doctorID", u"chiefComplaint"]:
        str_query.append("{} = '{}'".format(key, value))
    if len(str_query) == 0:
        query_sql = "SELECT * FROM cases"
    else:
        query = " and ".join(str_query)
        query_sql = "SELECT * FROM cases WHERE {}".format(query)

    results_all = []
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            for i,v in enumerate(cases_key):
                temp_dict[v] = res[i]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all

def update_case(case_dict):
    """
　　　通过case_dict更新ase记录
    :param case_dict:key 为case表中所有可能的字段
            {
                "caseID": ,
                "caseSecondID": ,
                "chiefComplaint": ,
                "isFinish": ,
            }
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    str_query = []
    condition = "WHERE caseFirstID = {} and caseSecondID = " \
                "{}".format(case_dict.get(u"caseFirstID", ""), case_dict.get(u"caseSecondID", ""))
    for key, value in case_dict.items():
        if key not in [u"caseFirstID", u"caseID", u"caseSecondID"] and key in cases_key:
            str_query.append("{} = '{}'".format(key, value))
    query = " , ".join(str_query)
    query_sql = "update cases set {} {};".format(query, condition)
    print query_sql
    flag = 0
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        query_cx.commit()
        cursor_query.close()
        flag = 1
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return flag

def query_case_during_peroid_of_patientid(case_dict):
    """
　　　通过patientid查询case记录
    :param {start_time,end_time,patientID}
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    query_sql = "select * from cases where patientID = {} and  caseDate BETWEEN '{}' AND '{}' " \
        .format(case_dict.get('patientID'), case_dict.get("start_time"), case_dict.get("end_time"))
    results_all = []
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        # print len(results)
        for res in results:
            # print res
            temp_dict = dict()
            for i,v in enumerate(cases_key):
                temp_dict[v] = res[i]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all

def search_cases(query):
    '''
            cases = db.search_cases({"disease_name":disease_name,"peixue":peixue,"patient_name":name,"telephone":telephone})
            select * from cases,patient WHERE cases.patientID=patient.patientID AND patient.telephone = '15612341234' AND patient.name = '王小山' AND cases.disease_zy = '失眠' AND cases.therapy LIKE '{}';
    '''
    con = conn()
    results = []
    sql = "select * from cases,patient WHERE cases.patientID=patient.patientID"
    condition = u""
    if len(query)>0:
        condition = u" and "+u" and ".join([u"{} like '%{}%'".format(k,v) for k,v in query.items()])
    sql = sql+condition+u";"
    # print sql
    try:
        cursor = con.cursor()
        cursor.execute(sql)
        lines = cursor.fetchall()
        res_keys = cases_key+patient_key
        for line in lines:
            r = dict()
            for i,v in enumerate(res_keys):
                r[v] = line[i]
            results.append(r)
    except Exception,e:
        print e
    finally:
        con.close()
        return results
####################################################################

def create_doctor():
    """
    创建医生表，主键自增长
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS doctor;")
    cursor.execute("create table doctor(doctorID INT primary key auto_increment, name VARCHAR(20), sex VARCHAR(6),"
                   " age  INT, telephone VARCHAR (20), identityCardNum VARCHAR (20), indication VARCHAR (200), "
                   "department VARCHAR (200), d_password VARCHAR (50),"
                   "ziduan1 VARCHAR (1000), ziduan2 VARCHAR (1000),ziduan3 VARCHAR (1000),ziduan4 VARCHAR (1000))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()

def insert_doctor(doctor_dict):
    """
    医生表插入操作
    :return:
    """
    success = 1
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    sql = "INSERT INTO doctor(name,sex,age, telephone,\
          identityCardNum, indication, department, d_password)VALUES ('{}','{}',{},'{}','{}','{}','{}'," \
          "'{}');".format(doctor_dict.get("name", ""),
                          doctor_dict.get("sex", ""),
                          doctor_dict.get("age", 0),
                          doctor_dict.get("telephone", ""),
                          doctor_dict.get("identityCardNum", ""),
                          doctor_dict.get("indication", ""),
                          doctor_dict.get("department", ""),
                          doctor_dict.get("d_password", ""))
    print sql
    try:
        cursor_insert.execute(sql)
        con_insert.commit()
        cursor_insert.close()
    except Exception, e:
        print e
        con_insert.rollback()
        success = 0
    finally:
        con_insert.close()
        return success

def query_doctor(doctor_dict):
    """
    给定医生的信息字典，查询医生ＩＤ
    :param doctor_dict:｛
            "name":"王医生",
            "identityCardNum":"王小山",
            "socialSecurityNum":"15612341234",
            "telephone":"15612341234",
            "doctorID" : 1,
            ｝
    :return:返回查询到的所有患者档案信息，用列别表示，[｛医生信息Ａ｝，｛医生信息Ｂ｝,......]
    """
    key_list = doctor_dict.keys()
    doctor_dict = {key: doctor_dict[key] for key in key_list if key in doctor_key}
    query_cx = conn()
    str_query = []
    for key, value in doctor_dict.items():
        if value != "":
            str_query.append("{} = '{}'".format(key, value))
    query = " and ".join(str_query)
    if len(query) == 0:
        query_sql = "SELECT * FROM doctor"
    else:
        query_sql = "SELECT * FROM doctor WHERE {}".format(query)
    results_all = []
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'doctorID'] = res[0]
            temp_dict[u'name'] = res[1]
            temp_dict[u'sex'] = res[2]
            temp_dict[u'age'] = res[3]
            temp_dict[u'telephone'] = res[4]
            temp_dict[u'identityCardNum'] = res[5]
            temp_dict[u'indication'] = res[6]
            temp_dict[u'department'] = res[7]
            temp_dict[u'remen_dict'] = res[9]
            temp_dict[u'tigejiancha_dict'] = res[10]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all

def update_doctor(doctor_dict):
    """
    更细医生信息
    :param doctor_dict:｛
            "name":"王医生",
            "identityCardNum":"王小山",
            "socialSecurityNum":"15612341234",
            "telephone":"15612341234",
            "doctorID" : 1,
            ｝
    :return:返回查询到的所有患者档案信息，用列别表示，[｛医生信息Ａ｝，｛医生信息Ｂ｝,......]
    """
    query_cx = conn()
    str_query = []
    condition = "WHERE doctorID = {}".format(doctor_dict.get(u"doctorID", u""))
    for key, value in doctor_dict.items():
        if value != "" and key not in [u"caseFirstID", u"caseSecondID", u'doctorID'] and key in doctor_key:
            str_query.append("{} = '{}'".format(key, value))
    query = " , ".join(str_query)
    query_sql = "update doctor set {} {};".format(query, condition)
    # print query_sql
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        query_cx.commit()
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
####################################################################
def create_patient():
    """
    创建患者表，主键自增长
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS patient;")
    cursor.execute("create table patient(patientID INT primary key auto_increment, name VARCHAR(20), sex VARCHAR(6),"
                   "age VARCHAR (10), telephone VARCHAR (20), identityCardNum VARCHAR (20), socialSecurityNum VARCHAR (20), p_password VARCHAR (50),"
                   "ziduan1 VARCHAR (1000), ziduan2 VARCHAR (1000),ziduan3 VARCHAR (1000),ziduan4 VARCHAR (1000))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")

    cursor.close()

def insert_patient(patient_dict):
    """
    患者表插入操作
    patient_dict:患者信息字典
    :return:
    """
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    success = 1
    # u'height', u'weight', u'job', u'address', u'family_history'
    sql = "INSERT INTO patient(name,sex,age,telephone,\
          identityCardNum,socialSecurityNum, p_password,height,weight,job,address,family_history)VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
          "'{}');".format(patient_dict.get("name", ""),
                          patient_dict.get("sex", ""),
                          patient_dict.get("age", ""),
                          patient_dict.get("telephone", ""),
                          patient_dict.get("identityCardNum", ""),
                          patient_dict.get("socialSecurityNum", ""),
                          patient_dict.get("p_password", ""),
                          patient_dict.get("height", ""),
                          patient_dict.get("weight", ""),
                          patient_dict.get("job", ""),
                          patient_dict.get("address", ""),
                          patient_dict.get("family_history", ""))
    try:
        cursor_insert.execute(sql)
        con_insert.commit()
        cursor_insert.close()
    except Exception, e:
        print e
        con_insert.rollback()
        success = 0
    finally:
        con_insert.close()
        return success
def query_patient(patient_id):
    titles = u','.join(patient_key)
    query_sql = "select "+titles+" from patient WHERE patientID = "+str(patient_id)
    query_cx = conn()
    temp_dict = dict()
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        res = cursor_query.fetchone()
        if res:
            # temp_dict = dict()
            for i,name in enumerate(patient_key):
                temp_dict[name] = res[i]
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return temp_dict

def update_patient(patient_dict):
    """
　　　通过case_dict更新ase记录
    :param case_dict:key 为case表中所有可能的字段
            {
                "caseID": ,
                "caseSecondID": ,
                "chiefComplaint": ,
                "isFinish": ,
            }
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    str_query = []
    condition = "WHERE patientID = {}".format(patient_dict.get(u"patientID", ""))
    for key, value in patient_dict.items():
        if value != "" and key not in [u"patientID"] and key in patient_key:
            str_query.append("{} = '{}'".format(key, value))
    query = " , ".join(str_query)
    query_sql = "update patient set {} {};".format(query, condition)
    # print query_sql
    flag = 0
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        query_cx.commit()
        cursor_query.close()
        flag = 1
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return flag

####################################################################

def insert_appendix(appendix_dict):
    """
    药物表插入操作，首先会判断药物是否已经存在系统中
    :param appendix_dict:｛
            caseFirstID:附件属于的病例的FirstID
            caseSecondID:附件属于的病例的SecondID
            name:　附件名称
            path:　附件地址
            type: 附件类型，PDF, WORD等
            abstract: 附件摘要
            ｝
    :return:
    status：
        0: 附件插入成功；
        １：附件插入失败；
    """

    con_insert = conn()
    cursor_insert = con_insert.cursor()
    sql = "INSERT INTO appendix(caseFirstID, caseSecondID, name, type, path, abstract, upload_time, doctorID)VALUES ({},{},'{}','{}', '{}','{}','{}'," \
          "{});".format(appendix_dict.get(u"caseFirstID", 1),
                          appendix_dict.get(u"caseSecondID", 0),
                          appendix_dict.get(u"name", u""),
                          appendix_dict.get(u"type", u""),
                          appendix_dict.get(u"path", u""),
                          appendix_dict.get(u"abstract", u""),
                          appendix_dict.get(u"upload_time", u""),
                          appendix_dict.get(u"doctorID", 0)
                          )
    status = 1
    # print sql
    try:
        cursor_insert.execute(sql)
        con_insert.commit()
        cursor_insert.close()
        status = 0
    except Exception, e:
        print e
        con_insert.rollback()
        status = 1
    finally:
        con_insert.close()
        return status

def query_appendix(appendix_dict):
    """
    给定附件信息，查询对应的附件信息
    :param appendix_dict:｛
                u'caseFirstID': 1,
                u'caseSecondID': 0,
                u'name': u"化验图像",
                u'type': u'JPG',
                u'path': u'/appendix/化验图像',
                u'abstract': u'这是病人的化验图像，这是摘要信息'
            ｝
    :return:返回查询到的所有附件信息，用列别表示，[｛附件信息Ａ｝，｛附件信息Ｂ｝,......]
    """
    key_list = appendix_dict.keys()
    appendix_dict = {key: appendix_dict[key] for key in key_list if key in appendix_key}
    query_cx = conn()
    str_query = []
    for key, value in appendix_dict.items():
        if value != "":
            str_query.append("{} = '{}'".format(key, value))
    query = " and ".join(str_query)
    query_sql = "SELECT * FROM appendix WHERE {};".format(query)
    results_all = []
    # print query_sql
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'appendixID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'name'] = res[3]
            temp_dict[u'type'] = res[4]
            temp_dict[u'path'] = res[5]
            temp_dict[u'abstract'] = res[6]
            temp_dict[u'upload_time'] = res[7]
            temp_dict[u'doctorID'] = res[8]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all

def delete_appendix(appendix_dict):
    """
    """
    query_cx = conn()
    query_sql = "delete FROM appendix WHERE appendixID = {};".format(appendix_dict[u'appendixID'])
    results_all = []
    # print query_sql
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        query_cx.commit()
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all

def update_appendix(appendix_dict):
    """
    给定附件信息，更新对应的附件信息
    :param appendix_dict:｛
                u'appendixID': 1
                u'caseFirstID': 1,
                u'caseSecondID': 0,
                u'name': u"化验图像",
                u'type': u'JPG',
                u'path': u'/appendix/化验图像',
                u'abstract': u'这是病人的化验图像，这是摘要信息'
            ｝
    :return:返回查询到的所有附件信息，用列别表示，[｛附件信息Ａ｝，｛附件信息Ｂ｝,......]
    """
    query_cx = conn()
    str_query = []
    condition = "WHERE appendixID = {}".format(appendix_dict.get(u"appendixID", ""))
    for key, value in appendix_dict.items():
        if value != "" and key not in [u"caseFirstID", u"caseSecondID", u'appendixID'] and key in appendix_key:
            str_query.append("{} = '{}'".format(key, value))
    query = " , ".join(str_query)
    query_sql = "update appendix set {} {};".format(query, condition)
    # print query_sql
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        query_cx.commit()
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()

if __name__ == u"__main__":
    import json
    # create_cases()
    # for i in range(1,11):
    #     case_dict = {u'caseFirstID':i, u'caseSecondID':'0', u"disease_zy":u"失眠",u"disease_xy":u"失眠",u'first_symptom':u"失眠", u'second_symptom':u"不易入睡", u'look':u"面黄", u'listen':u"无",u'question':u"无", u'pulse':u"无", u'onset_time':'2017-11-20 15:47:28', u'case_date':'2017-11-20 15:47:28', u"patientID":1, u"doctorID":3}
    #     insert_cases(case_dict)
    # result = query_cases(cases_dict={"doctorID":3})
    # query = {"name":u"王小山","telephone":u"15612341234","disease_zy":u"失眠"}
    # result = search_cases({})

    # result = query_patient("1")
    # print len(result), json.dumps(result,ensure_ascii=False,encoding=u'utf-8')
    create_logs()
