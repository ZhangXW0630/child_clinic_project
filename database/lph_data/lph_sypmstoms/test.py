#coding=utf-8
import pickle
id_name = pickle.load(open(u"id_name.pkl", 'r'))
huayan_dict = pickle.load(open(u"huayan_dict.pkl", "r"))
for key,value in id_name.items():
    print key, value

id_name[u"ygjc"] = u"乙肝检测"


huayan_dict[u"ygjc"] = {
    u"谷丙转氨酶(ALT)": u"0-40",
    u"乙肝表面抗原(HBsAg)": u"阳性",
    u"乙肝表面抗体(HBsAb)": u"阳性",
    u"乙肝E抗原(HBeAg)": u"阴性",
    u"乙肝E抗体(HBeAb)": u"阴性",
    u"乙肝核心抗体(HBcAb)": u"阴性"
}
with open(u"huayan_dict.pkl", "w") as f:
    pickle.dump(huayan_dict, f)

