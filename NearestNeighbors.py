# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:06:11 2021

@author: allma
"""

import numpy as np
print("DATA-51100, Fall 20101")
print("NAME: Allison MacDonald")
print("PROGRAMMING ASSIGNMENT #3")

### Data Import
trainData = "iris-training-data.csv"
testData = "iris-testing-data.csv"

#### 2D arrays for the testing and training data
trainArr = np.loadtxt(trainData, delimiter=',', usecols=(0, 1, 2, 3))
testArr = np.loadtxt(testData, delimiter=',', usecols=(0, 1, 2, 3))

### 1D array to store labels
trainClasses = np.loadtxt(trainData, dtype='<U15', delimiter=',', usecols=4)
testClasses = np.loadtxt(testData, dtype='<U15', delimiter=',', usecols=4)

### Calculating distance
dist  = np.sqrt((np.square(testArr[:, np.newaxis]-trainArr)).sum(axis=2))
min_dist = dist.argmin(axis=1) 


predLables = np.array([[trainClasses[i]] for i in min_dist]).reshape(trainClasses.shape)

### Accuracy calculated from the trainData import
acc = ((predLables == testClasses).sum())/(len(predLables))

print("#, TRUE, PREDICTED")
for i in range(len(predLables)):
    print("%d, %s, %s" % (i+1, testClasses[i], predLables[i]))

print("Accuracy: %.2f%%" % (acc*100))