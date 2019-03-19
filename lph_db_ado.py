#!/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
# -*- coding=utf-8 -*-
# name: db ado 数据库接口
# author: liupenghe
# date: 2016-08-11

import MySQLdb as mysql
import random
import re
import json

def connect_db():
    """
    获取数据库的连接
    :return: 数据库连接句柄
    """
    try:
        conn = mysql.connect(host='localhost', user='root', passwd='123456', db='robot_db', port=3306,
                             use_unicode=True, charset='utf8')
        return conn
    except mysql.Error, e:
        print "Mysql error {} : {}".format(e.args[0], e.args[1])



# conn = connect_db()

def select_unprocessed_patients(d_id):
    """
    选择出未被某位医生处理的病人信息
    :param d_id: 医生id
    :return: 患者信息列表
    """
    conn = connect_db()
    unprocessed_patients = []
    try:
        cur = conn.cursor()
        select_patients_str = u"select * from patients where p_d_id='{}'and p_is_processed='{}'".format(d_id, 0)
        cur.execute(select_patients_str)
        sql_results = cur.fetchall()
        for res in sql_results:
            patient = {
                "p_id": res[0],
                "p_name": res[3],
                "p_phone": res[1],
                "p_sex": res[4],
                "p_age": res[5],
                "p_info": res[6],
                "p_d_id": res[7],
                "p_is_processed": res[8],
                "p_date": res[10]
            }
            p_check = select_patient_check(str(res[0]))
            p_diagnosis = select_patient_diagnosis(str(res[0]))
            if len(p_check) != 0:
                unprocessed_patients.append((patient, p_check, p_diagnosis))
        cur.close()
        unprocessed_patients = sorted(unprocessed_patients, key=lambda item: item[0]["p_date"], reverse=True)
        return unprocessed_patients
    except Exception, e:
        print u"select unprocessed patients error {}".format(e.message)
    finally:
        print u"select unprocessed patients success - d_id = {}".format(d_id)
        conn.close()


def select_patient_by_id(p_id):
    """
    根据病人id寻找病人的信息
    :param p_id:
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        select_sql = u"select * from newPatient where patientID='{}';".format(p_id)
        print select_sql
        cur.execute(select_sql)
        res = cur.fetchone()
        patient = {
            "patientID": res[0],
            "p_name": res[1],
            "p_sex": res[2],
            "p_age": res[3],
            "p_telephone": res[4],
            "identityCardNum": res[5],
            "socialSecurityNum": res[6],
            "p_password": res[7]
        }
        print u"select patient by id success {}".format(patient)
        cur.close()
        return patient
    except Exception, e:
        print u"select patient by id error {}".format(e.message)
    finally:
        conn.close()


def select_latest_p_id(patient):
    """
    根据患者信息查询其最新记录的id
    :param patient:
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        select_sql = u"select * from patients where p_phone = '{}' order by p_date desc".format(patient["p_phone"])
        cur.execute(select_sql)
        res = cur.fetchone()
        cur.close()
        return res[0]
    except Exception, e:
        print u"select latest_p_id error"
    finally:
        conn.close()


def select_doctor_by_id(d_id):
    """
    根据医生的id查找医生
    :param d_id:
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        select_str = u"select * from doctors where d_id = '{}'".format(d_id)
        cur.execute(select_str)
        res = cur.fetchone()
        doctor = {
            "d_id": res[0],
            "d_phone": res[1],
            "d_name": res[3],
            "d_sex": res[4],
            "d_age": res[5],
            "d_department": res[6],
            "d_major": res[7],
        }
        print u"select patient by id success {}".format(doctor)
        cur.close()
        return doctor
    except Exception, e:
        print u"select patient by id error {}".format(e.message)
    finally:
        # pass
        conn.close()



def select_patient_id(patient):
    """
    根据病人信息查询其id
    :param patient: dict结构
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        select_sql = u"select p_id from patients where p_phone = '{}'".format(patient.get("p_phone", u""))
        cur.execute(select_sql)
        p_id = cur.fetchone()[0]
        cur.close()
        return p_id
    except Exception, e:
        print u"select patient id error {}".format(e.message)
    finally:
        # pass
        conn.close()


