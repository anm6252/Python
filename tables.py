# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 07:33:36 2021

@author: allma
"""

print("DATA-51100, Fall, 2021")
print("NAME: Allison MacDonald")
print("PROGRAMMING ASSIGNMENT #7")

import pandas as pd
from pandas import Series, DataFrame
import numpy as np

### Format
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

### Data Frame
DF = pd.read_csv('ss13hil.csv')


##### TABLE #1: DESCRIPTIVE STATISTICS OF HINCP,GROUPED BY HHT #####

### Groupby
groupTable1 = DF['HINCP'].groupby(DF['HHT'])

def getStatsOne(group):
    return {'mean': group.mean(),'std': group.std(),'count': group.count(),'min':group.min(),'max':group.max()}

stackTable1 = groupTable1.apply(getStatsOne)

### Table Labels
HHT_Stats = {
1:'Married couple household',
2:'Other family household:Male householder, no wife present',
3:'Other family household:Female householder, no husband present',
4:'Nonfamily household:Male householder:Living alone',
5:'Nonfamily household:Male householder:Not living alone',
6:'Nonfamily household:Female householder:Living alone',
7:'Nonfamily household:Female householder:Not living alone'}

stackTable1.rename(index = HHT_Stats, inplace=True)

### Unstacking and Sorting
tableOne = stackTable1.unstack(level=-1)
tableOne.sort_values('mean',ascending=False, inplace=True)

### Renaming the Main Title
tableOne.index.names = ['HHT - Household/Family Type']
tableOne = tableOne[['mean','std','count','min','max']]

### Removing of Decimals
tableOne['count'] = tableOne['count'].astype(int)
tableOne['min'] = tableOne['min'].astype(int)
tableOne['max'] = tableOne['max'].astype(int)

### Printing the Table
print("*** Table 1 - Descriptive Statistics of HINCP, grouped by HHT ***")
print(tableOne)
print("")



##### TABLE #2: HHL VS. ACCESS - FREQUENCY TABLE #####

tableTwo = DF[['HHL','ACCESS','WGTP']].dropna()

### Table Labels
HHL_Titles = {
1:'English Only',
2:'Spanish',
3:'Other Indo-European Languages',
4:'Asian and Pacific Island Languages',
5:'Other Language'}

ACCESS_Titles = {
1:'Yes w/ Subsrc.',
2:'Yes, wo/ Subsrc.',
3:'No'}

### Groupby
groupTable2 =  tableTwo.groupby(['HHL','ACCESS'])['WGTP']

### Getting Sums for each Group
def getSums(group):
    return {'WGTP':group.sum()}

### Sum Application
stackTable2 = groupTable2.apply(getSums) 
stackTable2 = stackTable2/tableTwo['WGTP'].sum()

### Unstacking
tableTwoFinal = stackTable2.unstack(level=-1).unstack(level=-1)

### Changing/Adding Titles
tableTwoFinal.rename(index = HHL_Titles, inplace = True)
tableTwoFinal.index.names = ['HHL - Household Language']
tableTwoFinal.rename(columns = ACCESS_Titles, inplace = True)

### Sums of the Columns
tableSums = tableTwoFinal['WGTP','Yes w/ Subsrc.'] + tableTwoFinal['WGTP','Yes, wo/ Subsrc.']+tableTwoFinal['WGTP','No']
tableTwoFinal['WGTP','All'] = tableSums

tableTwoFinal.loc['All'] = tableTwoFinal.sum()

### Formatting the Table
tableTwoFinal['WGTP','Yes w/ Subsrc.'] = pd.Series(["{0:.2f}%".format(val * 100) for val in tableTwoFinal['WGTP','Yes w/ Subsrc.']], index = tableTwoFinal.index)
tableTwoFinal['WGTP','Yes, wo/ Subsrc.'] = pd.Series(["{0:.2f}%".format(val * 100) for val in tableTwoFinal['WGTP','Yes, wo/ Subsrc.']], index = tableTwoFinal.index)
tableTwoFinal['WGTP','No'] = pd.Series(["{0:.2f}%".format(val * 100) for val in tableTwoFinal['WGTP','No']], index = tableTwoFinal.index)
tableTwoFinal['WGTP','All'] = pd.Series(["{0:.2f}%".format(val * 100) for val in tableTwoFinal['WGTP','All']], index = tableTwoFinal.index)

### Printing the Table
print("*** Table 2 - HHL vs. ACCESS - Frequency Table ***")
print("                                              sum")
print(tableTwoFinal)
print("")



##### TABLE #3: QUANTILE ANALYSIS OF HINCP - HOUSEHOLD INCOME (PAST 12 MONTHS) #####

tableThree = DF[['HINCP','WGTP']].dropna()

### Groupby
groupTable3 =  tableThree.groupby(pd.qcut(tableThree['HINCP'], 3, labels = ["low", "medium", "high"]))

def getColumns(group):
    return {'min':group.min(),'max':group.max(),'mean':group.mean(),'household_count':group['WGTP'].sum()}

### Stacking 
stackTable3 = groupTable3.apply(getColumns)

### Cleaning the Quartiles
def getQuartiles(quartile):
    return {'min':quartile['min'][0],'max':quartile['max'][0],'mean':quartile['mean'][0].round(6),'household_count':quartile['household_count']}

### Resetting the values
stackTable3['low'] = getQuartiles(stackTable3['low'])
stackTable3['medium'] = getQuartiles(stackTable3['medium'])
stackTable3['high'] = getQuartiles(stackTable3['high'])


lowQuart = stackTable3['low'].values
medQuart = stackTable3['medium'].values
highQuart = stackTable3['high'].values

### New DataFrame
tableThreeFinal = pd.DataFrame({
    'min':[lowQuart[3],medQuart[3],highQuart[3]],
    'max':[lowQuart[0],medQuart[0],highQuart[0]],
    'mean':[lowQuart[1],medQuart[1],highQuart[1]],
    'household_count':[lowQuart[2],medQuart[2],highQuart[2]]}, index = ['low','medium','high'])

tableThreeFinal = tableThreeFinal[['min','max','mean','household_count']]

### Adding the Table Title 
tableThreeFinal.index.name = 'HINCP'

### Print Table
print("*** Table 3 - Quantile Analysis of HINCP - Household income (past 12 months) ***")
print(tableThreeFinal)