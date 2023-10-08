#!/usr/bin/python3

# scikit-learn k-fold cross-validation
import sys
from sklearn.model_selection import KFold
from numpy import array

# data sample
data_file = sys.argv[1]
with open(data_file, "r") as f:
    data = array(f.readlines())
    # prepare cross validation
    kfold = KFold(n_splits=5, shuffle=True)
    # enumerate splits
    index = 1
    for train, test in kfold.split(data):
        #print(train, test)
    	#print('train: %s, test: %s' % (data[train], data[test]))
        with open("train_"+str(index)+".tsv", "w") as output:
            for rec in data[train]:
                output.write(rec)
        with open("dev_"+str(index)+".tsv", "w") as output:
            for rec in data[test]:
                output.write(rec)
        index +=1