def insert_patient_info(patient):
    """
    插入病人数据
    :param patient: 字典格式
    :return:
    """
    conn = connect_db()

    try:
        cur = conn.cursor()
        insert_str = u"insert into " \
                     u"patients(p_phone, p_password, p_name, p_sex, p_age, p_info, p_d_id, p_is_processed, p_d_info, p_date)" \
                     u" values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            patient.get("p_phone", u""), patient.get("p_password", u""), patient.get("p_name", u""),
            patient.get("p_sex", u""), patient.get("p_age", u""), patient.get("p_info", u""),
            patient.get("p_d_id", u""),
            patient.get('p_is_processed', u""), patient.get("p_d_info", u""), patient.get("p_date", u"")
        )
        cur.execute(insert_str)
        conn.commit()
        cur.close()
        print u"insert patient info success - {}".format(patient)
    except Exception, e:
        print e.args
        print e.message
        print u"insert patients info error {}".format(e.message)
    finally:
        # pass
        conn.close()


def update_patient_d_id(p_id, p_d_id):
    """
    更新病人的就诊医生id
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        update_str = u"update patients set p_d_id = '{}' where p_id = '{}'".format(p_d_id, p_id)
        cur.execute(update_str)
        conn.commit()
        cur.close()
        print u"update patient doctor id success"
    except Exception, e:
        print u"update patient doctor id error {}".format(e.message)
    finally:
        # pass
        conn.close()


def update_patient_info(p_id, patient):
    """
    更新患者的信息
    :param p_id: 患者ID
    :param patient: dict格式
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        update_sql = u"update patients set p_info = '{}' where p_id = '{}'".format(
            patient.get("p_info", u""), p_id)
        cur.execute(update_sql)
        conn.commit()
        cur.close()
        print u"update patient info success - {}".format(patient)
    except Exception, e:
        print u"update patient info error {}".format(e.message)
    finally:
        # pass
        conn.close()


def update_patient_status(p_id, p_is_processed, p_d_info):
    """
    更新医生处理过的医生状态
    :param p_id: 患者ID
    :param p_is_processed: 是否已处理
    :param p_d_info: 医生处理意见
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        update_sql = u"update patients set p_is_processed = '{}', p_d_info= '{}' where p_id = '{}'".format(
            p_is_processed, p_d_info, p_id)
        cur.execute(update_sql)
        conn.commit()
        cur.close()
        print u"update patient status success - {}".format(p_is_processed)
    except Exception, e:
        print u"update patient status error {}".format(e.message)
    finally:
        # pass
        conn.close()


def select_doctor_info(doctor):
    """
    查询相应医生信息
    :param: doctor, dict格式
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        select_sql = u"select * from doctors where d_name = '{}' and d_password = '{}'".format(doctor["d_name"],
                                                                                               doctor["d_password"])
        cur.execute(select_sql)
        res = cur.fetchone()
        if res is None:
            return -1
        print u"select doctor info success! "
        return 1
    except Exception, e:
        print u"select doctor info error {}".format(e.message)
    finally:
        # pass
        conn.cursor()


def insert_doctor_info(doctor):
    """
    插入医生信息
    :param: doctor, dict格式
    :return:
    """
    conn = connect_db()
    try:
        if select_doctor_info(doctor) == 1:
            return -1
        cur = conn.cursor()
        insert_sql = u"insert into doctors(d_phone, d_password, d_name, d_sex, d_age, d_department, d_major) " \
                     u"values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(doctor["d_phone"],
                                                                                 doctor["d_password"],
                                                                                 doctor["d_name"],
                                                                                 doctor["d_sex"],
                                                                                 doctor["d_age"],
                                                                                 doctor["d_department"],
                                                                                 doctor["d_major"]
                                                                                 )
        cur.execute(insert_sql)
        conn.commit()
        cur.close()
        print u"insert doctor info success {}".format(doctor)
        return 1
    except Exception, e:
        print u"insert doctor info error {}".format(e.message)
    finally:
        # pass
        conn.close()


