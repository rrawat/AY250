"""
Generic Brushing program
"""


import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.nxutils import points_inside_poly
from matplotlib.colors import colorConverter
from matplotlib.collections import RegularPolyCollection

from matplotlib import figure
from matplotlib.lines import Line2D                        

  
import os
from matplotlib.mlab import csv2rec
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import matplotlib

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pylab


class NewDrawClass:
	#this is the class which is responsible for drawing the subplots, and for coloring invidiual datapoints
	
	def __init__(self, fig, data):
		#only makes a new subplots at the beginning, otherwise just used for drawing stuff
		self.fig = fig
		self.y_axis_name = 'L2 Lexical Knowledge Score'
		self.x_axis_names = ('Participant', 'Musical Ability Score','Age on Arrival','Language Use Score')
		
		xtitles = ('Participant', 'Musical Ability Score','Age on Arrival','Language Use Score')
		ytitles = ('LKS','LKS','LKS','LKS')
		for i in np.arange(4):
			ax=fig.add_subplot(2,2,i+1) 
			ax.scatter(lex[xtitles[i]],lex['L2 Lexical Knowledge Score'])

			ax.set_ylabel(ytitles[i])
			ax.set_xlabel(xtitles[i])
			ax.label = xtitles[i]					#looking for some way to easily distinguish axes objects from each other
		plt.draw()
		
		
		
		
	def draw_data(self, data, color='yellow'):
		"The GOAL OF THIS FUNCTION IS TO COLOR POINTS ON MULTIPLE SUBPLOTS. FOR EXAMPLE, IF YOU PASS IT A REC ARRAY, IT WILL \
		DRAW ALL THE POINTS ON THE APPROPRAITE SUBPLOTS WITH A CERTAIN COLOR. "
		
		for axes_object in self.fig.get_axes():
			self.update_ax(axes_object, data, color)
		plt.draw()
		
	def update_ax(self, axes_object, data , col):
		#ACTUALLY DOES THE WORK OF DRAW_DATA FUNCTION
		xlabel = axes_object.get_xlabel()
		ylabel = 'L2 Lexical Knowledge Score'
		axes_object.scatter(data[xlabel], data[ylabel], color = col)

class Rectangle:
	"this class keeps track of lots of special rectangles and can draw the rectangles and select \
	subsets of data which can be colored in special ways"
	RecList = [ ] 															#LIST OF ALL RECTANGLES, ACTIVE(WILL BE DRAWN), 
																			#AND INACTIVE(POINTS NOT DRAWN)
	def __init__(self,x0, y0, x1, y1, axes, figure, total_data):
		Rectangle.RecList.append(self)
		
		self.axes = axes
		self.x0 = x0
		self.y0 = y0
		self.x1 = x1
		self.y1 = y1
		self.xlabel = axes.get_xlabel()
		self.ylabel = 'L2 Lexical Knowledge Score'
		
		#THE RECTANGLE BOUNDARY, WILL BE DEFINED LATER
		self.polygon = None
		
		#SETTING A RECT TO INACTIVE LEADS TO IT NOT GETTING PLOTTED THROUGH OTHER FUNCTIONS
		self.active = True
		
		#DATA
		self.total_data = total_data
		self.select_points()
		
		#PLOTTING
		self.plotRectangle()
		
		
		
	def select_points(self):
		#SELECTS DATA POINTS THAT FALL WITHIN THE RECTANGLE IN THE SUBPLOT THE USER INDICATES
		color_data = self.selectData(self.x0, self.x1, self.xlabel, self.total_data)
		color_data = self.selectData(self.y0, self.y1, self.ylabel, color_data)
		self.data = color_data
		
	def selectData(self, start, end, attribute, data):
		#WORKER FOR SELECT_POINTS
		data2 = data[data[attribute] > start]
		data2 = data2[data2[attribute] < end]
		return data2
		
	def plotRectangle(self):
		"plots the outline, BUT DOESN'T SHADE IN THE POINTS, THAT IS DONE IN FUNCTIONS OF THE BRUSHING CLASS"
		x0, y0, x1, y1 = self.x0, self.y0, self.x1, self.y1		
		bottomleft, topright  = self.axes.transLimits.transform(((x0,y0),(x1, y1)))
		self.polygon = self.axes.axhspan(y0, y1,xmin=bottomleft[0], xmax=topright[0], facecolor='0.5', fill=False)
		
	def deleteRectangles(self,x,y, axes):
		"IF A USER RIGHT CLICKS(SEE BRUSHING CLASS), THE COORDINATES OF THE CLICK are used to inactivate rectangles"
		for r in Rectangle.RecList:
			if r.axes == axes:
				if (r.x0 < x) and (r.x1 > x):
					if r.y0 <y and r.y1 > y:
						r.polygon.remove()
						r.active = False
		
