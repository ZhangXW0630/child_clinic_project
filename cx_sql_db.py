# -*- coding:utf-8 -*-
from MySQLdb import connect
import datetime

def conn():
    conn_cx = connect(host='127.0.0.1', user='root', passwd='123456', db='robot_db', port=3306, charset="utf8")
    return conn_cx

patient_key = [u'patientID', u'name', u'sex', u'age', u'telephone', u'identityCardNum', u'socialSecurityNum']
doctor_key = [u'doctorID', u'name', u'sex', u'age', u'telephone', u'identityCardNum', u'indication', u'department', u"remen_dict", u"tigejiancha_dict"]
case_key = [u'caseID', u'caseFirstID', u'caseSecondID', u'chiefComplaint', u'HPI', u'physicalExamination', u'chemicalExamination',
            u'differentialDiagnosis', u'treatment', u'predictionResults',  u'auxInfo',   u'patientID', u'caseDate', u'isFinish',
            u'check_recommend', u'zd_model', u'zd_res', u'zd_reason', u"recommend_medicine",u"category", u"disease_prob"]
DCRelation_key = [u'relationId', u'caseId', u'caseSecondID', u'doctorID', u'doctorRole', u'doctorComment', u'caseFirstID', u'comment_time']
medicine_key = [u'medicineID', u'medicineSystemID']
treatment_key = [u'treatmentSystemID', u'treatmentID']
appendix_key = [u'appendixID', u'caseFirstID', u'caseSecondID', u'name', u'type', u'path', u'abstract', u'upload_time']
CARelation_key = [u'CARelationID', u'caseFirstID', u'caseSecondID', u'name', u'type', u'info', u'assayID']
dianxuan_key = [u"dianxuanID",u"doctorID",u"category",u"remen_dict",u"tigejiancha_dict"]

new_case_length = 21
new_patient_length = 10

