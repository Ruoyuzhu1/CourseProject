#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:19:08 2020

@author: guanhuali
"""



from sklearn import model_selection, preprocessing, metrics
from sklearn import ensemble
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

feature = pd.read_csv('part1features.csv',skip_blank_lines = True).dropna()

labels = np.array(feature['label'])

feature = feature.drop('label',axis=1)

feature = np.array(feature)

train_x, test_x, train_y, test_y = model_selection.train_test_split(feature, labels, test_size = 0.05)

rf = RandomForestClassifier(n_estimators = 200, random_state = 100)
    
rf.fit(train_x, train_y)

prediction = rf.predict(test_x)

result = metrics.accuracy_score(prediction, test_y)

cfmatrix = metrics.confusion_matrix(test_y,prediction)


with open('rf_classifier1', 'wb') as picklefile:
     pickle.dump(rf,picklefile)

print(result)
print(cfmatrix)
sns.heatmap(cfmatrix,annot=True)
plt.show()

