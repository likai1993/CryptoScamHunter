#!/usr/bin/python3

# scikit-learn k-fold cross-validation
import sys
from sklearn.model_selection import KFold
from numpy import array

# data sample
data_file = sys.argv[1]
with open("title/"+data_file, "w") as output1:
    with open("desp/"+data_file, "w") as output2:
        with open(data_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                tp = line.split("\t")[0]
                if tp[0] == "\"":
                    title = line.split("\t")[0].split("\",")[0] + "\""
                    desp = line.split("\t")[0].split("\",")[1:]
                    if len(desp) == 0:
                        #print(desp)
                        desp = ["\""]
                    label = line.split("\t")[1]
                    output1.write(title+"\t"+label)
                    output2.write('\",'.join(desp)+"\t"+label)
                else:
                    title = line.split("\t")[0].split(",")[0]
                    desp = line.split("\t")[0].split(",")[1:]
                    if len(desp) == 0:
                        desp = ["\""]
                    label = line.split("\t")[1]
                    output1.write(title+"\t"+label)
                    output2.write(','.join(desp)+"\t"+label)
