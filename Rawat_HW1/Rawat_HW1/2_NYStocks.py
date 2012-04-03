
"""
Reproduces NY Stock plot (stocks.png) using data from google_data.txt, yahoo_data.txt, and ny_temps.txt (3 line plots on one figure, with two y axes)
"""


from matplotlib.mlab import csv2rec
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import matplotlib
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pylab

  
goog = mlab.csv2rec("google_data.txt",names=('MJD','Value'), delimiter='\t')
yahoo = mlab.csv2rec("yahoo_data.txt",names=('MJD','Value'),skiprows=1, delimiter='\t')
temp = mlab.csv2rec("ny_temps.txt",names=('MJD','High'),skiprows=1, delimiter='\t')
  
f = plt.figure()
ax = f.add_subplot(111)


#2dary axis
ax2 = ax.twinx()   
  
#Data
ax.plot(yahoo['MJD'],yahoo['Value'],'-',color='indigo',lw=2)
ax.plot(goog['MJD'],goog['Value'],'-b',lw=2)
ax2.plot(temp['MJD'],temp['High'],'--r',lw=2)
  
#Title

ax.set_title('New York Temperature, Google, and Yahoo!', fontsize='xx-large',fontname="Times")#,weight='bold')
  
#Axis labels
ax.set_xlabel('Date (MJD)',size='large')
ax.set_ylabel('Value (Dollars)',size='large')
ax2.set_ylabel(r'Temperature ($^{\circ}$F)',size='large')
  
#Axis limits
ax.set_xlim(49000,55600)
ax.set_ylim(-20,775)
ax2.set_ylim((-150,100))


#Minor gridlines
ax.yaxis.set_minor_locator(MultipleLocator(20))
ax.xaxis.set_minor_locator(MultipleLocator(200))
ax2.yaxis.set_minor_locator(MultipleLocator(10))

#legend 
axline = ax.get_lines()			#get lines of plot to use in the legend
ax2line = ax2.get_lines()
legend = ax.legend((axline[0],axline[1],ax2line[0]),('Yahoo! Stock Value','Google Stock Value','NY Mon. High Temp'),loc='center left')

#hide legend box
legendbox = legend.get_frame()
legendbox.set_visible(False)

#set legend text size
for t in legend.get_texts():
    t.set_fontsize('medium')
  
  
plt.show()