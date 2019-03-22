# -*- coding:utf-8 -*-#

from __future__ import division
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import OPDB
import json,pickle,random,Levenshtein,re
import tornado.web
import db_sql as db
from openpyxl import load_workbook
import os
import lph_db_ado as myDb
import cx_sql_db as cxDB
from data import analysis_yiyi as huayan_canshu_shuoming

class JudgeTimesAndIsExisted(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        user_id = self.get_argument('uid')
        user_times=self.get_argument('times')
        temp_dict = OPDB.query_patientsinquiry_table(user_id,user_times)
        if temp_dict['status'] == "success":
            self.write(temp_dict)
# class CurrentTimes(tornado.web.RequestHandler):
#     def get(self):
#         pass
#     def post(self):
#         user_id = self.get_argument('uid')
#         user_times=self.get_argument('times')
#         temp_dict = OPDB.query_patientsinquiry_table(user_id,user_times)
#         if temp_dict['status'] == "success":
#             self.write(temp_dict)
class PatientStandardHandler(tornado.web.RequestHandler):
    def get(self):
        uname = self.get_argument('uname')
        self.render("patient_record.html", all_cases={}, current={"name":uname},category=0,source="")
    def post(self):
        pass
class StoreInquiryRecordHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        ad=self.request.arguments
        print(ad)
        OPDB.insert_patient_inquirystatus_table(ad)
class StoreHealthRecordHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        ad=self.request.arguments
        y=ad['year'][0]
        m=ad['month'][0]
        d=ad['day'][0]
        if(len(y)>0 and len(m)>0 and len(d)>0):
            birth = y+"-"+m+"-"+d
        ad['birth'] =birth
        OPDB.insert_patient_healthstatus_table(ad)

class  JudgeIsExistHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        user_id=self.get_argument('uid')
        temp_dict = OPDB.query_isexist(user_id)
        if temp_dict['status']=="success":
            self.write(temp_dict)

class CheckInquiryDetailHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        u_id=self.get_argument('u_id')
        data={"u_id":u_id}
        self.write(json.dumps(data))
class HealthCheckHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('u_id')
        current = {"name": self.get_argument('current')}
        all_data = {"name": "张笑文",
                    "sex": "男",
                    "birthday": "1994/01/01",
                     "time": "20190101 ",
                    "index":"1"
                    }
        self.render("doctor_record.html", u_id=id, all_data=all_data, current=current, source='0')
    def post(self):
        pass
class HealthRecordHandler(tornado.web.RequestHandler):
    def get(self):
        uname = self.get_argument('uname')
        uid = self.get_secure_cookie("user_id")
        times=OPDB.query_current_times(uid)
        print(times)
        self.render("patient_record.html", all_cases={}, current={"name":uname,"uid" : uid},category=0,source="",times=times)
    def post(self):
        pass
class CheckDetailHandler(tornado.web.RequestHandler):

    def get(self):

        pass
    def post(self):
        u_id=self.get_argument('u_id')
        alldata= {"name": "张笑文",
                        "sex": "男",
                        "birthday": "1994/01/01",
                        "time": "20190101 ",
                 }
        data={"u_id":u_id,"alldata":alldata}
        self.write(json.dumps(data))
class ReloadImgHandler(tornado.web.RequestHandler):
    """
    验证码刷新控制器
    """
    with open("./database/lph_data/lph_sypmstoms/all_validate_images.pkl", "r") as f:
        all_validata_images = pickle.load(f)

    def get(self):
        self.render("user_login.html")

    def post(self):
        image_info = random.choice(self.all_validata_images)
        print image_info
        user_type = self.get_argument("user_type")
        # print user_type
        user_phone = self.get_argument("user_phone")
        # print user_phone
        user_password = self.get_argument("user_password")
        reload_info = {}
        reload_info["user_phone"] = user_phone
        reload_info["user_password"] = user_password
        reload_info["user_type"] = user_type
        reload_info["image_info"] = image_info
        self.write(json.dumps(reload_info))
class LoginHandler(tornado.web.RequestHandler):
    """
    登录逻辑控制器
    """
    with open("./database/lph_data/lph_sypmstoms/all_validate_images.pkl", "r") as f:
        all_validata_images = pickle.load(f)

    def get(self):
        if self.get_argument("source","") == "wx":
            source =self.get_argument("source")
        else:
            source =""
        image_info = random.choice(self.all_validata_images)
        self.render("user_login.html", img_info=image_info,source=source)

    def post(self):
        user_type = self.get_argument("user_type")
        # print user_type
        user_phone = self.get_argument("user_phone")

        # print user_phone
        user_password = self.get_argument("user_password")
        temp_dict= OPDB.query_patient_user(user_phone, user_password)
        # print user_id, user_name, is_existed
        if temp_dict['status']=='success':
            user_id=temp_dict['id']
            self.set_secure_cookie("user_id", str(user_id))
            self.set_secure_cookie("user_name", temp_dict['name'])
            self.set_secure_cookie("user_type", str(user_type))
        self.write(temp_dict)
        # user_id, user_name, is_existed = myDb.search_user(user_phone, user_password, int(user_type))
        # # print user_id, user_name, is_existed
        # res_json = {}
        # if is_existed == 1:
        #     res_json["status"] = "success"
        #     res_json["user_type"] = int(user_type)
        # else:
        #     res_json["status"] = "fail"
        # self.set_secure_cookie("user_id", str(user_id))
        # self.set_secure_cookie("user_name", str(user_name))
        # self.set_secure_cookie("user_type", str(user_type))
        # self.write(json.dumps(res_json))

class DoctorHomeHandler(tornado.web.RequestHandler):
    """
    医生和家长主页控制器
    """
    def get(self):
        if self.get_argument("source","") == "wx":
            source =self.get_argument("source")
        else:
            source =""
        category = self.get_argument("category")
        user_id = self.get_argument("uid")
        user_name=self.get_argument('uname')
        user_type = self.get_secure_cookie("user_type")
        user_id = self.get_secure_cookie("user_id")
        res={"uid":user_id,"name":user_name}
        # doctor_dict = {
        #     u'doctorID': 3,
        # }
        # res_doctor = cxDB.query_newDoctor(doctor_dict)[0]
        if category == "0":
            # allcases={'name':'张笑文','sex':'男','birthday':'1994/01/01','fathername':'xld','mothername':'mama','phone':'13312341234','time':'20190101','id':'1'}
            self.render("patient_home.html", all_cases={}, current=res,category=category,source=source)
        elif category == "1":

            allcases ={"1":{"name": "张笑文",
                        "sex": "男",
                        "age":"3",
                        "birthday": "1994/01/01",
                        "fathername": "xld",
                        "mothername": "mama",
                        "phone": "13312341234",
                        "time": "20190101 ",
                        "id": "1"
                 }}

            self.render("doctor_home.html", all_cases=allcases, current=res_doctor,category=category,source=source)
        else:
            self.redirect("/child/login")

    def post(self):
        """
        处理主页上的搜索请求
        :return:
        """
        patient_info = {
            u"name": self.get_argument("p_name"),
            u"telephone": self.get_argument("p_phone"),
            u"identityCardNum": self.get_argument("p_id_card"),
            u"socialSecurityNum": self.get_argument("p_socailID"),
            u"doctorID": self.get_secure_cookie("user_id"),
            u"startdate": self.get_argument("start_time"),
            u"enddate": self.get_argument("end_time")
        }

        # 根据patient_info查询
        search_results = cxDB.query_allcase_from_doctor_and_patient(patient_info)
        # search_results = sorted(search_results, key=lambda item: item[u"caseDate"], reverse=True)
        # 查询结果




class DoctorCaseHandler(tornado.web.RequestHandler):
    """
    医生对应的病例页控制器
    """
    xitong = pickle.load(open("./database/lph_data/lph_sypmstoms/xitong_new.pkl", "r"))
    remen = pickle.load(open("./database/lph_data/lph_sypmstoms/remen_new.pkl", "r"))
    tigejiancha = pickle.load(open("./database/lph_data/lph_sypmstoms/tigejiancha_new.pkl", "r"))
    def get(self):
            id=self.get_argument('u_id')
            current={"name":self.get_argument('current')}
            all_data={"name": "张笑文",
                        "sex": "男",
                        "birthday": "1994/01/01",
                        "time": "20190101 ",
                 }
            self.render("doctor_cases.html",u_id=id,all_data=all_data,current=current,source='0')


    def post(self):
        u_id=self.get_argument('u_id')
        case={}
        print (u_id)

        self.render('check_detail.html',u_id=u_id,case=case)


class DoctorHuayanCaseHandler(tornado.web.RequestHandler):
    """
    医生输入化验检测页面控制器
    """

    huayan_dict = pickle.load(open("./database/lph_data/lph_sypmstoms/huayan_dict.pkl", "r"))
    id_name = pickle.load(open("./database/lph_data/lph_sypmstoms/id_name.pkl", "r"))
    huayan_excel = huayan_dict[u'xcg']
    pattern_list = [u'血液学常规检查', u'生化血脂', u'生化肾功', u'凝血四项', u'生化全项组合',
                    u'甲功全套', u'体液免疫', u'自身抗体', u'乙型肝炎标志五项',
                    u'血脂全项', u'风湿类风湿', u"乙肝检测"]
    pattern_str = u"|".join(pattern_list)
    pattern = re.compile(pattern_str)

    def get_age_index(self, p_age):
        ages_range = self.huayan_excel[u"儿童红细胞参数"].keys()
        p_age *= 365
        for index, age in enumerate(ages_range):
            if u"日" in age:
                two_age = [float(a) for a in age.split(u"日")[0].split(u"~")]
                if two_age[0] <= p_age <= two_age[-1]:
                    return index
                else:
                    continue
            elif u"月" in age:
                two_age = [float(a) * 30 for a in age.split(u"月")[0].split(u"~")]
                if two_age[0] <= p_age <= two_age[-1]:
                    return index
                else:
                    continue
            elif u"岁" in age:
                two_age = [float(a) * 365 for a in age.split(u"岁")[0].split(u"~")]
                if two_age[0] <= p_age <= two_age[-1]:
                    return index
                else:
                    continue
        return 0

    # def preprocess_huayan(self, patient_huayan):
    #     """
    #     预处理患者化验结果
    #     :param patient_huayan: 患者化验结果
    #     :return:
    #     """
    #     huayan_res = {}
    #
    #     if patient_huayan is None:
    #         return huayan_res
    #
    #     for hy_name in [u"儿童红细胞参数", u"儿童白细胞计数分类参数", u"儿童白细胞计数参考范围", u"儿童血小板参数"]:
    #         for h_k, h_v in patient_huayan[hy_name].items():
    #             if len(h_v) > 0:
    #                 normal_v = [float(v) for v in h_v[u"正常值"].split(u"~")]
    #                 try:
    #                     real_v = float(h_v[u"实际值"])
    #                     if len(normal_v) > 1:
    #                         low = normal_v[0]
    #                         high = normal_v[1]
    #                     else:
    #                         low = normal_v[0]
    #                         high = normal_v[0]
    #
    #                     if low <= real_v <= high:
    #                         huayan_res[h_k] = unicode(real_v) + u"，正常"
    #                     elif low > real_v:
    #                         huayan_res[h_k] = unicode(real_v) + u"，偏低"
    #                     elif high < real_v:
    #                         huayan_res[h_k] = unicode(real_v) + u"，偏高"
    #                 # except Exception, e:
    #                 #     huayan_res[h_k] = u"未输入"
    #     self.write(json.dumps(huayan_res))

    def generate_huayan_dict(self, huanyan_str):
        match = self.pattern.search(huanyan_str)
        pattern_pos = []
        while match:
            tgtxt = match.group()  # 匹配结果
            posd = match.span()
            match = self.pattern.search(huanyan_str, posd[1])  # 匹配下一个
            pattern_pos.append([tgtxt, posd])
        pattern_pos.append([u"", [len(huanyan_str), -1]])
        length = len(pattern_pos)
        res = {}
        for i in range(length - 1):
            res[pattern_pos[i][0]] = huanyan_str[pattern_pos[i][1][1]:pattern_pos[i + 1][1][0]]
        results = {}
        for key, value in res.items():
            zhibiao_list = value.split(u"  ★★  ")
            value_list = {}
            for zhibiao in zhibiao_list:
                # print u'########', zhibiao
                try:
                    zhibiao_key = zhibiao.split(u': ')[0].strip()
                    zhibiao_value = zhibiao.split(u': ')[1]
                    zhibiao_value_num = zhibiao_value.split(u'，')[0].strip()
                except Exception, e:
                    continue
                if u'正常' in zhibiao_value:
                    zhibiao_flag = 1
                elif u'偏低' in zhibiao_value:
                    zhibiao_flag = 2
                elif u'偏高' in zhibiao_value:
                    zhibiao_flag = 3
                else:
                    zhibiao_flag = 4
                # print zhibiao_flag
                value_list[zhibiao_key] = [zhibiao_value_num, zhibiao_flag]
            results[key] = value_list
        return results

    def get(self):
        user_type = self.get_secure_cookie("user_type")
        user_id = self.get_secure_cookie("user_id")
        if user_type == "1" and user_id is not None:
            doctor_id = self.get_secure_cookie("user_id")
            patient_id = self.get_argument("patientID")
            caseFirstID = self.get_argument("caseFirstID")
            caseSecondID = self.get_argument("caseSecondID")
            # print patient_id
            patient_res = cxDB.query_patient({u"patientID": patient_id})
            p_age_index = self.get_age_index(patient_res[0][u"age"])
            query_dict = {
                u'caseFirstID': caseFirstID,
                u'caseSecondID': caseSecondID
            }
            res_case = cxDB.query_case(query_dict)
            huayan_str = res_case[0][u'chemicalExamination']
            first_str = huayan_str.split(u"####识别结果如下###")[0]
            other_dict = self.generate_huayan_dict(first_str)
            temp = {}
            if other_dict.get(u'血液学常规检查', u"") != u"":
                for key, value in other_dict[u'血液学常规检查'].items():
                    new_keys = re.sub(u"([\u4e00-\u9fa5]+)", u"", key)[0:-2]
                    try:
                        if new_keys[-1] != u')':
                            new_keys = new_keys[0:-1]
                    except Exception:
                        pass
                    temp[new_keys] = value
                    # print key, new_keys
                other_dict[u'血液学常规检查'] = temp
            self.render("doctor_huayan.html", huayan_dict=self.huayan_dict, p_age_index=p_age_index,
                        caseFirstID=caseFirstID, caseSecondID=caseSecondID, patientID=patient_id, id_name=self.id_name,
                        other_dict=other_dict)


    def my_split(self, huanyan_str):
        match = self.pattern.search(huanyan_str)
        pattern_pos = []
        while match:
            tgtxt = match.group()  # 匹配结果
            posd = match.span()
            match = self.pattern.search(huanyan_str, posd[1])  # 匹配下一个
            pattern_pos.append([tgtxt, posd])
        pattern_pos.append([u"", [len(huanyan_str), -1]])
        length = len(pattern_pos)
        res = {}
        for i in range(length - 1):
            res[pattern_pos[i][0]] = huanyan_str[pattern_pos[i][1][1]:pattern_pos[i + 1][1][0]]
        return res

    def generate_huayan(self, hz_hy, id_name, add_str):
        res = self.my_split(hz_hy)
        res[id_name] = add_str
        huanyan_str = u""
        for key, value in res.items():
            huanyan_str += key + u'\n' + value.strip() + u'\n'
        return huanyan_str

    def post(self):
        huayan_str = self.get_argument("huayanStr")
        # 将前端传回的化验检测字符串转换为python字典格式
        doctor_id = self.get_secure_cookie("user_id")
        huayan_keys = [u"儿童红细胞参数", u"儿童白细胞计数参考范围", u"儿童白细胞计数分类参数", u"儿童血小板参数"]
        huayan_canshu = {}
        four_parts = huayan_str.split(u"#")
        for index, key in enumerate(huayan_keys):
            huayan_canshu[key] = {}
            for zhibiao in four_parts[index].split(u";"):
                if zhibiao.split(u":")[0] != u"":
                    huayan_canshu[key][zhibiao.split(u":")[0]] = {
                        u"正常值": u"" + zhibiao.split(u":")[-1].split(u",")[0],
                        u"实际值": u"" + zhibiao.split(u":")[-1].split(u",")[-1],
                    }
        ca_dict = {
            u"caseFirstID": int(self.get_argument("caseFirstID")),
            u"caseSecondID": int(self.get_argument("caseSecondID")),
            u"doctorID": doctor_id
        }
        q_res = cxDB.query_case(ca_dict)
        ca_dict[u"info"] = json.dumps(huayan_canshu, encoding="utf-8", ensure_ascii=False)

        processed_huayan = self.preprocess_huayan(huayan_canshu)
        ph_str = u''
        for ph_key, ph_value in processed_huayan.items():
            if ph_value != u"未输入":
                cs_shuoming = huayan_canshu_shuoming.huayancanshu_shuoming.get(ph_key, {u"名称": ph_key, u"参考范围": u"暂无",
                                                                                        u"临床意义": u"暂无"})
                ph_str += ph_key + u'({})'.format(cs_shuoming.get(u'名称')) + u": " + ph_value + u"  ★★  "
        huanyan_str = self.generate_huayan(q_res[0][u'chemicalExamination'], u'血液学常规检查', ph_str[0:-4])
        # print huayan_str

        self.write(json.dumps(huanyan_str))


class DoctorCaseMedicineHandler(tornado.web.RequestHandler):
    """
    点击选择药物后，弹出的药物界面控制器
    """

    def get(self):
        hz_xbs = self.get_argument("hz_xbs")
        hz_zs = self.get_argument("hz_zs")
        hz_xy = self.get_argument("hz_xy")
        hz_tg = self.get_argument("hz_tg")
        query = u'。'.join([hz_zs, hz_xbs, hz_xy, hz_tg])
        medicines = recommend_search(query)
        self.render('doctor_case_medicine.html', medicines=medicines, diseases=hz_xy)
