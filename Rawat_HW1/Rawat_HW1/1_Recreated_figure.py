
"""
Reproduces LexScoreimg.jpg using data from lexical_score.txt

"""


from matplotlib.mlab import csv2rec
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import matplotlib
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from pylab import *


lex = mlab.csv2rec("lexical_score.txt",names=('Participant','L2 Lexical Knowledge Score','Age on Arrival','Length of Residence','Language Use Score','Phonological STM Score','Musical Ability Score'), delimiter=',',skiprows=1)

  



f = plt.figure()
ax = f.add_subplot(111)

#add trendline
x=lex['Musical Ability Score']

m,b = polyfit(x,lex['L2 Lexical Knowledge Score'], 1)

ax.plot(x,m*x+b,c='0')

#remove ticks
ax.xaxis.tick_bottom()
ax.yaxis.tick_left()

# add scatterplot
ax.scatter(lex['Musical Ability Score'],lex['L2 Lexical Knowledge Score'],marker='o', c='0')

  
#add axis labels
ax.set_xlabel('Musical Ability Score',size='large')
ax.set_ylabel('L2 Lexical Knowledge Score',size='large')


#set limits
ax.set_xlim(4,20)
ax.set_ylim(5,35)

#note r^2 value
ax.annotate('$r^2 = 0.569$',(16,22))

#remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

  
plt.show()