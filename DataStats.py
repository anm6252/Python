# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 15:45:20 2021

@author: allma
"""

import pandas as pd
import numpy as np
import re

print("DATA 51100 - Fall 2021")
print("NAME: Allison MacDonald")
print("PROGRAMMING ASSIGNMENT #5")

### Reading in the data file
dataFile = pd.read_csv('cps.csv')

### Creating the DataFrame
dataColumns = dataFile[
    ['School_ID', 'Short_Name', 'Is_High_School', 'Zip', 'Student_Count_Total', 'College_Enrollment_Rate_School',
     'Grades_Offered_All', 'School_Hours']].sort_index()

### Grades
dataColumns['Lowest_Grade_Offered'] = dataColumns.apply(lambda x: x['Grades_Offered_All'][0:2], 1).str.replace(",",
                                                                                                                   '')
dataColumns['Highest_Grade_Offered'] = dataColumns.apply(lambda x: x['Grades_Offered_All'][-2:], 1).str.replace(",",
                                                                                                                    '')

### Replacing the missing numeric values
def start(x):
    if str(x[0]) == 'nan':
        return 0
    else:
        return int(re.findall(r'[1-9]', x[0])[0])

time = dataColumns[['School_Hours']].apply(start, axis=1)
dataColumns = dataColumns.assign(Starting_Hour=time)

for num in dataColumns.select_dtypes(['int64', 'float64']).columns:
    dataColumns[num].fillna(dataColumns[num].mean(), inplace=True)


# Display the first 10 rows of this dataframe
dataColumns = dataColumns.drop(['Grades_Offered_All', 'School_Hours'], axis=1)

print(dataColumns.head(10))


### Mean of College Enrollment Rate for High Schools
meanEnroll = dataColumns.groupby('Is_High_School')['College_Enrollment_Rate_School'].mean()


### Standard deviation of College Enrollment Rate for High Schools
SDEnroll = dataColumns.groupby('Is_High_School')['College_Enrollment_Rate_School'].std()

print("College Enrollment Rate for High Schools = ", meanEnroll[1].round(2), "(sd=", SDEnroll[1].round(2), ")", "\n")


### Mean and standard deviation of Student_Count_Total for non-High Schools
meanCountTotal = dataColumns.groupby('Is_High_School')['Student_Count_Total'].mean()
SDCountTotal = dataColumns.groupby('Is_High_School')['Student_Count_Total'].std()

print("Total Student Count for non-High Schools = ", meanCountTotal[0].round(2), "(sd=", SDCountTotal[0].round(2), ")", "\n")


### Distribution of starting hours for all schools
seven = []
eight = []
nine = []

for n in dataColumns['Starting_Hour']:
    if n == 7:
        seven.append(n)
    if n == 8:
        eight.append(n)
    if n == 9:
        nine.append(n)

print("Distribution of Starting Hours")
print("7am: ", len(seven))
print("8am: ", len(eight))
print("9am: ", len(nine), "\n")


### Number of schools outside of the Loop Neighborhood (i.e., outside of zip codes 60601, 60602, 60603, 60604, 60605, 60606, 60607, and 60616)
zipcodes = [60601, 60602, 60603, 60604, 60605, 60606, 60607, 60616]
outsideLoop = []
for zips in dataColumns['Zip']:
    if zips not in zipcodes:
        outsideLoop.append(zips)


print("Number of schools outside the Loop Neighborhood: ", len(outsideLoop))