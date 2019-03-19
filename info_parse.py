# -*- coding: utf-8 -*-#
#coding=utf-8
import os
import re
from query_v3 import query_data
#def run_parse(key1,key2,key3,key5):
def run_parse(key1,key2):
    all_info_list = []  # 存储所有信息
    info_list=[]
    result_list=[]
    l_info_list=[]
    path = r"./regular/age_regular.txt"
    regular_file = open(path)
    # print("打开文件成功")
    regular_list = []
    line = regular_file.readline()

    #读取正则匹配的年龄规则
    while line:
        line = line.strip('\n')
        regular_list.append(line)
        line = regular_file.readline()
    regular_file.close()

    path = r"./regular/special_body.txt"
    regular_file = open(path)
    # print("打开文件成功")
    special_list = []
    line = regular_file.readline()

    #读取特殊体质匹配的规则
    while line:
        line = line.strip('\n')
        special_list.append(line)
        line = regular_file.readline()
    regular_file.close()





    #将所有句子的年龄字段全部提取，这个是如果本条信息如果未涉及年龄字段则查找父亲节点出现的年龄字段赋值给子节点
    def get_father(top_bottom,all_info_list,fahter_id,search_id):
        for x in info_list:
            if fahter_id==x[0]:
                if search_id==0:
                    top_bottom=top_bottom+x[3]
                    return top_bottom
                else:
                    top_bottom=top_bottom+x[4]
                    return top_bottom
    #用条件判断语句将年龄信息全部提取
    def get_age(all_info_list):
        for t in all_info_list:
            top = []
            bottom = []
            # print("t:",t)
            for i in range(0, len(regular_list)):
                pattern = re.compile(regular_list[i], re.U)  # re.I 表示忽略大小写
                m = pattern.findall(t[1])
                # print(m)
                if len(m) > 0:
                    for x in m:
                        if i==0:
                            if x.find('-')>=0:
                                result=x.split('-')
                            elif x.find('~')>=0:
                                result=x.split('~')
                            elif x.find('〜')>=0:
                                result=x.split('〜')
                            # print(result)
                            x1 = re.findall("\d+", result[0])[0]
                            x2 = re.findall("\d+", result[1])[0]
                            bottom.append(float(x1))
                            top.append(float(x2))
                        elif i==1:
                            if x.find('-')>=0:
                                result=x.split('-')
                            elif x.find('~')>=0:
                                result=x.split('~')
                            elif x.find('〜')>=0:
                                result=x.split('〜')
                            # print(result)
                            x1 = re.findall("\d+", result[0])[0]
                            x2 = re.findall("\d+", result[1])[0]
                            bottom.append(float(x1)*12)
                            top.append(float(x2)*12)
                        elif i==2:
                            if x.find('-')>=0:
                                result=x.split('-')
                            elif x.find('~')>=0:
                                result=x.split('~')
                            elif x.find('〜')>=0:
                                result=x.split('〜')
                            # print(result)
                            x1 = re.findall("\d+", result[0])[0]
                            x2 = re.findall("\d+", result[1])[0]
                            bottom.append(float(x1))
                            top.append(float(x2)*12)
                        elif i==3:
                            if x.find('-') >= 0:
                                result = x.split('-')
                            elif x.find('~') >= 0:
                                result = x.split('~')
                            elif x.find('〜') >= 0:
                                result = x.split('〜')
                            # print(result)
                            x1 = re.findall("\d+", result[0])[0]
                            x2 = re.findall("\d+", result[1])[0]
                            bottom.append(float(x1)/30*7)
                            top.append(float(x2)/30*7)
                        elif i==4:
                            x = re.findall("\d+",x)[0]
                            top.append(float(x)/30*7)
                            # print("top",top)
                        elif i==5:
                            x = re.findall("\d+", x)[0]
                            bottom.append(float(x)/30*7)
                            # print("bottom", bottom)
                        elif i==7:
                            x = re.findall("\d+",x)[0]
                            top.append(float(x)*12)
                            # print("top",top)
                        elif i==6:
                            x = re.findall("\d+", x)[0]
                            bottom.append(float(x)*12)
                            # print("bottom", bottom)
                        elif i == 8:
                            x = re.findall("\d+", x)[0]
                            top.append(float(x) * 12)
                            # print("top",top)

                        elif i == 9:
                            x = re.findall("\d+", x)[0]
                            top.append(float(x))
                            # print("top",top)

                        elif i==10:
                            x = re.findall("\d+",x)[0]
                            top.append(float(x)/30*7)
                            # print("top",top)
                        elif i==11:
                            x = re.findall("\d+", x)[0]
                            bottom.append(float(x)/30*7)
                            # print("bottom", bottom)

                        elif i==12:
                            x = re.findall("\d+",x)[0]
                            bottom.append(float(x))
                            # print("top",top)
                        elif i==13:
                            x = re.findall("\d+", x)[0]
                            bottom.append(float(x))
                            # print("bottom", bottom)
                        elif i==14:
                            x = re.findall("\d+", x)[0]
                            bottom.append(float(x)*12)
                            # print("bottom", bottom)
                        elif i==15:
                            x = re.findall("\d+",x)[0]
                            top.append(float(x))
                            # print("top",top)
                        elif i==16:
                            x = re.findall("\d+",x)[0]
                            top.append(float(x))
                            # print("top",top)
                        elif i==17:
                            x = re.findall("\d+",x)[0]
                            top.append(float(x)*12)
                            # print("top",top)
                        elif i==18:
                            x = re.findall("\d+",x)[0]
                            top.append(float(x))
                            # print("top",top)
                        elif i==19:
                            x = re.findall("\d+",x)[0]
                            top.append(float(x))
                            # print("top",top)
                        #之前测试代码
                        # elif i==1:
                        #     x = re.findall("\d+", x)[0]
                        #     bottom.append(x)
                        #     # print("bottom", bottom)
                        # elif i == 2:
                        #     x = re.findall("\d+", x)[0]
                        #     top .append(x)
                        #     # print("top", top)
                        # elif i == 3:
                        #     x = re.findall("\d+", x)[0]
                        #     bottom.append(x)
                        #     # print("bottom", bottom)
                        # elif i==4:
                        #     if x.find('-')>=0:
                        #         result=x.split('-')
                        #     elif x.find('~')>=0:
                        #         result=x.split('~')
                        #     elif x.find('〜')>=0:
                        #         result=x.split('〜')
                        #     # print(result)
                        #     x1 = re.findall("\d+", result[0])[0]
                        #     x2 = re.findall("\d+", result[1])[0]
                        #     bottom.append(x1)
                        #     top.append(x2)
                            # print("top", top)
                            # print("bottom", bottom)
            # print("node:",t[0])

            father = ""
            str = t[0].split('.')
            len_str = len(str)
            if len_str > 2:
                for j in range(0, len_str - 2):
                    father = father + str[j] + "."
                    # 现打印下父亲节点的ID值
                father=father+')'
                # print("father:", father + ')')
            if len(top)==0 and father!='':
                top=get_father(top,info_list,father,0)
            if len(bottom)==0 and father!='':
                bottom=get_father(bottom,info_list,father,1)
            t.append(father)
            t.append(top)
            t.append(bottom)
            info_list.append(t)

    # def get_special_status(info_list):
    #     normal_status=["健康"]
    #     auxiliary=False
    #     for t in info_list:
    #         # special_status.clear()
    #         for i in range(0, len(special_list)):
    #             pattern = re.compile(special_list[i], re.U)  # re.I 表示忽略大小写
    #             m = pattern.findall(t[1])
    #             if len(m) > 0:
    #                 special_status = []
    #                 special_status.append(special_list[i])
    #
    #                 auxiliary=True
    #         if auxiliary==False:
    #             t.append(normal_status)
    #             l_info_list.append(t)
    #         elif auxiliary==True:
    #             t.append(special_status)
    #             l_info_list.append(t)
    #
    #         # print(t)
    #
    #         auxiliary=False
    #到时候存数据库再说
    # ret = cur.executemany("insert into sentence_data ('cid','content','fatherID','top_age','bottom_age')values(%s,%s,%s,%s,%s)", )
    # # 提交
    # conn.commit()
    # cur.close()
    # #关闭连接对象
    # conn.close()


    input_path = r'./testdata.txt'
    pattern = re.compile(u"^\(.*?\)", re.U)  # re.I 表示忽略大小写

    open_file = open(input_path)
    # print("打开文件成功")
    line = open_file.readline()
    line=line.strip('\n')

    #将所有的信息按找ID+内容的形式存储到list中
    while line:
        # print(line)
        row_list = []
        m=pattern.match(line)
        if m:
            # print(m.group())

            # seg=re.split("[。；;]",line[len(m.group()):])
            # for x in seg:
            #     print x
            row_list.append(m.group())
            row_list.append(line[len(m.group()):])
            # row_list.append(line[len(m.group()):])
            all_info_list.append(row_list)
        line = open_file.readline()
        line=line.strip('\n')
    open_file.close()
    get_age(all_info_list)
    # get_special_status(info_list)
    return query_data( info_list,key1,key2)



