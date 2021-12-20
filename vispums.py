# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib as mpl
import pandas as pd
from pandas import DataFrame
import numpy as np

print("Data-51100. Fall 2021")
print("NAME: Allison MacDonald, Bryon Czaja")
print("PROGRAMMING ASSIGNMENT #6")


size1 = 10 ### For Axis Title
size2= 14 ### For Larger, Main Title
size3 = 7 ### Legend 

### Data Loading
data = pd.read_csv('ss13hil.csv')

### Create Figure with 2x2 Subplot
figure, ax = plt.subplots(2, 2)

figure.subplots_adjust(hspace=0.40)
figure.set_size_inches(14, 7)



##### PIE CHART #####

### Pie Chart Set-up
ax[0,0].set_title('Household Languages', fontsize = size2)    
ax[0,0].set_ylabel('HHL', fontsize = size1) 

### Data Plotting  
ax[0,0].pie(data.HHL.value_counts().dropna(), startangle=242)
ax[0,0].axis('equal')

### Language Key For Pie Chart
languages = ['English Only', 'Spanish', 'Other Indo-European', 'Asian and Pacific Island Languages', 'Other']
ax[0,0].legend(languages, loc = 2, fontsize = size3)



##### HISTOGRAM #####

### Histogram Set-up
ax[0,1].set_title('Distribution of Household Income', fontsize = size2)
ax[0,1].set_xlabel('Household Income($) - Log Scaled', fontsize = size1)
ax[0,1].set_ylabel('Density', fontsize = size1)

### Data Scaling
bins = np.logspace(1,7,100)
ax[0,1].set_xscale('log')

### Y-axis Labels
mticker = ticker.ScalarFormatter(useOffset=False)
mticker.set_powerlimits((-6, 6))
ax[0,1].yaxis.set_major_formatter(mticker)
ax[0,1].yaxis.set_minor_formatter(mticker)

### Data Plotting
histData = data.HINCP.dropna()

ax[0,1].hist(histData, bins, density = True, facecolor = 'green', alpha = 0.5)
histData.plot(kind = 'kde', ax = ax[0,1], color = 'k', linestyle = '--')


##### BAR GRAPH #####

### Bar Graph Set-up
ax[1,0].set_title('Vehicles Available in Households', fontsize = size2)
ax[1,0].set_xlabel('# of Vehicles', fontsize = size1)
ax[1,0].set_ylabel('Thousands of Households', fontsize = size1)

### Data Plotting
barData = data.groupby('VEH')['WGTP'].sum()/1000
ax[1,0].bar(barData.index, barData.values, facecolor = 'red')



##### SCATTER PLOT #####

### Scatter Plot Set-up
ax[1,1].set_title('Property Taxes vs. Property Values', fontsize = size2)
ax[1,1].set_xlabel('Property Values($)', fontsize = size1)
ax[1,1].set_ylabel('Taxes($)', fontsize = size1)
ax[1,1].ticklabel_format(useOffset = False, style = 'plain')

### Data Fixing
scatterData = data[['TAXP','VALP','WGTP','MRGP']].dropna()
cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["lightblue","white","pink"])
ax[1,1].set_xlim(0,1200000)

def GetTaxMapping():
    taxData = {}
    taxData[1] = np.NaN
    taxData[2] = 1
    
    #Build the dictionary that updates by $50
    for code in range(3,23):
        taxData[code] = 50 + 50 * (code - 3)
   
    #Build the dicionary that updates by $100 starting from $1000
    for code in range(22,63):
       taxData[code] = 1000 + 100 * (code - 22)
       
    #This is everything else that don't quite convert eassily.
    taxData[63] = 5500
    taxData[64] = 6000
    taxData[65] = 7000
    taxData[66] = 8000
    taxData[67] = 9000
    taxData[68] = 10000
 
    return taxData


taxData = GetTaxMapping()

for y in range(1,69):
    scatterData['TAXP'] = scatterData['TAXP'].replace(to_replace = y, value = taxData[y]) 

### Data Plotting
scatterPlot = ax[1,1].scatter(scatterData.VALP, scatterData.TAXP, marker = 'o', s = scatterData.WGTP/10, c = scatterData.MRGP, cmap = 'seismic', alpha = 0.05)
cb = plt.colorbar(scatterPlot, format = '%li')
cb.set_label(label='First Mortage Payment(Monthly $)', size = size3)





plt.savefig('pums.png', dpi = 100)
plt.show()