def search_user(user_phone, user_password, user_type):
    """
    查找用户是否再数据库中
    :param user_phone: 用户手机号
    :param user_password: 用户密码
    :param user_type: 用户类型
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        if user_type == 0:
            search_sql = u"select patientID, name from newPatient where telephone = '{}' and name = '{}'".format(
                user_phone, user_password)
        else:
            search_sql = u"select doctorID, name from newDoctor where telephone = '{}' and d_password = '{}'".format(
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
        conn.close()


def select_all_doctors_ids():
    """
    找出医生的数目
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        select_str = u"SELECT d_id FROM doctors"
        cur.execute(select_str)
        res = cur.fetchall()
        cur.close()
        print u"select doctor number success"
        print res
        return [int(tup[0]) for tup in res]
    except Exception, e:
        print u"select doctor number error {}".format(e.message)
    finally:
        # pass
        conn.close()


def insert_patient_check(p_check):
    """
    向checks表插入患者检查结果
    :param p_check: 字典格式
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        insert_sql = u"INSERT INTO checks(check_model, check_res, check_reason, c_p_id) " \
                     u"VALUES('{}', '{}', '{}', '{}')".format(
            p_check.get("check_model", u""), p_check.get("check_res", u""),
            p_check.get("check_reason", u""), p_check.get("c_p_id", u"")
        )
        cur.execute(insert_sql)
        conn.commit()
        cur.close()
        print u"insert patient check success"
    except Exception, e:
        print u"insert patient check error {}".format(e.message)
    finally:
        # pass
        conn.close()


def update_patient_check(p_check):
    """
    根据患者id更新检查表
    :param p_id:
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        update_sql = u"update checks set check_model = '{}', check_res = '{}', check_reason = '{}' where c_p_id = '{}'".format(
            p_check.get("check_model", u""), p_check.get("check_res", u""),
            p_check.get("check_reason", u""), p_check.get("c_p_id", u"")
        )
        cur.execute(update_sql)
        conn.commit()
        cur.close()
        print u"update patient checks success"
    except Exception, e:
        print u"update patient checks error {}".format(e.message)
    finally:
        # pass
        conn.close()


def select_patient_check(p_id):
    """
    根据患者的id查询患者的检查结果
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        select_sql = u"select * from checks where c_p_id = '{}'".format(p_id)
        cur.execute(select_sql)
        res = cur.fetchone()
        p_check = dict()
        if res is not None:
            p_check["check_model"] = res[1]
            p_check["check_res"] = res[2]
            p_check["check_reason"] = res[3]
            p_check["c_p_id"] = res[4]
        cur.close()
        print u"select patient check success"
        return p_check
    except Exception, e:
        print u"select patient check error {}".format(e.message)
    finally:
        # pass
        conn.close()


def insert_patient_diagnosis(p_diagnosis):
    """
    向diagnosis表中插入患者诊断结果
    :param p_diagnosis: 字典格式
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        insert_sql = u"INSERT INTO diagnosis(zd_model, zd_res, zd_reason, dia_p_id) " \
                     u"VALUES('{}', '{}', '{}', '{}')".format(
            p_diagnosis.get("zd_model", u""), p_diagnosis.get("zd_res", u""),
            p_diagnosis.get("zd_reason", u""), p_diagnosis.get("dia_p_id", u"")
        )
        cur.execute(insert_sql)
        conn.commit()
        cur.close()
        print u"insert patient diagnosis success"
    except Exception, e:
        print e.args, e.message
        print u"insert patient diagnosis error {}".format(e.message)
    finally:
        # pass
        conn.close()