class NewBrushClass:
	"this class handles user input, it allows user to draw rects and delete them, using left and right clicks (and drags)"
	
	def __init__(self, fig, y, lex, draw_obj):
		self.rectangles = [ ]
		self.lex = lex											#lex is the data, a rec array
		self.draw_obj = draw_obj								# instance of the drawing class, used to update the display of
		 														# points on the plot
		
		
		#Key bindings
		self.fig = fig
		self.cid =	fig.canvas.mpl_connect('button_press_event', self.onclick)
		self.cid2 =	 fig.canvas.mpl_connect('button_release_event', self.offclick)
		self.keycid = fig.canvas.mpl_connect('key_press_event', self.on_key)
			
		#use these variables to preserve state
		self.current_axes_label = None
		self.x0 = None
		self.x1 = None
		self.y0 = None
		self.y1 = None
		self.rects = []

	def reset(self):
		"reset picker state"
		self.current_axes_label = None
		self.x0, self.x1, self.y0, self.y1 = None, None, None, None
		
	def onclick(self, event):
		"IF A USER LEFT CLICKS, THEN THE CODE IS USED TO DRAW A RECTANGLE, A RIGHT CLICK IS USED TO DELETE RECTANGLES"
		if event.xdata == None or event.ydata==None: return
		#Catch middle/right clicks
		if event.button == 2 or event.button == 3:
			self.deleteRect(event)
			return
			
		#Else set x0, and y0
		self.current_axes_label = event.inaxes.label
		self.x0, self.y0 = event.xdata, event.ydata
		
	def deleteRect(self, event):
		"THIS REMOVES A RECTANGLE BY INACTIVATING IT, THEN UPDATING THE DISPLAY. IT'S A LITTLE BUGGY, I'M NOT SURE WHY"
		"sometimes you have to click on a rectagle a few times to remove it, other times clicking in different locations can help"
		
		if len(self.rectangles) > 0:
			self.rectangles[0].deleteRectangles(event.xdata, event.ydata, event.inaxes)
		self.updatePlot()
		
	def offclick(self, event):
		"#only proceed for normal, left clicks: make the rectangle and draw points"
		"sets x1, y1, which are the second set of coordinates for the rectangle"
		if event.xdata == None or event.ydata==None:	return
		if self.current_axes_label != event.inaxes.label: return			#if the person is mousing over a differnt graph
			
			
		self.x1, self.y1, ax = event.xdata, event.ydata, event.inaxes
		
		x0 = min(self.x0, self.x1)
		x1 = max(self.x0, self.x1)
		y0 = min(self.y0, self.y1)
		y1 = max(self.y0, self.y1)
		
		#make a new rectangle
		r = Rectangle(x0, y0, x1, y1, ax, self.fig, total_data = self.lex)
		self.rectangles.append(r)
		
		#update the plot
		self.updatePlot()
		self.reset()
		

	def updatePlot(self):
		#first make all data points yellow
		self.draw_obj.draw_data(self.lex, 'yellow')
		plt.draw()
		#at this point, rectangle polygons(see rectangle.polygon) have been removed from the display
		#because draw() removes them
		#however, if the rectangle has not been removed, it is still a black box
		
		for rect in self.rectangles:
			if rect.active:
				#shade in the corresponding points on all graphs
				#as each rectangle "contains" a set of the data(rectangle.data), it can be shaded in 
				self.draw_obj.draw_data(rect.data, 'red')
		plt.draw()
				
		
	def on_key(self, event):
		"wanted to use key bindings, but somehow they didn't work. ALl of my key clicks ended up showing in the terminal line \
		and didn't cause the print statemnt to appear, instead I used rightclicking for similar functionality of removing rectangles"
		print "ds"
		if event.key == 'd':
			"when the key is pressed, deletes the shown rectangle, then redraws everything"
			print dir(event)




lex = mlab.csv2rec("lexical_score.txt",names=('Participant','L2 Lexical Knowledge Score','Age on Arrival','Length of Residence','Language Use Score','Phonological STM Score','Musical Ability Score'), delimiter=',',skiprows=1)		
figure = plt.figure()
NDC = NewDrawClass(figure, lex)
NDC.draw_data(lex)
x = NewBrushClass(figure,'L2 Lexical Knowledge Score',lex, NDC)

plt.show()