# -*- coding=utf-8 -*-
# coding=utf-8

from a_handlers import *

import json,pickle,time,re,Levenshtein,base64,datetime,random
import os.path
import requests
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options, parse_command_line


define("port", default=3388, help="run on the given port", type=int)


class MakeApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/child/doctor_home", DoctorHomeHandler),
            (r"/child/login", LoginHandler),
            (r"/child/doctor_case/([0-9]*)", DoctorCaseHandler),
            (r"/child/doctor_huayan_case", DoctorHuayanCaseHandler),
            (r"/child/doctor_case_medicine", DoctorCaseMedicineHandler),
            (r"/child/check_detail", CheckDetailHandler),
            (r"/child/check_inquiry_detail", CheckInquiryDetailHandler),
            (r"/child/doctor_record", HealthCheckHandler),
            (r"/child/patient_record", HealthRecordHandler),
            (r"/child/reloadimg", ReloadImgHandler),
            (r"/child/judgeisexist", JudgeIsExistHandler),
            (r"/child/storehealthrecord", StoreHealthRecordHandler),
            (r"/child/storeinquiryrecord", StoreInquiryRecordHandler),
            (r"/child/judgeinqueryisexist", JudgeInqueryIsExistHandler),
            (r"/child/patient_standard", PatientStandardHandler),
            (r"/child/judge_times_existed", JudgeTimesAndIsExisted),
            (r"/child/get_advice", GetAdvice),
            (r"/child/get_growthstandard", GetGrowthStandard),
            (r"/child/doctor_case", DoctorCaseHandler)

            # (r"/child/login", LoginHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret='81oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
            # login_url='/child/login'
            login_url='/child/login'
        )
        super(MakeApp, self).__init__(handlers, **settings)


def main():
    parse_command_line()
    app = MakeApp()
    app.listen(options.port, address="0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
