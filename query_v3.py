# -*- coding: utf-8 -*-#
#coding=utf-8
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import io
possible_list=[]
temp_list=[]
finally_list=[]

path = r"./regular/id_regular.txt"
regular_file = open(path)
print("打开文件成功")
regular_list = []
line = regular_file.readline()
while line:
    line = line.strip('\n')
    regular_list.append(line)
    line = regular_file.readline()
regular_file.close()
# print regular_list

# def marking(auxiliary_array):
#     # print("------打分步骤------")
#     pc=0
#     result=0
#     for x in range(0,len(auxiliary_array)):
#         if auxiliary_array[x]>0:
#             pc=pc+1
#         else:
#             temp=0
#             if pc==1:
#                 temp=1
#             elif pc==2:
#                 temp = 10
#             elif pc==3:
#                 temp=100
#             elif pc==4:
#                 temp=1000
#             elif pc==5:
#                 temp=10000
#             elif pc==6:
#                 temp=100000
#             pc=0
#             result=result+temp
#     return result



def query_data(info_list,keyword1,keyword2):
    start_list=[]
    possible_list=[]
    temp_list=[]
    finally_list=[]
    #前面可以添加主题分类信息，先按照主题选择对应的文章集合，再去找有用的信息，缩小查询范围
    keyword1 = re.findall("\d+", keyword1)[0]

    #筛选出内容相关的几段
    # for x in range(0,len(info_list)):
    #     for y in regular_list:
    #         # p = re.compile(y)
    #         # print str(info_list[x][1]).decode('utf-8')
    #         # print type(y),type(info_list[x][1])
    #         # temp=re.sub(y.decode('utf-8'), '', info_list[x][1].decode('utf-8'))
    #         # print y
    #
    #         m=re.findall(y.encode('utf-8'),info_list[x][1],re.U)
    #         # print info_list[x][1]
    #         if len(m)>0:
    #             # print m[0]
    #             temp=info_list[x][1].replace(m[0],"")
    #             # print temp
    #         else:
    #             temp=info_list[x][1]
    #
    #         # temp=temp.decode('ascii','ignore').encode('utf-8')
    #         # print temp,keyword3
    #         # keyword3='u\''+keyword3+'\''
    #         # keyword3.encode('utf-8')
    #         temp=temp.strip()
    #         cmp2=(u''+keyword3+u'').encode('utf-8')
    #         cmp2=cmp2.strip()
    #         # print cmp2
    #         # print chardet.detect(cmp2)
    #         # print 'temp:',temp,'key:',cmp2
    #         if temp==cmp2:
    #             ID=info_list[x][0]
    #             x=x+1
    #             while (info_list[x][2]==ID):
    #
    #                 start_list.append(info_list[x])
    #                 x = x + 1
    #
    # print  str(start_list).decode("string_escape")
    for x in info_list:
        if len(x[3])>0:
            top=int(max(x[3]))
        else:
            top=65535
        if len(x[4]) > 0:
            bottom = int(min(x[4]))
        else:
            bottom=0
        temp=int(keyword1)
        if temp<=top and temp>=bottom:
            possible_list.append(x)
    keyword2=str(keyword2)
    # print(str(possible_list).decode("string_escape"))
    for x in possible_list:
        temp=x[1]

        # m = re.findall(keyword2,temp, re.U)
        if keyword2 in temp:
            # print keyword2, temp
            temp_list.append(x[1])
    for x in temp_list:
        temp=x.decode('utf-8')
        print(temp)
        Pos=temp.find(keyword2)

        while Pos!=-1:
            start=Pos-1
            while start >0:

                if temp[start]=='。' or temp[start]==':' or temp[start]=='；' or temp[start]==';':
                    break
                else:
                    start=start-1

            finally_list.append(temp[start:Pos])
            Pos=temp.find(keyword2,Pos+1)

    # 年龄配对后的留下的信息
    # for x in possible_list:
    #
    #     for t in x[5]:
    #         cmp1=t.decode("utf-8")
    #         cmp2=keyword2
    #         # print cmp1,keyword2,t
    #         if cmp1==cmp2:
    #             temp_list.append(x)
    #             break
    # print(temp_list)
    # print(str(temp_list).decode("string_escape"))
    store_goal=[]
    #匹配条目二之后留下来的信息
    # for x in temp_list:
    #     auxiliary_array=[]
    #     transfer = x[1].decode("utf-8")
    #     for i in range(0,len(transfer)):
    #         # print transfer
    #         for j in range(0,len(keyword5)):
    #             temp=keyword5[j]
    #             cmp1=temp
    #             cmp2=transfer[i]
    #
    #             if cmp1==cmp2:
    #                 auxiliary_array.append(j+1)
    #             else:
    #                 auxiliary_array.append(0)
    #     goal=marking(auxiliary_array)
    #     # finally_list.append(x)
    #     store_goal.append(goal)
    #     # finally_list.append(goal)
    # print(finally_list)



    #大于2条则返回评分最高的2条
    # if len(temp_list)>=2:
    #     for i in range(0,len(temp_list)):
    #         index = store_goal.index(max(store_goal))
    #         print(temp_list[index][1], store_goal[index])
    #         if(store_goal[index]>5 ):
    #             finally_list.append(temp_list[index][1])
    #             store_goal[store_goal.index(max(store_goal))] = -1
    #         else:
    #             print("无结果")
    #             break;
    #     # index = store_goal.index(max(store_goal))
    #     # print(temp_list[index][1], store_goal[index])
    #     # if(store_goal[index]>5):
    #     #     finally_list.append(temp_list[index][1])
    #     # else:
    #     #     print("无结果")
    #0条或者所有条目评分都为0则无返回结果
    # elif len(temp_list)==0 or max(store_goal)==0:
    #     print("无返回结果")
    #小于2条只输出评分大于0的条目
    # else:
    #     for i in range(0,len(temp_list)):
    #         if store_goal[i]>5:
    #             print(temp_list[i][1],store_goal[i])
    #             finally_list.append(temp_list[i][1])
    return finally_list
    # result = model.most_similar(u'喂养')
    #
    # for word in result:
    #     print (word[0], word[1])
    # print("------------------")
    # result = model.most_similar(u'食物')
    #
    # for word in result:
    #
    #     print (word[0], word[1])