def update_patient_diagnosis(p_diagnosis):
    """
    更新患者诊断结果
    :param p_diagnosis:
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        update_str = u"update diagnosis set zd_model = '{}', zd_res = '{}', zd_reason = '{}' where dia_p_id = '{}'".format(
            p_diagnosis.get("zd_model", u""), p_diagnosis.get("zd_res", u""),
            p_diagnosis.get("zd_reason", u""), p_diagnosis.get("dia_p_id", u"")
        )
        cur.execute(update_str)
        conn.commit()
        cur.close()
        print u"update patient diagnosis success"
    except Exception, e:
        print u"update patient diagnosis error {}".format(e.message)
        print e.args
    finally:
        # pass
        conn.close()


def select_patient_diagnosis(p_id):
    """
    根据患者id查询患者的诊断信息
    :param p_id:
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        select_sql = u"select * from diagnosis where dia_p_id = '{}'".format(p_id)
        cur.execute(select_sql)
        res = cur.fetchone()
        p_diagnosis = dict()
        if res is not None:
            p_diagnosis["zd_model"] = res[1]
            p_diagnosis["zd_res"] = res[2]
            p_diagnosis["zd_reason"] = res[3]
            p_diagnosis["dia_p_id"] = res[4]
        cur.close()
        print u"select patient diagnosis success"
        return p_diagnosis
    except Exception, e:
        print u"select patient diagnosis error {}".format(e.message)
    finally:
        # pass
        conn.close()