def query_patient(patient_dict):
    """
    给定患者的信息字典，其中的key与数据库中patient表对应，除了doctorId不可有其他key
    :param patient_dict:｛
            "name":"王小山",
            "identityCardNum":"王小山",
            "socialSecurityNum":"15612341234",
            "telephone":"15612341234",
            "doctorID" : 1,
            ｝
    :return:返回查询到的所有患者档案信息，用列别表示，[｛患者Ａ信息｝，｛患者Ｂ信息｝,......]
    """
    key_list = patient_dict.keys()
    patient_dict = {key: patient_dict[key] for key in key_list if key in patient_key}
    query_cx = conn()
    str_query = []
    for key, value in patient_dict.items():
        if value != "" and key not in [u"doctorID", u"chiefComplaint"]:
            str_query.append("{} = '{}'".format(key, value))
    if len(str_query) == 0:
        query_sql = "SELECT * FROM newPatient"
    else:
        query = " and ".join(str_query)
        query_sql = "SELECT * FROM newPatient WHERE {}".format(query)

    results_all = []
    # print query_sql
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'patientID'] = res[0]
            temp_dict[u'name'] = res[1]
            temp_dict[u'sex'] = res[2]
            temp_dict[u'age'] = res[3]
            temp_dict[u'telephone'] = res[4]
            temp_dict[u'identityCardNum'] = res[5]
            temp_dict[u'socialSecurityNum'] = res[6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_DCRelation_from_doctor(doctorid):
    """
    根据医生ＩＤ查询所有的医生病人病例关系表
    :param doctorid:　医生类别[docid1,docid2,......]
    :return:[{
            "relationID" :,
            "caseID":,
            "caseSecondID":,
            "doctorID":,
            "doctorRole"：,
            "doctorComment"
         }, {},.....]
    """
    query_cx = conn()
    str_query = []
    for eachid in doctorid:
        if eachid != "":
            str_query.append("'{}'".format(eachid))
    if len(str_query) == 0:
        query_sql = "select * from newDCRelation"
    else:
        query = " , ".join(str_query)
        query_sql = "select * from newDCRelation where doctorId in ({});".format(query)
    results_all = []
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'relationID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'doctorID'] = res[3]
            temp_dict[u'doctorRole'] = res[4]
            temp_dict[u'doctorComment'] = res[5]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_case_from_patientid(patientid):
    """
　　　通过patientid查询case记录
    :param patientid:[id1,id2,.....]
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    str_query = []
    for eachid in patientid:
        if eachid != u"" :
            str_query.append("'{}'".format(eachid))
    query = " , ".join(str_query)
    query_sql = "select * from newCase, newPatient where caseSecondID = 0 and  newPatient.patientID " \
                " in ({}) and newCase.patientID = newPatient.patientID;".format(query)
    results_all = []

    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]
            temp_dict[u'patientID'] = res[new_case_length+0]
            temp_dict[u'name'] = res[new_case_length+1]
            temp_dict[u'sex'] = res[new_case_length+2]
            temp_dict[u'age'] = res[new_case_length+3]
            temp_dict[u'telephone'] = res[new_case_length+4]
            temp_dict[u'identityCardNum'] = res[new_case_length+5]
            temp_dict[u'socialSecurityNum'] = res[new_case_length+6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all



def query_case_from_caseid(caseid):
    """
　　　通过caseid查询case记录
    :param caseid:[1,id2,.....]
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    str_query = []
    for eachid in caseid:
        if eachid != "":
            str_query.append("'{}'".format(eachid))
    query = " , ".join(str_query)
    query_sql = "select * from newCase, newPatient where  caseSecondID = 0 and caseFirstID in ({}) and newCase.patientID = newPatient.patientId ORDER BY caseDate;".format(query)
    results_all = []

    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'patientID'] = res[11]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]
            temp_dict[u'patientID'] = res[new_case_length+0]
            temp_dict[u'name'] = res[new_case_length+1]
            temp_dict[u'sex'] = res[new_case_length+2]
            temp_dict[u'age'] = res[new_case_length+3]
            temp_dict[u'telephone'] = res[new_case_length+4]
            temp_dict[u'identityCardNum'] = res[new_case_length+5]
            temp_dict[u'socialSecurityNum'] = res[new_case_length+6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_case_by_case_first_and_secondID(case_dict):
    """
    根据病例的firstID和secondID查询病例
    :return:
    """
    query_cx = conn()
    query_sql = "select * from newCase, newPatient, newDCRelation where  newCase.caseFirstID = {} and newCase.caseSecondID = {} and newCase.patientID = newPatient.patientID  and newCase.caseFirstID = newDCRelation.caseFirstID and newCase.caseSecondID = newDCRelation.caseSecondID ORDER BY caseDate;".format(
        case_dict.get(u"caseFirstID"), case_dict.get(u"caseSecondID"))
    results_all = []

    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]
            temp_dict[u'patientID'] = res[20]
            temp_dict[u'name'] = res[21]
            temp_dict[u'sex'] = res[22]
            temp_dict[u'age'] = res[23]
            temp_dict[u'telephone'] = res[24]
            temp_dict[u'identityCardNum'] = res[25]
            temp_dict[u'socialSecurityNum'] = res[26]
            temp_dict[u'doctorRole'] = res[new_case_length + new_patient_length + 4]
            temp_dict[u"doctorComment"] = res[new_case_length + new_patient_length + 5]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_case(case_dict):
    """s"""
    key_list = case_dict.keys()
    case_dict = {key: case_dict[key] for key in key_list if key in case_key}
    query_cx = conn()
    str_query = []
    for key, value in case_dict.items():
        if value != "":
            str_query.append("{} = '{}'".format(key, value))
    query = " and ".join(str_query)
    query_sql = "select * from newCase where {};".format(query)
    results_all = []

    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'patientID'] = res[11]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'disease_prob'] = res[20]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_case_patient(case_dict):
    """
　　　通过case_dict查询case记录
    :param case_dict:key 为case表中所有可能的字段
            {
                "caseID": ,
                "caseSecondID": ,
                "chiefComplaint": ,
                "isFinish": ,
            }
    :return:[{病例信息，患者信息},{},{}]
    """
    key_list = case_dict.keys()
    case_dict = {key: case_dict[key] for key in key_list if key in case_key}
    query_cx = conn()
    str_query = []
    for key, value in case_dict.items():
        if value != "":
            str_query.append("{} = '{}'".format(key, value))
    query = " and ".join(str_query)
    query_sql = "select * from newCase, newPatient where {} AND  newCase.patientID = newPatient.patientID;".format(query)
    results_all = []

    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'patientID'] = res[11]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]
            temp_dict[u'patientID'] = res[new_case_length+0]
            temp_dict[u'name'] = res[new_case_length+1]
            temp_dict[u'sex'] = res[new_case_length+2]
            temp_dict[u'age'] = res[new_case_length+3]
            temp_dict[u'telephone'] = res[new_case_length+4]
            temp_dict[u'identityCardNum'] = res[new_case_length+5]
            temp_dict[u'socialSecurityNum'] = res[new_case_length+6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_case_from_caseid_and_patientid(caseid, patientid):
    """
　　　通过caseid 和　patientid查询case记录，查询满足这两个约束的病例
    :param　caseid:[id1,id2,.....]
            patientid:[id1,id2,.....]
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    str_query = []
    for eachid in caseid:
        if eachid != "":
            str_query.append("'{}'".format(eachid))
    query = " , ".join(str_query)

    str_patient_query = []
    for eachid in patientid:
        if eachid != "":
            str_patient_query.append("'{}'".format(eachid))
    patient_query = " , ".join(str_patient_query)

    query_sql = "select * from newCase, newPatient where caseSecondID = 0 and caseFirstID in ({}) and newPatient.patientID in ({}) and newCase.patientID in ({}) and newCase.patientID = newPatient.patientID ORDER BY caseDate;".format(query, patient_query, patient_query)
    results_all = []

    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]
            temp_dict[u'patientID'] = res[new_case_length+0]
            temp_dict[u'name'] = res[new_case_length+1]
            temp_dict[u'sex'] = res[new_case_length+2]
            temp_dict[u'age'] = res[new_case_length+3]
            temp_dict[u'telephone'] = res[new_case_length+4]
            temp_dict[u'identityCardNum'] = res[new_case_length+5]
            temp_dict[u'socialSecurityNum'] = res[new_case_length+6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_case_from_caseid_and_patientid_secondID(caseid, patientid, patient_dict = {}):
    """
　　　通过caseid 和　patientid查询case记录，查询满足这两个约束的病例
    :param　caseid:[id1,id2,.....]
            patientid:[id1,id2,.....]
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    str_query = []
    for eachid in caseid:
        if eachid != "":
            str_query.append("'{}'".format(eachid))
    query = " , ".join(str_query)

    str_patient_query = []
    for eachid in patientid:
        if eachid != "":
            str_patient_query.append("'{}'".format(eachid))
    patient_query = " , ".join(str_patient_query)

    # query_sql = "select * from newCase, newPatient where caseFirstID in ({}) and newPatient.patientID in ({}) and newCase.patientID in ({}) and newCase.patientID = newPatient.patientID ORDER BY caseDate;".format(query, patient_query, patient_query)
    # results_all = []
    date_list = []
    startdate = patient_dict.get(u'startdate', u"")
    enddate = patient_dict.get(u'enddate', u"")
    if startdate != u"":
        date_list.append(" caseDate >= '{}' ".format(startdate))
    if enddate != u"":
        date_list.append(" caseDate <= '{}' ".format(enddate + u' 23:59:59'))
    # print date_list
    if len(date_list) > 0:
        query_sql = "select * from newCase, newPatient where caseFirstID in ({}) and newPatient.patientID in ({}) and {} and newCase.patientID in ({}) and newCase.patientID = newPatient.patientID ORDER BY caseDate;".format(
            query, patient_query, 'and'.join(date_list), patient_query)

    else:
        query_sql = "select * from newCase, newPatient where caseFirstID in ({}) and newPatient.patientID in ({}) and newCase.patientID in ({}) and newCase.patientID = newPatient.patientID ORDER BY caseDate;".format(
            query, patient_query, patient_query)
    results_all = []

    # print query_sql

    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]
            temp_dict[u'patientID'] = res[new_case_length+0]
            temp_dict[u'name'] = res[new_case_length+1]
            temp_dict[u'sex'] = res[new_case_length+2]
            temp_dict[u'age'] = res[new_case_length+3]
            temp_dict[u'telephone'] = res[new_case_length+4]
            temp_dict[u'identityCardNum'] = res[new_case_length+5]
            temp_dict[u'socialSecurityNum'] = res[new_case_length+6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_case_from_caseid_new(caseid):
    """
　　　通过caseid 和　patientid查询case记录，查询满足这两个约束的病例
    :param　caseid:[id1,id2,.....]
            patientid:[id1,id2,.....]
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    str_query = []
    for eachid in caseid:
        if eachid != "":
            str_query.append("'{}'".format(eachid))
    query = " , ".join(str_query)
    query_sql = "select * from newCase, newPatient  where caseFirstID in ({}) and newCase.patientID = newPatient.patientID ORDER BY caseDate;".format(query)
    results_all = []
    # print query_sql
    comment_all = []
    # print new_case_length
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            zhuzhi, doctorComment, res_all = query_newDCRelation_for_doctor_case({u'caseFirstID': res[1], u'caseSecondID': res[2]})
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]
            temp_dict[u'patientID'] = res[new_case_length+0]
            temp_dict[u'name'] = res[new_case_length+1]
            temp_dict[u'sex'] = res[new_case_length+2]
            temp_dict[u'age'] = res[new_case_length+3]
            temp_dict[u'telephone'] = res[new_case_length+4]
            temp_dict[u'identityCardNum'] = res[new_case_length+5]
            temp_dict[u'socialSecurityNum'] = res[new_case_length+6]
            temp_dict[u'zhuzhi'] = zhuzhi
            temp_dict[u'doctorComment'] = doctorComment
            # temp_dict[u'comment_all'] = res_all
            results_all.append(temp_dict)
            comment_all.extend(res_all)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        comment_all = sorted(comment_all, key=lambda item:item[u'commentTime'])
        print u'comment_all', len(comment_all)
        return results_all, comment_all


def query_allcase_from_doctorid(doctorid):
    """
    给予医生ＩＤ查询这个医生的全部病例
    :param doctorid:
    :return:[{病例信息，患者信息},{},{}]
    """
    DCR = query_DCRelation_from_doctor([doctorid])
    caseid = []
    res_all = []
    for each in DCR:
        if each[u'caseFirstID'] not in caseid:
            caseid.append(each[u'caseFirstID'])
    if len(caseid) > 0:
        res_all = query_case_from_caseid(caseid)
    return res_all


def query_allcase(doctorid):
    """
    给予医生ＩＤ查询这个医生的全部病例
    :param doctorid:
    :return:[{病例信息，患者信息},{},{}]
    """
    DCR = query_DCRelation_from_doctor([doctorid])
    caseid = []
    res_all = []
    for each in DCR:
        if each[u'caseFirstID'] not in caseid:
            caseid.append(each[u'caseFirstID'])
    if len(caseid) > 0:
        res_all = query_case_from_caseid(caseid)
    # res_all = query_allcase_sub()
    # print len(res_all)
    return res_all

def query_allcase_of_category(doctorid,category=0):
    """
    给予医生ＩＤ查询这个医生的全部病例
    :param doctorid:
    :return:[{病例信息，患者信息},{},{}]
    """
    DCR = query_DCRelation_from_doctor([doctorid])
    caseid = []
    res_all = []
    for each in DCR:
        if each[u'caseFirstID'] not in caseid:
            caseid.append(each[u'caseFirstID'])
    # if len(caseid) > 0:
    #     res_all = query_case_from_caseid(caseid)
    res_all = query_allcase_sub(category)
    # print len(res_all)
    return res_all


def query_allcase_sub(category):
    """
　　query_allcase函数的子函数，不会再外部调用
    :param caseid:[1,id2,.....]
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    query_sql = "select * from newCase, newPatient where  caseSecondID = 0 AND newCase.category = {} and newCase.patientID = newPatient.patientId ORDER BY caseDate;".format(category)
    results_all = []

    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'patientID'] = res[11]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]
            temp_dict[u'patientID'] = res[new_case_length+0]
            temp_dict[u'name'] = res[new_case_length+1]
            temp_dict[u'sex'] = res[new_case_length+2]
            temp_dict[u'age'] = res[new_case_length+3]
            temp_dict[u'telephone'] = res[new_case_length+4]
            temp_dict[u'identityCardNum'] = res[new_case_length+5]
            temp_dict[u'socialSecurityNum'] = res[new_case_length+6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_allcase_from_doctor_and_patient(patient_dict):
    """
    医生根据患者查看此患者在这里的所有病例
    :param patient_dict: 查询信息，包含患者信息和医生ID
    :return: satus：状态，0：表示此患者没有档案信息，１：表示此患者有档案信息，但是没有；
    ３：表示既有档案，又有病例信息
    """
    status_dict = {}
    res_p_all = query_patient(patient_dict)
    print u'############'
    if len(res_p_all) > 0:
        patientid = []
        for res in res_p_all:
            if res[u'patientID'] not in patientid:
                patientid.append(res[u'patientID'])
        doctorid = [patient_dict[u'doctorID']]
        res_all = query_allcase_by_search(doctorid, patientid, patient_dict)
        if len(res_all) > 0:
            status_dict[u'status'] = 2
            status_dict[u'res_all'] = res_all
        else:
            status_dict[u'status'] = 1
            status_dict[u'res_all'] = res_p_all
    else:
        status_dict[u'status'] = 0
        status_dict[u'res_all'] = []
    return status_dict


def query_allcase_from_doctorid_and_patientid(doctorid, patientid, choose_firstID):
    """
    查询某个医生对某个病人的全部病例信息
    :param doctorid:[id1,id2,.....]
    :param patientid:[id1,id2,.....]
    :return:[{病例信息，患者信息},{},{}]
    """
    DCR = query_DCRelation_from_doctor(doctorid)
    caseid = []
    for each in DCR:
        caseid.append(each[u'caseFirstID'])
    if len(caseid) > 0:
        res_all = query_case_from_caseid_and_patientid_secondID(choose_firstID, patientid)
        for res in res_all:
            for dcr in DCR:
                if res.get(u"caseFirstID") == dcr.get(u"caseFirstID") and res.get(u"caseSecondID") == dcr.get(u"caseSecondID"):
                    res[u"doctorRole"] = dcr.get(u"doctorRole")
                    res[u"doctorComment"] = dcr.get(u"doctorComment")
                    break
    else:
        res_all = []
    return res_all


def query_allcase_by_search(doctorid, patientid, patient_dict = {}):
    """
    查询某个医生对某个病人的全部病例信息
    :param doctorid:[id1,id2,.....]
    :param patientid:[id1,id2,.....]
    :return:[{病例信息，患者信息},{},{}]
    """
    DCR = query_DCRelation_from_doctor(doctorid)
    caseid = []
    for each in DCR:
        caseid.append(each[u'caseFirstID'])
    if len(caseid) > 0:
        res_all = query_case_from_caseid_and_patientid_secondID(caseid, patientid, patient_dict)
        for res in res_all:
            for dcr in DCR:
                if res.get(u"caseFirstID") == dcr.get(u"caseFirstID") and res.get(u"caseSecondID") == dcr.get(u"caseSecondID"):
                    res[u"doctorRole"] = dcr.get(u"doctorRole")
                    res[u"doctorComment"] = dcr.get(u"doctorComment")
                    break
    else:
        res_all = []
    return res_all


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
    # print condition
    for key, value in case_dict.items():
        if value != "" and key not in [u"caseFirstID", u"caseID", u"caseSecondID"] and key in case_key:
            str_query.append("{} = '{}'".format(key, value))
    query = " , ".join(str_query)
    # print case_dict
    # print query
    query_sql = "update newCase set {} {};".format(query, condition)
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


def update_DCRelation(dcr_dict):
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
    condition = "WHERE caseFirstID = {} and caseSecondID = {} and doctorID = {}"\
        .format(dcr_dict.get(u"caseFirstID", ""), dcr_dict.get(u"caseSecondID", ""), dcr_dict.get(u"doctorID", ""))
    # print condition
    for key, value in dcr_dict.items():
        if value != u"" and key not in [u"caseFirstID", u"doctorID", u"caseSecondID"] and key in DCRelation_key:
            str_query.append("{} = '{}'".format(key, value))
    query = " , ".join(str_query)
    query_sql = "update newDCRelation set {} {};".format(query, condition)
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


def create_newPatient():
    """
    创建患者表，主键自增长
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS newPatient;")
    cursor.execute("create table newPatient(patientID INT primary key auto_increment, name VARCHAR(20), sex VARCHAR(6),"
                   "age VARCHAR (10), telephone VARCHAR (20), identityCardNum VARCHAR (20), socialSecurityNum VARCHAR (20), p_password VARCHAR (50),"
                   "ziduan1 VARCHAR (1000), ziduan2 VARCHAR (1000),ziduan3 VARCHAR (1000),ziduan4 VARCHAR (1000))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")

    cursor.close()


def insert_newPatient(patient_dict):
    """
    患者表插入操作
    patient_dict:患者信息字典
    :return:
    """
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    sql = "INSERT INTO newPatient(name,sex,age,telephone,\
          identityCardNum,socialSecurityNum, p_password)VALUES ('{}','{}','{}','{}','{}','{}'," \
          "'{}');".format(patient_dict.get("name", ""),
                          patient_dict.get("sex", ""),
                          patient_dict.get("age", ""),
                          patient_dict.get("telephone", ""),
                          patient_dict.get("identityCardNum", ""),
                          patient_dict.get("socialSecurityNum", ""),
                          patient_dict.get("p_password", ""))
    try:
        cursor_insert.execute(sql)
        con_insert.commit()
        cursor_insert.close()
    except Exception, e:
        print e
        con_insert.rollback()
    finally:
        con_insert.close()


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
    query_sql = "update newPatient set {} {};".format(query, condition)
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


def create_newDoctor():
    """
    创建医生表，主键自增长
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS newDoctor;")
    cursor.execute("create table newDoctor(doctorID INT primary key auto_increment, name VARCHAR(20), sex VARCHAR(6),"
                   " age  INT, telephone VARCHAR (20), identityCardNum VARCHAR (20), indication VARCHAR (200), "
                   "department VARCHAR (200), d_password VARCHAR (50),"
                   "ziduan1 VARCHAR (1000), ziduan2 VARCHAR (1000),ziduan3 VARCHAR (1000),ziduan4 VARCHAR (1000))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()



def insert_newDoctor(doctor_dict):
    """
    医生表插入操作
    :return:
    """
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    sql = "INSERT INTO newDoctor(name,sex,age, telephone,\
          identityCardNum, indication, department, d_password)VALUES ('{}','{}',{},'{}','{}','{}','{}'," \
          "'{}');".format(doctor_dict.get("name", ""),
                          doctor_dict.get("sex", ""),
                          doctor_dict.get("age", 0),
                          doctor_dict.get("telephone", ""),
                          doctor_dict.get("identityCardNum", ""),
                          doctor_dict.get("indication", ""),
                          doctor_dict.get("department", ""),
                          doctor_dict.get("d_password", ""))
    # print sql
    # try:
    #     cursor_insert.execute(sql)
    #     con_insert.commit()
    #     cursor_insert.close()
    # except Exception, e:
    #     print e
    #     con_insert.rollback()
    # finally:
    #     con_insert.close()



def query_newDoctor(doctor_dict):
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
        query_sql = "SELECT * FROM newDoctor"
    else:
        query_sql = "SELECT * FROM newDoctor WHERE {}".format(query)
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


'''dianxuan:category,doctorID,remen_dict,tigejiancha_dict,dianxuanID,
'''


def create_dianxuan():
    """
    创建医生表，主键自增长
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS dianxuan;")
    cursor.execute("create table dianxuan(dianxuanID INT primary key auto_increment, doctorID INT ,category INT,"
                   "remen_dict VARCHAR(5000),tigejiancha_dict VARCHAR (5000)) "
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()


def insert_dianxuan(dianxuan_dict):
    """
    医生表插入操作
    :return:
    """
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    sql = "INSERT INTO dianxuan(doctorID,category,remen_dict,tigejiancha_dict"\
         ")VALUES ({},{},'{}','{}');".format(dianxuan_dict.get("doctorID"),
                                             dianxuan_dict.get("category",0),
                                             dianxuan_dict.get("remen_dict",""),
                                             dianxuan_dict.get("tigejiancha_dict",""))
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


def update_dianxuan(dianxuan_dict):
    """
    更细医生信息
    :param dianxuan_dict:｛
            "doctorID":1,
            "cateogory":0 ,
            "remen_dict":"dict",
            "tigejiancha_dict":"dict",
            ｝
    :return:返回查询到的所有患者档案信息，用列别表示，[｛医生信息Ａ｝，｛医生信息Ｂ｝,......]
    """
    query_cx = conn()
    str_query = []
    condition = "WHERE doctorID = {} AND category = {}".format(dianxuan_dict.get(u"doctorID", 0),dianxuan_dict.get(u"category",0))
    for key, value in dianxuan_dict.items():
        if value != "" and key not in [u"category", u'doctorID'] and key in dianxuan_key:
            str_query.append("{} = '{}'".format(key, value))
    query = " , ".join(str_query)
    query_sql = "update dianxuan set {} {};".format(query, condition)
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


def query_dianxuan(dianxuan_dict):
    """
    给定医生的信息字典，查询医生ＩＤ
    :param doctor_dict:｛
            "category" : 0,
            "doctorID" : 1,
            ｝
    :return:返回查询到的所有患者档案信息，用列别表示，[｛医生信息Ａ｝，｛医生信息Ｂ｝,......]
    """
    key_list = dianxuan_dict.keys()
    doctor_dict = {key: dianxuan_dict[key] for key in key_list if key in dianxuan_key}
    query_cx = conn()
    str_query = []
    for key, value in doctor_dict.items():
        if value != "":
            str_query.append("{} = {}".format(key, value))
    query = " and ".join(str_query)
    if len(query) == 0:
        query_sql = "SELECT * FROM dianxuan"
    else:
        query_sql = "SELECT * FROM dianxuan WHERE {}".format(query)
    print query_sql
    results_all = []
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'dianxuanID'] = res[0]
            temp_dict[u'doctorID'] = res[1]
            temp_dict[u'category'] = res[2]
            temp_dict[u'remen_dict'] = res[3]
            temp_dict[u'tigejiancha_dict'] = res[4]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all
def update_newDoctor(doctor_dict):
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
    query_sql = "update newDoctor set {} {};".format(query, condition)
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



def create_newCase():
    """
    创建病例表，存储病例信息；主键，自增类型，用于标识病例的唯一性
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS newCase;")
    cursor.execute("create table newCase(caseID INT auto_increment primary key, caseFirstID INT, caseSecondID INT , chiefComplaint VARCHAR(200),"
                   " HPI  VARCHAR (500), physicalExamination VARCHAR (500), chemicalExamination VARCHAR (500),"
                   " differentialDiagnosis VARCHAR (500), treatment VARCHAR (3000), predictionResults VARCHAR (500),"
                   "auxInfo VARCHAR (2000), patientID INT, caseDate VARCHAR (20), "
                   "isFinish int,check_recommend VARCHAR (1000), ziduan2 VARCHAR (1000),ziduan3 VARCHAR (1000),ziduan4 VARCHAR (1000),"
                   "recommend_medicine VARCHAR(2000),category INT DEFAULT 0 )"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()


def insert_newCase(case_dict):
    """
    病例表插入操作
    :return:
    """

    second_id = query_maxSecondID(case_dict)
    case_dict[u"caseSecondID"] = second_id
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    sql = "INSERT INTO newCase(caseFirstID, caseSecondID,chiefComplaint,HPI, physicalExamination,\
chemicalExamination, differentialDiagnosis, treatment, predictionResults, auxInfo, patientID, caseDate, isFinish, check_recommend,zd_model,zd_res,zd_reason,recommend_medicine,category,disease_prob) " \
          "VALUES({},{}, '{}','{}','{}','{}','{}','{}','{}','{}',{}," \
          "'{}', {},'{}','{}','{}','{}','{}',{},'{}');".format(case_dict.get(u'caseFirstID', 1),
                            case_dict.get(u'caseSecondID', 0),
                            case_dict.get(u'chiefComplaint', u""),
                            case_dict.get(u'HPI', u""),
                            case_dict.get(u'physicalExamination', u""),
                            case_dict.get(u'chemicalExamination', u""),
                            case_dict.get(u'differentialDiagnosis', u""),
                            case_dict.get(u'treatment', u""),
                            case_dict.get(u'predictionResults', u""),
                            case_dict.get(u'auxInfo', u""),
                            case_dict.get(u'patientID', 1),
                            case_dict.get(u'caseDate', u""),
                            case_dict.get(u'isFinish', 0),
                            case_dict.get(u'check_recommend', u""),
                            case_dict.get(u'zd_model',u''),
                            case_dict.get(u'zd_res',u''),
                            case_dict.get(u'zd_reason',u''),
                            case_dict.get(u'recommend_medicine',u''),
                            case_dict.get(u'category',0),
                            case_dict.get(u'disease_prob', u"")
                              )
    try:
        cursor_insert.execute(sql)
        con_insert.commit()
        cursor_insert.close()
    except Exception, e:
        print e
        con_insert.rollback()
    finally:
        con_insert.close()


def create_newDCRelation():
    """
    newDCRelation表，用于储存医生和病例之间的关系信息
    relationID:主键，自增类型，用于标识关系的唯一性
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS newDCRelation;")
    cursor.execute("create table newDCRelation(relationID INT primary key auto_increment, caseFirstID INT, caseSecondID INT,"
                   "doctorID INT, doctorRole VARCHAR (20), doctorComment VARCHAR (500), comment_time VARCHAR(100),"
                   "ziduan1 VARCHAR(1000), ziduan2 VARCHAR (1000),ziduan3 VARCHAR (1000),ziduan4 VARCHAR (1000))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()


def insert_newDCRelation(DCRelation_dict):
    """
    关系表插入操作
    :return:
    """
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    now = datetime.datetime.now()
    comment_time = now.strftime('%Y-%m-%d %H:%M:%S')
    comment_time_from_dict = DCRelation_dict.get(u"comment_time", u"")
    if comment_time_from_dict != u"":
        comment_time = comment_time_from_dict
    sql = "INSERT INTO newDCRelation(caseFirstID,caseSecondID,doctorID, doctorRole,\
          doctorComment, comment_time)VALUES ({},{},{},'{}','{}'," \
          "'{}');".format(DCRelation_dict.get(u"caseFirstID", 0),
                          DCRelation_dict.get(u"caseSecondID", 0),
                          DCRelation_dict.get(u"doctorID", 0),
                          DCRelation_dict.get(u"doctorRole", u""),
                          DCRelation_dict.get(u"doctorComment", u""),
                          comment_time)
    try:
        cursor_insert.execute(sql)
        con_insert.commit()
        cursor_insert.close()
    except Exception, e:
        print e
        con_insert.rollback()
    finally:
        con_insert.close()


def query_newDCRelation(DCRelation_dict):
    """
    给定关系信息字典，查询关系信息
    :param doctor_dict:｛
               "caseId" : 1,
                "doctorID" : 1,
                "caseSecondID" : 0,
                "doctorRole" : "主治医生",
                "doctorComment" : ""
            ｝
    :return:返回查询到的所有患者档案信息，用列别表示，[｛医生信息Ａ｝，｛医生信息Ｂ｝,......]
    """
    key_list = DCRelation_dict.keys()
    DCRelation_dict = {key: DCRelation_dict[key] for key in key_list if key in DCRelation_key}
    query_cx = conn()
    str_query = []
    for key, value in DCRelation_dict.items():
        if value != "":
            str_query.append("{} = '{}'".format(key, value))
    query = " and ".join(str_query)
    query_sql = "SELECT * FROM newDCRelation WHERE {}".format(query)
    results_all = []
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'relationID'] = res[0]
            temp_dict[u'caseID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'doctorID'] = res[3]
            temp_dict[u'doctorRole'] = res[4]
            temp_dict[u'doctorComment'] = res[5]
            temp_dict[u'comment_time'] = res[6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def query_newDCRelation_for_doctor_case(DCRelation_dict):
    """
    给定关系信息字典，查询关系信息
    :param doctor_dict:｛
               "caseId" : 1,
                "doctorID" : 1,
                "caseSecondID" : 0,
                "doctorRole" : "主治医生",
                "doctorComment" : ""
            ｝
    :return:返回查询到的所有患者档案信息，用列别表示，[｛医生信息Ａ｝，｛医生信息Ｂ｝,......]
    """
    key_list = DCRelation_dict.keys()
    DCRelation_dict = {key: DCRelation_dict[key] for key in key_list if key in DCRelation_key}
    query_cx = conn()
    str_query = []
    for key, value in DCRelation_dict.items():
        if value != "":
            str_query.append("{} = '{}'".format(key, value))
    query = " and ".join(str_query)
    query_sql = "SELECT * FROM newDCRelation, newDoctor WHERE {} and newDCRelation.doctorID = newDoctor.doctorID ORDER BY comment_time;".format(query)
    results_all = []
    # print query_sql
    zhuzhi = u''
    doctorComment = u''
    res_all = []
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'doctorRole'] = res[4]
            temp_dict[u'doctorComment'] = res[5]
            temp_dict[u'commentTime'] = res[6]
            temp_dict[u'doctorID'] = res[11]
            temp_dict[u'doctorName'] = res[12]
            if res[4] == u'主治医生':
                zhuzhi = res[12]
            if res[5] != u'':
                doctorComment += res[12] + u'({})'.format(res[6]) + u' 评论：' + res[5] + u'\n'
                res_all.append(temp_dict)

        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return zhuzhi, doctorComment, res_all


def query_maxFirstID():
    query_cx = conn()
    query_sql = "select MAX(caseFirstID) from newCase;"
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


def query_maxSecondID(case_dict):
    query_cx = conn()
    query_sql = "select MAX(caseSecondID) from newCase where caseFirstID = {};".format(case_dict.get(u'caseFirstID', 1))
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


def create_medicine():
    """
    创建患者表，主键自增长
    ID:系统内唯一编码，自增长；
    medicineID:药物国家唯一编码；
    ziduan1:其他备用字段
    ziduan2:其他备用字段
    ......:
    ziduan10:其他备用字段
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS medicine;")
    cursor.execute("create table medicine(medicineSystemID INT primary key auto_increment, medicineID VARCHAR (50), ziduan1 VARCHAR (1000),"
                   "ziduan2 VARCHAR (1000), ziduan3 VARCHAR (1000), ziduan4 VARCHAR (1000), ziduan5 VARCHAR (1000),"
                   "ziduan6 VARCHAR (1000), ziduan7 VARCHAR (1000), ziduan8 VARCHAR (1000), ziduan9 VARCHAR (1000),"
                   "ziduan10 VARCHAR (1000), UNIQUE KEY (medicineID))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")

    cursor.close()


def query_medicine(medicine_dict):
    """
    给定药物信息，查询对应的药物信息
    :param medicine_dict:｛
            "name":"药物名称",
            "medicineID":"药物ＩＤ",
            "ziduan1":"其他字段",
            ｝
    :return:返回查询到的所有患者档案信息，用列别表示，[｛药物信息Ａ｝，｛药物信息Ｂ｝,......]
    """
    key_list = medicine_dict.keys()
    medicine_dict = {key: medicine_dict[key] for key in key_list if key in medicine_key}
    query_cx = conn()
    str_query = []
    for key, value in medicine_dict.items():
        if value != "":
            str_query.append("{} = '{}'".format(key, value))
    query = " and ".join(str_query)
    query_sql = "SELECT * FROM medicine WHERE {};".format(query)
    results_all = []
    # print query_sql
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        # print results
        for res in results:
            temp_dict = dict()
            temp_dict[u'medicineSystemID'] = res[0]
            temp_dict[u'medicineID'] = res[1]
            temp_dict[u'ziduan1'] = res[2]
            temp_dict[u'ziduan2'] = res[3]
            temp_dict[u'ziduan3'] = res[4]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def insert_medicine(medicine_dict):
    """
    药物表插入操作，首先会判断药物是否已经存在系统中
    :param medicine_dict:｛
            "name":"药物名称",
            "medicineID":"药物ＩＤ",
            "ziduan1":"其他字段",
            ｝
    :return:
    status：
        0: 药物不存在，插入成功；
        1: 药物不存在，插入失败；
        2: 药物存在，插入失败，返回已存在药物的信息；
    """
    results = {}
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    medicine_insert_ID = {}
    medicine_insert_ID[u'medicineID'] = medicine_dict.get(u"medicineID", u"")
    res_all = query_medicine(medicine_insert_ID)
    if len(res_all) > 0:
        results[u'status'] = 2
        results[u'res_all'] = res_all
        return results
    sql = "INSERT INTO medicine(medicineID)VALUES ('{}');".format(medicine_dict.get(u"medicineID", u""))
    status = 1
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
        results[u'status'] = status
        results[u'res_all'] = []
        return results


def create_treatment():
    """
    创建患者表，主键自增长
    ID:系统内唯一编码，自增长；
    ziduan1:其他备用字段
    ziduan2:其他备用字段
    ......:
    ziduan10:其他备用字段
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS treatment;")
    cursor.execute("create table treatment(treatmentSystemID INT primary key auto_increment,treatmentID VARCHAR (50), ziduan1 VARCHAR (1000),"
                   "ziduan2 VARCHAR (1000), ziduan3 VARCHAR (1000), ziduan4 VARCHAR (1000), ziduan5 VARCHAR (1000),"
                   "ziduan6 VARCHAR (1000), ziduan7 VARCHAR (1000), ziduan8 VARCHAR (1000), ziduan9 VARCHAR (1000),"
                   "ziduan10 VARCHAR (1000))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()


def query_treatment(treatment_dict):
    """
    给定药物信息，查询对应的药物信息
    :param treatment_dict:｛
            "ziduan1":"字段１",
            "ziduan2":"字段２",
            "ziduan3":"字段３",
            ｝
    :return:返回查询到的所有患者档案信息，用列别表示，[｛药物信息Ａ｝，｛药物信息Ｂ｝,......]
    """
    key_list = treatment_dict.keys()
    treatment_dict = {key: treatment_dict[key] for key in key_list if key in treatment_key}
    query_cx = conn()
    str_query = []
    for key, value in treatment_dict.items():
        if value != "":
            str_query.append("{} = '{}'".format(key, value))
    query = " and ".join(str_query)
    query_sql = "SELECT * FROM treatment WHERE {};".format(query)
    results_all = []
    # print query_sql
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        # print results
        for res in results:
            temp_dict = dict()
            temp_dict[u'treatmentSystemID'] = res[0]
            temp_dict[u'treatmentID'] = res[1]
            temp_dict[u'ziduan1'] = res[2]
            temp_dict[u'ziduan2'] = res[3]
            temp_dict[u'ziduan3'] = res[4]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def insert_treatment(treatment_dict):
    """
    药物表插入操作，首先会判断药物是否已经存在系统中
    :param treatment_dict:｛
            "treatmentID":"治疗ＩＤ",
            "ziduan1":"其他字段",
            ｝
    :return:
    status：
        0: 药物不存在，插入成功；
        1: 药物不存在，插入失败；
        2: 药物存在，插入失败，返回已存在的信息；
    """
    results = {}
    con_insert = conn()
    cursor_insert = con_insert.cursor()
    treatment_insert_ID = {}
    treatment_insert_ID[u'treatmentID'] = treatment_dict.get(u"treatmentID", u"")
    res_all = query_treatment(treatment_insert_ID)
    if len(res_all) > 0:
        results[u'status'] = 2
        results[u'res_all'] = res_all
        return results
    # print res_all
    sql = "INSERT INTO treatment(treatmentID, ziduan1, ziduan2)VALUES ('{}', '{}'," \
          "'{}');".format(treatment_dict.get(u"treatmentID", u""),
                          treatment_dict.get(u"ziduan1", u"1"),
                          treatment_dict.get(u"ziduan2", u"1"))
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
        results[u'status'] = status
        results[u'res_all'] = []
        return results


def create_appendix():
    """
    创建附件表，主键自增长
    appendixID:系统内唯一编码，自增长；
    caseFirstID:附件属于的病例的FirstID
    caseSecondID:附件属于的病例的SecondID
    name:　附件名称
    path:　附件地址
    type: 附件类型，PDF, WORD等
    abstract: 附件摘要
    ziduan1:　其他字段
    ziduan2: 其他字段
    ziduan3: 其他字段
    ziduan4: 其他字段
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS appendix;")
    cursor.execute("create table appendix(appendixID INT primary key auto_increment, caseFirstID INT, caseSecondID INT,"
                   "name VARCHAR (1000), type VARCHAR (1000), path VARCHAR (1000), abstract VARCHAR (1000),upload_time VARCHAR(1000), "
                   "doctorID int, ziduan2 VARCHAR (1000), ziduan3 VARCHAR (1000), ziduan4 VARCHAR (1000))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()


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


def create_CARelation():
    """
    创建病例化验关系表，主键自增长
    CARelationID:　系统内唯一编码，自增长；
    caseFirstID: 化验属于的病例的FirstID
    caseSecondID:　化验属于的病例的SecondID
    assayID: 化验ID
    name:　化验名称
    type: 化验类型
    info: 化验信息
    ziduan1:
    ziduan2:
    zidua3:
    ziduan4:
    :return:
    """
    con = conn()
    cursor = con.cursor()
    cursor.execute("Drop table if EXISTS CARelation;")
    cursor.execute("create table CARelation(CARelationID INT primary key auto_increment, caseFirstID INT, caseSecondID INT,"
                   "assayID INT , name VARCHAR (1000), type VARCHAR (1000), info VARCHAR (3000), ziduan1 VARCHAR (1000),"
                   "ziduan2 VARCHAR (1000), ziduan3 VARCHAR (1000), ziduan4 VARCHAR (1000))"
                   "ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
    cursor.close()


def insert_CARelation(CARelation_dict):
    """
    病例化验关系表插入操作
    :param CARelation_dict:｛
                caseFirstID: 化验属于的病例的FirstID
                caseSecondID:　化验属于的病例的SecondID
                assayID: 化验ID
                name:　化验名称
                type: 化验类型
                info: 化验信息
            ｝
    :return:
    status：
        0: 附件插入成功；
        １：附件插入失败；
    """

    con_insert = conn()
    cursor_insert = con_insert.cursor()
    sql = "INSERT INTO CARelation(caseFirstID, caseSecondID, assayID, name, type, info)VALUES ({},{},{}, '{}','{}'," \
          "'{}');".format(CARelation_dict.get(u"caseFirstID", 1),
                          CARelation_dict.get(u"caseSecondID", 0),
                          CARelation_dict.get(u"assayID", 0),
                          CARelation_dict.get(u"name", u""),
                          CARelation_dict.get(u"type", u""),
                          CARelation_dict.get(u"info", u"")
                          )
    status = 1
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


def query_CARelation(CARelation_dict):
    """
    给定病例关系信息，查询对应的病例化验关系信息
    :param appendix_dict:｛
                CARalation: 唯一表示此关系的ＩＤ
                caseFirstID: 化验属于的病例的FirstID
                caseSecondID:　化验属于的病例的SecondID
                assayID: 化验ID
                name:　化验名称
                type: 化验类型
                info: 化验信息
            ｝
    :return:返回查询到的所有病例化验信息，用列别表示，[｛病例化验信息Ａ｝，｛病例化验信息Ｂ｝,......]
    """
    query_cx = conn()
    str_query = []
    for key, value in CARelation_dict.items():
        if value != "" and key in CARelation_key:
            str_query.append("{} = '{}'".format(key, value))
    query = " and ".join(str_query)
    query_sql = "SELECT * FROM CARelation WHERE {};".format(query)
    results_all = []
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'CARelationID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'assayID'] = res[3]
            temp_dict[u'name'] = res[4]
            temp_dict[u'type'] = res[5]
            temp_dict[u'info'] = res[6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def update_CARelation(CARelation_dict):
    """
    给定病例化验关系信息，更新对应的信息
    :param appendix_dict:｛
                CARelationID: 唯一标识这一关系的ID
                caseFirstID: 化验属于的病例的FirstID
                caseSecondID:　化验属于的病例的SecondID
                assayID: 化验ID
                name:　化验名称
                type: 化验类型
                info: 化验信息
            ｝
    :return:
    """
    query_cx = conn()
    str_query = []
    condition = "WHERE CARelationID = {}".format(CARelation_dict.get(u"CARelationID", ""))
    for key, value in CARelation_dict.items():
        if value != "" and key not in [u"caseFirstID", u"caseSecondID", u'CARelationID'] and key in CARelation_key:
            str_query.append("{} = '{}'".format(key, value))
    query = " , ".join(str_query)
    query_sql = "update CARelation set {} {};".format(query, condition)
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




def search_diseae_moban(patient_info):
    """
    根据疾病名称搜索疾病模版
    :param disease_name: 
    :return: 
    """
    status_dict = dict()
    cx_conn = conn()
    query_str = u'select * from newpatient where name like "%{}%"'.format(patient_info[u"name"])
    # print query_str
    mobans = []
    try:
        cx_cur = cx_conn.cursor()
        cx_cur.execute(query_str)
        cx_res = cx_cur.fetchall()
        for res in cx_res:
            temp_dict = dict()
            temp_dict[u'patientID'] = int(res[0])
            temp_dict[u'name'] = res[1]
            temp_dict[u'sex'] = res[2]
            temp_dict[u'age'] = res[3]
            temp_dict[u'telephone'] = res[4]
            temp_dict[u'identityCardNum'] = res[5]
            temp_dict[u'socialSecurityNum'] = res[6]
            mobans.append(temp_dict)
        cx_cur.close()
    except Exception, e:
        print e
    finally:
        cx_conn.close()

    if len(mobans) > 0:
        patientid = []
        for res in mobans:
            if res[u'patientID'] not in patientid:
                patientid.append(res[u'patientID'])
        doctorid = [patient_info[u'doctorID']]
        res_all = query_allmoban_by_search(doctorid, patientid, patient_info)
        if len(res_all) > 0:
            status_dict[u'status'] = 2
            status_dict[u'res_all'] = res_all
        else:
            status_dict[u'status'] = 1
            status_dict[u'res_all'] = mobans
    else:
        status_dict[u'status'] = 0
        status_dict[u'res_all'] = []
    return status_dict

def query_allmoban_by_search(doctorid, patientid, patient_info):
    # print doctorid
    DCR = query_DCRelation_from_doctor(doctorid)
    caseid = []
    for each in DCR:
        caseid.append(each[u'caseFirstID'])
    if len(caseid) > 0:
        res_all = query_moban_from_caseid_and_patientid_secondID(caseid, patientid, patient_info)
        for res in res_all:
            for dcr in DCR:
                if res.get(u"caseFirstID") == dcr.get(u"caseFirstID") and res.get(u"caseSecondID") == dcr.get(u"caseSecondID"):
                    res[u"doctorRole"] = dcr.get(u"doctorRole")
                    res[u"doctorComment"] = dcr.get(u"doctorComment")
                    break
    else:
        res_all = []
    return res_all


def query_moban_from_caseid_and_patientid_secondID(caseid, patientid, patient_dict):
    query_cx = conn()
    str_query = []
    for eachid in caseid:
        if eachid != "":
            str_query.append("'{}'".format(eachid))
    query = " , ".join(str_query)
    str_patient_query = []
    for eachid in patientid:
        if eachid != "":
            str_patient_query.append("'{}'".format(eachid))
    patient_query = " , ".join(str_patient_query)

    query_sql = "select * from newCase, newPatient where caseFirstID in ({}) and newPatient.patientID in ({}) and newCase.patientID in ({}) and newCase.patientID = newPatient.patientID ORDER BY caseDate;".format(
            query, patient_query, patient_query)
    results_all = []

    # print query_sql

    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        for res in results:
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]
            temp_dict[u'patientID'] = res[new_case_length + 0]
            temp_dict[u'name'] = res[new_case_length + 1]
            temp_dict[u'sex'] = res[new_case_length + 2]
            temp_dict[u'age'] = res[new_case_length + 3]
            temp_dict[u'telephone'] = res[new_case_length + 4]
            temp_dict[u'identityCardNum'] = res[new_case_length + 5]
            temp_dict[u'socialSecurityNum'] = res[new_case_length + 6]
            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all


def add_column():
    sql = "alter table  newPatient add column ziduan1 VARCHAR(1000);"
    sql = "alter table  newPatient add column ziduan2 VARCHAR(1000);"
    sql = "alter table  newPatient add column ziduan3 VARCHAR(1000);"
    sql = "alter table  newPatient add column ziduan4 VARCHAR(1000);"
    sql = "alter table  newDoctor add column ziduan1 VARCHAR(1000);"
    sql = "alter table  newDoctor add column ziduan2 VARCHAR(1000);"
    sql = "alter table  newDoctor add column ziduan3 VARCHAR(1000);"
    sql = "alter table  newDoctor add column ziduan4 VARCHAR(1000);"
    sql = "alter table  newCase CHANGE check_recommd  check_recommend VARCHAR(1000);"
    sql = "alter table  newCase add column ziduan2 VARCHAR(1000);"
    sql = "alter table  newCase add column ziduan3 VARCHAR(1000);"
    sql = "alter table  newCase add column ziduan4 VARCHAR(1000);"
    sql = "alter table  newDCRelation add column ziduan1 VARCHAR(1000);"
    sql = "alter table  newDCRelation add column ziduan2 VARCHAR(1000);"
    sql = "alter table  newDCRelation add column ziduan3 VARCHAR(1000);"
    sql = "alter table  newDCRelation add column ziduan4 VARCHAR(1000);"


def query_case_during_peroid_from_patientid(case_dict):
    """
　　　通过patientid查询case记录
    :param {start_time,end_time,patientID}
    :return:[{病例信息，患者信息},{},{}]
    """
    query_cx = conn()
    query_sql = "select * from newCase where patientID = {} and  caseDate BETWEEN '{}' AND '{}' "\
        .format(case_dict.get('patientID'),case_dict.get("start_time"),case_dict.get("end_time"))
    results_all = []
    try:
        cursor_query = query_cx.cursor()
        cursor_query.execute(query_sql)
        results = cursor_query.fetchall()
        # print len(results)
        for res in results:
            # print res
            temp_dict = dict()
            temp_dict[u'caseID'] = res[0]
            temp_dict[u'caseFirstID'] = res[1]
            temp_dict[u'caseSecondID'] = res[2]
            temp_dict[u'chiefComplaint'] = res[3]
            temp_dict[u'HPI'] = res[4]
            temp_dict[u'physicalExamination'] = res[5]
            temp_dict[u'chemicalExamination'] = res[6]
            temp_dict[u'differentialDiagnosis'] = res[7]
            temp_dict[u'treatment'] = res[8]
            temp_dict[u'predictionResults'] = res[9]
            temp_dict[u'auxInfo'] = res[10]
            temp_dict[u'patientID'] = res[11]
            temp_dict[u'caseDate'] = res[12]
            temp_dict[u'isFinish'] = res[13]
            temp_dict[u'check_recommend'] = res[14]
            temp_dict[u'zd_model'] = res[15]
            temp_dict[u'zd_res'] = res[16]
            temp_dict[u'zd_reason'] = res[17]
            temp_dict[u'recommend_medicine'] = res[18]
            temp_dict[u'category'] = res[19]
            temp_dict[u'disease_prob'] = res[20]

            results_all.append(temp_dict)
        cursor_query.close()
    except Exception, e:
        print e
    finally:
        query_cx.close()
        return results_all

if __name__ == '__main__':
    case_dict = {'patientID':82,'start_time':'2017-11-20 15:47:28','end_time':'2017-11-22 20:47:28'}
    cases = query_allcase_of_category(3, category=0)
    print len(cases)
    print cases
    # result = query_case_during_peroid_from_patientid(case_dict)
    # print result
    # create_dianxuan()
    # dianxuan_dict = {"doctorID":1,"category":0,"remen_dict":'remen_dict',"tigejiancha_dict":"tigejiancha_dict2"}
    # insert_dianxuan(dianxuan_dict)
    # update_dianxuan(dianxuan_dict)


    # doctor_dict = {
    #     "name": "潘医生",
    #     "telephone": "13412341234",
    #     "sex": "女",
    #     "age": 23,
    #     "d_password": "12345678",
    #     "department": "内科",
    #     "indication": "呼吸道专业"
    # }
    # insert_newDoctor(doctor_dict)
    # patient_dict = {
    #     "name":"王小山",
    #     "telephone":"15612341234",
    #     "sex":"男",
    # }
    # DCRelation_dict={
    # "caseFirstID" : 72,
    # "doctorID" : 2,
    # "caseSecondID" : 0,
    # "doctorRole" : "主治医生",
    # "doctorComment" : "",
    # "doctorComment2343": ""
    # }
    # case_dict = {
    #     "caseFirstID": 2,
    #     "caseSecondID": 0,
    #     "chiefComplaint": "主诉",
    #     "HPI": "现病史",
    #     "physicalExamination" : "体格检查",
    #     "chemicalExamination": "化验检测",
    #     "differentialDiagnosis": "医生开具的鉴别诊断",
    #     "treatment": "医生开的治疗手段",
    #     "predictionResults": "系统预测结果",
    #     "auxInfo": "辅助信息",
    #     "patientID": 1,
    #     "caseDate": "病例时间",
    #
    # }
    # DCRelation_dict = {}
    # create_newPatient()
    # insert_newPatient(patient_dict)
    # create_newDoctor()
    # insert_newDoctor(doctor_dict)
    # create_newCase()
    # insert_newCase(case_dict)
    # create_newDCRelation()
    # insert_newDCRelation(DCRelation_dict)
    # print "adasd"
    # results_all = query_patient(patient_dict)
    # print results_all[0]
    # patientid = [1]
    # results_all = query_case_from_patientid(patientid)
    # for each in results_all:
    #     print each
    # doctorid = [1]
    # results_all = query_DCRelation_from_doctor(doctorid)
    # for each in results_all:
    #     print each
    # caseid = [1]
    # results_all = query_case_from_caseid(caseid)
    # for each in results_all:
    #     print each

    # doctorid = 1
    # query_allcase_from_doctorid(doctorid)
    #
    #
    # query_patient_dict = {
    #     "name":"王小山",
    #     "telephone":"15612341234",
    #     "sex":"男",
    #     "doctorId": 1,
    # }
    # status_dict = query_allcase_from_doctor_and_patient(query_patient_dict)
    # for key,value in status_dict.items():
    #     print key, value
    # query_case_dict = {
    #     "caseFirstID": 1,
    #     "caseSecondID": 0,
    #     "predictionResults": "更新",
    #     "auxInfo": "更新",
    #     "caseDate": "更新"
    #
    # }
    # res_all = query_case(query_case_dict)
    # for res in res_all:
    #     print res
    # update_case(query_case_dict)
    # res_all = query_newDoctor(doctor_dict)
    # for res in res_all:
    #     print res
    # res_all = query_newDCRelation(DCRelation_dict)
    # for res in res_all:
    #     print res
    # print query_maxFirstID()
    # second_dict = {
    #     u"caseFirstID": 1
    # }
    # print query_maxSecondID(second_dict)
    # create_medicine()
    # create_treatment()
    # create_appendix()
    # create_CARelation()
    pass