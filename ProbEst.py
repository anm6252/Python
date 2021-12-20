# -*- coding: utf-8 -*-

print("Data 51100 - Fall 2021")
print("Name: Allison MacDonald")
print("Programming Assignment #4")

import pandas as pd

### Data imported
data = pd.read_csv("cars.csv")

### Choosing the model and aspiration columns
colData = data[['make', 'aspiration']]

makeData = (colData['make'].value_counts() / colData['make'].count() * 100).round(2)
aspData = (colData['aspiration'].value_counts() / colData['aspiration'].count() * 100)

dataFrame = pd.DataFrame({'make': makeData.index.unique(), 'make_prob': makeData.values})


### Conditional Probabilities

for make in colData['make'].unique():
    for asp in colData['aspiration'].unique():
        makeFrame = colData[colData['make'] == make]
        makeCount = makeFrame.shape[0]
        probFrame = makeFrame[makeFrame['aspiration'] == asp]
        probCount = probFrame.shape[0]
      
        if probCount != 0:
            print("Prob(aspiration=" + asp + "|make=" + make + ")" + " = " + str(round(100 * probCount / makeCount, 2)) + "%")
      
        else:
            print("Prob(aspiration=" + asp + "|make=" + make + ")" + " = " + str(0) + "%")

print("\n")


for make in colData['make'].unique():
    print("Prob(make=" + make + ") = " + str(round(data['make'].value_counts().loc[make] / data['make'].value_counts().sum() * 100, 2)) + "%")