def search_patient_results(p_phone):
    """
    患者查询其处理结果
    :param p_phone:
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        select_str = u"select * from patients where p_phone = '{}'".format(p_phone)
        cur.execute(select_str)
        res = cur.fetchone()
        if res is not None:
            patient = {
                "p_id": res[0],
                "p_name": res[3],
                "p_phone": res[1],
                "p_sex": res[4],
                "p_age": res[5],
                "p_info": res[6],
                "p_d_id": res[7],
                "p_is_processed": res[8],
                "p_date": res[10]
            }
            p_check = select_patient_check(patient.get("p_id"))
        else:
            patient = dict()
            p_check = dict()
        cur.close()
        print u"search patient results success"
        return patient, p_check
    except Exception, e:
        print u"search patient results error {}".format(e.message)
    finally:
        # pass
        conn.close()



def insert_invitation_code(create_id,content):
    """
    插入邀请码
    :param create_id:
    :param content:
    :return:
    """
    # con_insert = connect_db()
    conn = connect_db()
    cursor_insert = conn.cursor()
    sql = """INSERT INTO Invitation_code(create_user,code_content,flag)
              VALUES ({},'{}',0)""".format(create_id, content)
    try:
        cursor_insert.execute(sql)
        conn.commit()
        cursor_insert.close()
    except:
        conn.rollback()
    finally:
        # pass
        conn.close()


def gen_code():
    """
    随机产生邀请码
    :return:
    """
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(6):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt

def query(create_id, content):
    """
    查询生成的邀请码是否已存在
    :param create_id:
    :param content:
    :return:
    """
    conn = connect_db()
    sselect_sql = "SELECT * FROM Invitation_code WHERE create_user ={} and code_content = '{}' and flag = 0".format(create_id, content)
    try:
        cursor = conn.cursor()
        cursor.execute(sselect_sql)
        results = cursor.fetchall()
        if len(results) > 0:
            flag = 1
        else:
            flag = 0
        cursor.close()
        return flag
    except Exception ,e:
        print e
    finally:
        # pass
        conn.close()



def query_code(create_id, content):
    """
    查询用户数输入的邀请码是否有效
    :param create_id:
    :param content:
    :return:
    """
    conn = connect_db()
    sselect_sql = "SELECT * FROM Invitation_code WHERE create_user ={} and code_content = '{}' and flag = 0".format(create_id, content)
    try:
        cursor = conn.cursor()
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
        conn.close()


def create_code(create_id):
    """
    用户产生邀请码
    :param create_id:
    :return:
    """
    content_code = gen_code()
    flag = query(create_id, content_code)
    while(1):
        if flag == 1:
            content_code = gen_code()
            flag = query(create_id, content_code)
        elif flag == 0:
            insert_invitation_code(create_id, content_code)
            return content_code



def update_use_code(create_id, content):
    """
    更新使用了的邀请码
    :param create_id:
    :param content:
    :return:
    """
    conn = connect_db()
    update_sql = u"UPDATE Invitation_code SET flag = 1 WHERE create_user = {} and code_content = '{}' and flag = 0 ".format(create_id, content)
    print update_sql
    try:
        cursor = conn.cursor()
        cursor.execute(update_sql)
        conn.commit()
    except Exception ,e:
        print e
        conn.rollback()
    finally:
        # pass
        conn.close()


def select_id_by_phone(phone):
    """
    根据用户手机号查询其id
    :param phone: str
    :return:
    """
    conn = connect_db()
    try:
        cursor = conn.cursor()
        sql1 = u"select * from patients where p_phone = '{}'".format(phone)
        cursor.execute(sql1)
        res1 = cursor.fetchone()
        if res1 is not None and len(res1) != 0:
            cursor.close()
            print res1[0]
            return res1[0]
        sql2 = u"select * from doctors where d_phone = '{}'".format(phone)
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
        conn.close()


def query_zhenduan_doctor(doc_id):
    conn = connect_db()
    sselect_sql = "SELECT * FROM zhenduan_doctor WHERE doc_id ={} ".format(doc_id)
    try:
        cursor = conn.cursor()
        cursor.execute(sselect_sql)
        results = cursor.fetchall()
        cursor.close()
        if len(results) > 0:
            return results
        else:
            return []
    except Exception ,e:
        print e
    finally:
        conn.close()
        return []


def insert(doc_id,p_sex,p_age,p_zhusu,p_xbs, p_tgjc , p_hyjc,
            p_aljl, p_fxsm, p_zlxx , d_model_name ,d_model_result,d_model_explain ):
    conn = connect_db()
    cursor_insert = conn.cursor()
    sql = """INSERT INTO zhenduan_doctor(doc_id, p_sex, p_age, p_zhusu, p_xbs, p_tgjc, p_hyjc,
p_aljl, p_fxsm, p_zlxx, d_model_name, d_model_result, d_model_explain)
VALUES ({},{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(
        doc_id, p_sex, p_age, p_zhusu, p_xbs, p_tgjc, p_hyjc,
        p_aljl, p_fxsm, p_zlxx, d_model_name, d_model_result, d_model_explain)
    try:
        print sql
        cursor_insert.execute(sql)
        conn.commit()
        cursor_insert.close()
        flag = 1
    except:
        flag = 0
        conn.rollback()
    finally:
        conn.close()
        return flag


def query_all_binglis():
    """
    查询所有的病例
    :return:
    """
    conn = connect_db()
    sselect_sql = "SELECT * FROM binglis_all"
    res_binglis = []
    try:
        cursor = conn.cursor()
        cursor.execute(sselect_sql)
        results = cursor.fetchall()
        for res in results:
            each_bingli = {}
            each_bingli[u'编号'] = res[0]
            each_bingli[u'姓名'] = res[1]
            each_bingli[u'年龄']= res[2]
            each_bingli[u'既往史']= res[3]
            each_bingli[u'患者编号']= res[4]
            each_bingli[u'处理']= res[5]
            each_bingli[u'服药']= res[6]
            each_bingli[u'主诉']= res[7]
            each_bingli[u'体格检查']= res[8]
            each_bingli[u'现病史']= res[9]
            each_bingli[u'初步诊断']= res[10]
            each_bingli[u'日期']= res[11]
            each_bingli[u'注意']= res[12]
            each_bingli[u'辅助检查']= res[13]
            each_bingli[u'科室']= res[14]
            each_bingli[u'性别']= res[15]
            each_bingli[u'药物过敏史']= res[16]
            each_bingli[u'个人及家族史']= res[17]
            res_binglis.append(each_bingli)
        cursor.close()
    except Exception, e:
        print e
    finally:
        conn.close()
        return res_binglis


def query_one_bingli(huanzhebianhao):
    """
    查询1个病例
    :param huanzhebianhao:
    :return:
    """
    conn = connect_db()
    sselect_sql = "SELECT * FROM binglis_all WHERE  hzbh = '{}'".format(huanzhebianhao)
    each_bingli = {}
    try:
        cursor = conn.cursor()
        cursor.execute(sselect_sql)
        results = cursor.fetchall()
        for res in results:
            each_bingli[u'编号'] = res[0]
            each_bingli[u'姓名'] = res[1]
            each_bingli[u'年龄']= res[2]
            each_bingli[u'既往史']= res[3]
            each_bingli[u'患者编号']= res[4]
            each_bingli[u'处理']= res[5]
            each_bingli[u'服药']= res[6]
            each_bingli[u'主诉']= res[7]
            each_bingli[u'体格检查']= res[8]
            each_bingli[u'现病史']= res[9]
            each_bingli[u'初步诊断']= res[10]
            each_bingli[u'日期']= res[11]
            each_bingli[u'注意']= res[12]
            each_bingli[u'辅助检查']= res[13]
            each_bingli[u'科室']= res[14]
            each_bingli[u'性别']= res[15]
            each_bingli[u'药物过敏史']= res[16]
            each_bingli[u'个人及家族史']= res[17]
            break
        cursor.close()
    except Exception, e:
        print e
    finally:
        conn.close()
        return each_bingli


def search_bingli_by_keywords(keywords):
    """
    根据关键词找出所有的病例
    :param keywords:
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        sql = u"select * from binglis_all where cbzd like '%{}%'".format(keywords)
        cur.execute(sql)
        results = cur.fetchall()
        res_binglis = []
        for res in results:
            each_bingli = {}
            each_bingli[u'编号'] = res[0]
            each_bingli[u'姓名'] = res[1]
            each_bingli[u'年龄'] = res[2]
            each_bingli[u'既往史'] = res[3]
            each_bingli[u'患者编号'] = res[4]
            each_bingli[u'处理'] = res[5]
            each_bingli[u'服药'] = res[6]
            each_bingli[u'主诉'] = res[7]
            each_bingli[u'体格检查'] = res[8]
            each_bingli[u'现病史'] = res[9]
            each_bingli[u'初步诊断'] = res[10]
            each_bingli[u'日期'] = res[11]
            each_bingli[u'注意'] = res[12]
            each_bingli[u'辅助检查'] = res[13]
            each_bingli[u'科室'] = res[14]
            each_bingli[u'性别'] = res[15]
            each_bingli[u'药物过敏史'] = res[16]
            each_bingli[u'个人及家族史'] = res[17]
            res_binglis.append(each_bingli)
        cur.close()
        return res_binglis
    except Exception, e:
        print u"根据关键词查询error"
    finally:
        conn.close()


def find_cbzd(cbzd_str):
    diseases = []
    original_str = re.sub("[,.；，：。？、?:;]+".decode("utf8"), "$".decode("utf8"), cbzd_str)
    items = original_str.split(u"$")
    for item in items:
        if item is not None and item != u"":
            dis_label = item.strip()
            true_label = fuzzy_match(dis_label)
            diseases.append(true_label)

    return diseases


def fuzzy_match(dis_name):
    """
    将结果集中的同一个疾病的不同疾病名映射为痛一个病
    :param: dis_name, 某一疾病名
    :return:
    """
    if dis_name in [u"支气管肺炎（小叶型肺炎）", u"支气管肺炎（小叶性肺炎）", u"支原体性肺炎", u"小叶性肺炎",
                    u"小叶型肺炎", u"肺炎", u"肺炎（左下）", u"新生儿肺炎", u"支气管肺炎"]:
        return u"支气管肺炎"
    elif dis_name in [u"支气管炎", u"支气管炎（主）", u"急性支气管炎"]:
        return u"支气管炎"
    elif dis_name in [u"气管炎", u""
                              u"气管炎（主）", u"急性气管炎"]:
        return u"气管炎"
    elif dis_name in [u"喘息性支气管炎", u"急性喘息性支气管炎"]:
        return u"喘息性支气管炎"
    elif dis_name in [u"发热", u"感染性发热"]:
        return u"发热"
    elif dis_name in [u"呼吸道感染", u"上呼吸道感染"]:
        return u"呼吸道感染"
    elif dis_name in [u"腹痛", u"腹痛待查"]:
        return u"腹痛"
    elif dis_name in [u"化脓性扁桃体炎", u"急性化脓性扁桃体炎", u"急性化脓性扁桃腺炎"]:
        return u"化脓性扁桃体炎"
    elif dis_name in [u"肠炎", u"急性肠炎", u"婴儿肠炎"]:
        return u"肠炎"
    elif dis_name in [u"胃肠炎", u"急性胃肠炎"]:
        return u"胃肠炎"
    elif dis_name in [u"胃炎", u"急性胃炎"]:
        return u"胃炎"
    elif dis_name in [u"粒细胞缺乏", u"粒细胞缺乏症", u"中性粒细胞缺乏症", u"中性粒细胞减少症"]:
        return u"粒细胞缺乏症"
    elif dis_name in [u"喉炎", u"急性喉炎", u"慢性喉炎"]:
        return u"喉炎"
    elif dis_name in [u"急性扁桃体", u"急性扁桃体炎"]:
        return u"急性扁桃体炎"
    elif dis_name in [u"婴儿的骨软化性佝偻病"]:
        return u"骨软化性佝偻病"
    elif dis_name in [u"急性细菌性感染", u"细菌感染", u"细菌性感染"]:
        return u"细菌性感染"
    elif dis_name in [u"急性病毒感染", u"病毒感染"]:
        return u"病毒性感染"
    elif dis_name in [u"EB病毒感染", u"E-B病毒感染"]:
        return u"EB病毒感染"
    elif dis_name in [u"急性淋巴结炎", u"淋巴结炎"]:
        return u"淋巴结炎"
    elif dis_name in [u"颈淋巴结炎", u"急性颈淋巴结炎", u"急性颈部淋巴结炎"]:
        return u"颈淋巴结炎"
    elif dis_name in [u"阑尾炎", u"急性阑尾炎"]:
        return u"阑尾炎"
    elif dis_name in [u"疱疹性咽炎", u"疹性咽峡炎"]:
        return u"疹性咽峡炎"
    else:
        return dis_name

def query_fanwei(first,end):
    conn = connect_db()
    sselect_sql = "SELECT * FROM binglis_all WHERE riqi >='{}' and riqi <= '{}' order by riqi".format(first, end)
    res_binglis = []
    try:
        cursor = conn.cursor()
        cursor.execute(sselect_sql)
        results = cursor.fetchall()
        for res in results:
            each_bingli = {}
            each_bingli[u'编号'] = res[0]
            each_bingli[u'年龄'] = res[1]
            each_bingli[u'年龄']= res[2]
            each_bingli[u'既往史']= res[3]
            each_bingli[u'患者编号']= res[4]
            each_bingli[u'处理']= res[5]
            each_bingli[u'服药']= res[6]
            each_bingli[u'主诉']= res[7]
            each_bingli[u'体格检查']= res[8]
            each_bingli[u'现病史']= res[9]
            each_bingli[u'初步诊断']= res[10]
            each_bingli[u'日期']= res[11]
            each_bingli[u'注意']= res[12]
            each_bingli[u'辅助检查']= res[13]
            each_bingli[u'科别']= res[14]
            each_bingli[u'性别']= res[15]
            each_bingli[u'药物过敏史']= res[16]
            each_bingli[u'个人及家族史']= res[17]
            res_binglis.append(each_bingli)
        cursor.close()
    except Exception, e:
        print e
    finally:
        conn.close()
        return res_binglis

def query_fanwei_s(first,end):
    res_binglis = query_fanwei(first,end)
    result = {}
    for res in res_binglis:
        # print res[u'药物过敏史']
        cbzd = res[u'初步诊断']
        try:
            cbzd = cbzd.decode('utf-8')
        except:
            cbzd = cbzd.decode('gbk')
        # print type(cbzd)
        # print [cbzd,cbzd]
        # print len(cbzd)
        dis_list = find_cbzd(cbzd)
        # dis_list = cbzd.split(u'，')
        # print len(dis_list)

        for each_dis in dis_list:
            if each_dis not in result.keys():
                result[each_dis] = 1
            else:
                result[each_dis] += 1
    return result


def save_test_bingli(test_dict):
    """
    保存测试病例
    :param test_dict:
    :return:
    """
    conn = connect_db()
    blbh = test_dict[u'病例编号']
    doc_id = test_dict[u'医生编号']
    p_sex = test_dict[u'性别']
    p_age = test_dict[u'年龄']
    p_zhusu = test_dict[u'主诉']
    p_xbs = test_dict[u'现病史']
    p_tgjc = test_dict[u'体格检查']
    p_hyjc = test_dict[u'化验检测']
    p_aljl = test_dict[u'案例结论']
    p_fxsm = test_dict[u'分析说明']
    p_zlxx = test_dict[u'治疗信息']
    res_jiancha = test_dict[u'检查结果']
    res_zhenduan = test_dict[u'诊断结果']
    test_type = test_dict[u'测试类型']
    test_time = test_dict[u'时间戳']
    cursor_insert = conn.cursor()
    sql = u"""INSERT INTO save_test_binglis(blbh,doc_id, p_sex, p_age, p_zhusu, p_xbs, p_tgjc, p_hyjc,p_aljl, p_fxsm, p_zlxx,res_jiancha, res_zhenduan, test_type, test_time)VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(blbh, doc_id, p_sex, p_age, p_zhusu, p_xbs, p_tgjc, p_hyjc, p_aljl, p_fxsm, p_zlxx, res_jiancha, res_zhenduan, test_type, test_time)
    try:
        cursor_insert.execute(str(sql))
        conn.commit()
        cursor_insert.close()
        flag = 1
    except Exception, e:
        print e
        conn.rollback()
        flag = 0
    finally:
        conn.close()
    return flag


#
def select_all_doctors():
    """
    从数据库种找出所有的医生
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        sql = u"select * from doctors"
        cur.execute(sql)
        resulets = cur.fetchall()
        doctors = []
        for res in resulets:
            doc = {
                u"d_id": res[0],
                u"d_phone": res[1],
                u"d_name": res[3],
                u"d_sex": res[4],
                u"d_age": res[5],
                u"d_major": res[7]
            }
            doctors.append(doc)
        cur.close()
        return doctors
    except Exception, e:
        print "select all doctors error"
    finally:
        conn.close()
#

def insert_huayan(ph_info):
    """
    插入化验结果
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        sql = u"insert into patient_huayan(ph_info, ph_pid) VALUES ('{}', {})".format(ph_info[u"ph_info"], ph_info[u"ph_pid"])
        cur.execute(sql)
        conn.commit()
        cur.close()
        print u"insert patient huayan success"
    except Exception, e:
        print e.args
        print "insert patient huayan error"
    finally:
        conn.close()



def select_huayan(ph_pid):
    """
    根据患者ID查询其化验结果
    :param ph_pid:
    :return:
    """
    conn = connect_db()
    try:
        cur = conn.cursor()
        sql = u"select * from patient_huayan where ph_pid = {} ORDER BY ph_id DESC".format(ph_pid)
        cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        if res is not None and len(res) > 0:
            return res[1]
    except Exception, e:
        print e.args
        print "select huayan error"
    finally:
        conn.close()

def main():
    # select_unprocessed_patients(u"王医生")
    # patient = {
    #     "p_name": u"张小明",
    #     "p_sex": 0,
    #     "p_age": 2,
    #     "p_info": u"咳嗽, 发热",
    #     "p_pred_check": u"血检, 尿急",
    #     "p_pred_diagnosis": u"支气管肺炎",
    #     "p_d_id": 1,
    #     "p_is_processed": 0
    # }
    # update_patient_info(1, patient)
    # insert_patient_info(patient)
    # select_unprocessed_patients(u"王医生")

    # print create_code(3)

    # binglis = search_bingli_by_keywords(u"呼吸道感染")
    # print len(binglis)
    # print binglis[0]

    # doctor = {
    #     "d_phone": u"13812341234",
    #     "d_name": u"郑医生",
    #     "d_password": u"123456",
    #     "d_age": 32,
    #     "d_sex": 0,
    #     "d_department": u"儿科",
    #     "d_major": u"小儿发热"
    # }
    # insert_doctor_info(doctor)

    patient = {
        "p_phone": u"13612341234"
    }
    print select_latest_p_id(patient)


if __name__ == "__main__":
    main()
