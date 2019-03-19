#coding=utf-8
import pickle
import codecs
fs_out = codecs.open("a.txt", "r", "utf-8")
alllines = fs_out.readlines()
res = {}
for line in alllines:
    line = line.strip()
    k = line.split(u":")[0]
    res[k] = line.split(u":")[1].split(u",")
with open("skin_points.pkl", "w") as f:
    pickle.dump(res, f)