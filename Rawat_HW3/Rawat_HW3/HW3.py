import string	
import sys
import os
from PIL import Image
import sklearn
import matplotlib.pyplot as plt
import numpy as np
from skimage import data, io, filter, measure
from scipy import ndimage
from skimage.morphology import is_local_maximum

#define functions for the features
listoffunctions=[ ]


def area(i):
	"""feature 1: takes in opened image (array of pixels) and returns px x px area"""
	#print i
	x,y= i.size
	return [x*y]
listoffunctions.append(area)



def ratio_x_to_y(i):
	"""feature 2: returns x-to-y length ratio"""
	x,y= i.size
	return [float(x)/y]	
listoffunctions.append(ratio_x_to_y)


def percent_rgb(i):
	"""features 3-11: calculates features relating to ratios between the colors: 3-5: % of each color, 6-8: ratios of each color to another 9-11: ratio of light to dark of one color"""
	rgb_features=[]
	
	x = i.histogram()
	red = sum(x[0:255])
	green = sum(x[256:512])
	blue = sum(x[513:768])
	total = sum(x[:])
	
##percent red	
	percent_red=float(red)/total
	rgb_features.append(percent_red)
##percent green
	percent_green=float(green)/total
	rgb_features.append(percent_green)
##percent blue
	percent_blue=float(blue)/total
	rgb_features.append(percent_blue)

##red:green ratio	
	try:rg=float(red)/green
	except:rg=0
	finally:rgb_features.append(rg)
##red:blue ratio
	try:rb=float(red)/blue
	except:rb=0
	finally: rgb_features.append(rb)
##green:blue ratio
	try: gb=float(green)/blue
	except:gb=0
	finally:rgb_features.append(gb)

	#lightness and darkness of reds
	light_r = sum(x[0:128])
	dark_r=sum(x[129:255])
	light_b = sum(x[255:383])
	dark_b=sum(x[384:512])
	light_g = sum(x[513:640])
	dark_g=sum(x[641:768])
#red-light:dark ratio
	try: r_ld_ratio=light_r/float(dark_r)
	except:r_ld_ratio=0
	finally:rgb_features.append(r_ld_ratio)
#blue-light:dark ratio
	try: b_ld_ratio=light_rb/float(dark_rb)
	except:b_ld_ratio=0
	finally:rgb_features.append(b_ld_ratio)
#green-light:dark ratio
	try: g_ld_ratio=light_g/float(dark_g)
	except:g_ld_ratio=0
	finally:rgb_features.append(g_ld_ratio)

	return rgb_features
	
listoffunctions.append(percent_rgb)

def canny_filt_features(i):
	"""features 12-14: using the canny filter"""
	x_size=int(i.size[1]/float(4))
	i=i.resize((x_size,int((i.size[0]/float(i.size[1])*x_size))))
	
	canny_features=[]
	
	x=i.getdata()
	z=np.array(x)
	
	if z.size/(len(z))==1:
		if z.size%3 !=0:
			z= z[0:len(z)-len(z)%3]
		z= z.reshape(-1,3)

###features 12-14: percent of pixels that lie on an edge
	def percent_edges(color_array):
		"""determine fraction of px that lay on an edge for a given array"""
		edges=filter.canny(color_array, sigma=3)	
		total_px= edges.size
		#print total_px			
		edge_px=0	
		for i in edges:
			for a in i:
				if a == True:
					edge_px=edge_px+1
		#print 'edge_px=' , edge_px
		percent_edges=edge_px/float(total_px)
		return percent_edges
#feature 12: percent of red pixels that lie on edges
	try:		
		r_1d=z[:,0]
		r_array = r_1d.reshape(i.size)
		percent_edges_r=percent_edges(r_array)
	except: percent_edges_r=0
	finally: canny_features.append(percent_edges_r)
#feature 13: percent of green pixels that lie on edges
	try:		
		g_1d=z[:,1]
		g_array = g_1d.reshape(i.size)
		percent_edges_g=percent_edges(g_array)
	except: percent_edges_g=0
	finally: canny_features.append(percent_edges_g)
#feature 14: percent of blue pixels that lie on edges
	try:		
		b_1d=z[:,2]
		b_array = b_1d.reshape(i.size)
		percent_edges_b=percent_edges(b_array)
	except: percent_edges_b=0
	finally: canny_features.append(percent_edges_g)

#		if percent_edges_r>0:
#			edge_b_to_r = percent_edges_b/float(percent_edges_r)
			#canny_features.append(edge_b_to_r)

	return canny_features

listoffunctions.append(canny_filt_features)



def color_clump_features(i):
	"""features 15-18: calculates overlay ratio of r,g,b channels in each quadrant of the image"""
	cc_features=[]

	x_size=int(i.size[1]/float(5))
	i=i.resize((x_size,int((i.size[0]/float(i.size[1])*x_size))))
		
	x=i.getdata()
	z=np.array(x)
	if z.size/(len(z))==1:
		if z.size%3 !=0:
			z= z[0:len(z)-len(z)%3]
		z= z.reshape(-1,3)
		
##features 15-18: ratio of colors in each quadrant
	def quadrant_color(color_array1, color_array2, quadrant):
		"""determine ratio of color1 to color 2 in a given quadrant"""
		#define bounds
		if quadrant==1:
			xmin=0; xmax=int(i.size[1]/float(2))
			ymin=0; ymax=int(i.size[0]/float(2))
		elif quadrant==2:
			xmin=int(i.size[1]/float(2)); xmax=i.size[1]
			ymin=0; ymax=int(i.size[0]/float(2))
		elif quadrant==3:
			xmin=0; xmax=int(i.size[1]/float(2))
			ymin=int(i.size[0]/float(2))
			ymax=i.size[0]
		elif quadrant==4:
			xmin=int(i.size[1]/float(2))
			xmax=i.size[1]
			ymin=int(i.size[0]/float(2)) 
			ymax=i.size[0]
		
		
		color1_sum=0
		color2_sum=0

		for a in range(ymin,ymax):
			color1_sum=color1_sum+sum(color_array1[a,xmin:xmax])
		
		for a in range(ymin,ymax):
			color2_sum=color2_sum+sum(color_array2[a,xmin:xmax])

		if color2_sum ==0:
			return 0
		else: return color1_sum/float(color2_sum)
	try:		
		r_1d=z[:,0]
		r_array = r_1d.reshape(i.size)
		g_1d=z[:,1]
		g_array = g_1d.reshape(i.size)
		b_1d=z[:,2]
		b_array = b_1d.reshape(i.size)

		#compute for all color combos in all quadrants	
		quad_value1=float(quadrant_color(r_array, g_array, 1))
		quad_value2=float(quadrant_color(r_array, g_array, 2))
		quad_value3=float(quadrant_color(r_array, g_array, 3))
		quad_value4=float(quadrant_color(r_array, g_array, 4))
		quad_value5=float(quadrant_color(r_array, b_array, 1))
		quad_value6=float(quadrant_color(r_array, b_array, 2))
		quad_value7=float(quadrant_color(r_array, b_array, 3))
		quad_value8=float(quadrant_color(r_array, b_array, 4))
		quad_value9=float(quadrant_color(b_array, g_array, 1))
		quad_value10=float(quadrant_color(b_array, g_array, 2))
		quad_value11=float(quadrant_color(b_array, g_array, 3))
		quad_value12=float(quadrant_color(b_array, g_array, 4))
	except:
		quad_value1, quad_value2, quad_value3, quad_value4, quad_value5, quad_value6, quad_value7, quad_value8, quad_value9, quad_value10, quad_value11, quad_value12 =[0]*12
	finally:
		pass
		cc_features.append(quad_value1)
		cc_features.append(quad_value2)		
		cc_features.append(quad_value3)
		cc_features.append(quad_value4)
	return cc_features

listoffunctions.append(color_clump_features)



def contour_features(im):
	"""features 19- 24; contours of the image: number of contours in the image, mean of distance to background, and local maxima:pixel ratio"""

	contours=[]

	x_size=int(im.size[1]/float(10))
	i=im.resize((x_size,int((im.size[0]/float(im.size[1])*x_size))))
		
	x=i.getdata()
	z=np.array(x)
	if z.size/(len(z))==1:
		if z.size%3 !=0:
			z= z[0:len(z)-len(z)%3]
		z= z.reshape(-1,3)

		#print z.resize(z.size/float(3),3)
		#print z
	#contour mapping	
	contour_array=measure.find_contours(z,0.5)
	len_contours=contours.__len__()
	
	contours.append(len_contours)

# 19-21: distance features: use ndimage.distance to compute "distance" to background of each pixel. Then find mean among x, y, and z values (r,g,b) 
	
	distance=ndimage.distance_transform_edt(z)
	yvaluemean= sum(distance[:,0])/len(distance[:,0])
	xvaluemean= sum(distance[:,1])/len(distance[:,1])
	zvaluemean= sum(distance[:,2])/len(distance[:,2])
					

	contours.append(yvaluemean)
	contours.append(xvaluemean)
	contours.append(zvaluemean)

#22-24: local_max features: find number of local maxima among x,y,z values (rgb) compared to the number of pixels
	
	local_max=is_local_maximum(distance,z,np.ones((3,3)))	
	xmaxsum, ymaxsum, zmaxsum = [0,0,0]
	for a in (local_max[:,0]):
		if a ==False:
			xmaxsum+=1
	contours.append(xmaxsum/float(len(local_max[:,0])))
	for a in (local_max[:,1]):
		if a ==False:
			ymaxsum+=1
	contours.append(ymaxsum/float(len(local_max[:,0])))
	for a in (local_max[:,2]):
		if a ==False:
			zmaxsum+=1
	contours.append(zmaxsum/float(len(local_max[:,0])))

###25: object count
	filt_img=ndimage.gaussian_filter(z,10)
	T=70
	labeled,nr_objects=ndimage.label(filt_img>T)
	contours.append(nr_objects)

	return contours

listoffunctions.append(contour_features)


#------end of feature functions



#######Training


path = "/media/7054-87BA/Python/train"  #This is the path to the folder containing training images. I'm assuming there are only images in there.

#get list of files in training folder
files=[]
for f in os.listdir(path):
	fpath = os.path.join(path, f)
	files.append(fpath)


def getfeaturelist(imgFilePath, listoffunctions):
	"""takes in a file path for the image and the list of feature functions, opens the image, performs the feature functions, appends the values of the features to an array, and closes the function. Returns the list of feature values"""
	imgfeatures=[]
	i = Image.open(imgFilePath) 
	#print listoffunctions
	for feature_funct in listoffunctions:
		imgfeatures = imgfeatures + feature_funct(i)
	
	return imgfeatures

def classtonum(imgclass, imagesubjectlist):
	'''takes in string for the image class, returns numerical class value'''
	imgclassnum=imagesubjectlist.index(imgclass)
	return imgclassnum
	
def numbertoclass(classnum, imagesubjectlist):
	'''takes in numerical class value, returns string for image class'''
	return imagesubjectlist[classnum]
	


# list of all categories
imagesubjectlist=['airplanes', 'bat', 'bear', 'blimp', 'camel', 'comet', 'conch', 'cormorant', 'crab', 'dog', 'dolphin', 'duck', 'elephant','elk', 'frog', 'galaxy', 'giraffe', 'goat', 'goldfish', 'goose', 'gorilla', 'helicopter', 'horse', 'hot-air-balloon', 'hummingbird', 'iguana', 'kangaroo', 'killer-whale','leopards', 'llama', 'mars', 'mussels', 'octopus', 'ostrich', 'owl', 'penguin', 'porcupine', 'raccoon', 'saturn', 'skunk', 'snail', 'snake', 'speed-boat', 'starfish', 'swan', 'teddy-bear', 'toad', 'triceratops', 'unicorn', 'zebra']
		

	
#----input for random forest ---
Y=[] #list of numerical classes
X=[] #list of feature value lists

#for each image in training folder, append class to new list, do the functions, and get training img data
trainingpaths=[]
trainingclasses=[]
for imgfile in files:
	x =str(imgfile)
	if list(x).count('.')<2:
		trainingpaths.append(x)
		classstr=(x.split("_")[-2]).split("/")[-1]
		trainingclasses.append(classstr)
		Y.append(classtonum(classstr, imagesubjectlist))
		X.append(getfeaturelist(imgfile,listoffunctions))


#Random forest

from sklearn.ensemble import RandomForestClassifier 

clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(X, Y)


####Classification

#get path to folder from the command line input

n_list=sys.argv
classifypath=str(n_list[1])

#get list of files in classify folder
classifyfiles=[]
for f in os.listdir(classifypath):
	fname = os.path.join(classifypath, f)
	classifyfiles.append(fname)


# get feature list for each image
classifyX=[]
classification_paths=[]
classification_classes=[]


for imgfile in classifyfiles:
	imgfeatures=[]
	x =str(imgfile)
	
	if list(x).count('.')<2:
		classification_paths.append(x.split("/")[-1])
		
		classification_classstr=(x.split("_")[-2]).split("/")[-1]
		classification_classes.append(classification_classstr)
		classifyX.append(getfeaturelist(imgfile,listoffunctions))

#get classes in an array
predictedclassarray= clf.predict(classifyX) 

predclassstr=[]

#convert back to string values of classes
for classnum in predictedclassarray:
	predclassstr.append(numbertoclass(classnum,imagesubjectlist))

#for the output table
print 'real class'.center(25), '\t', 'predicted class'.center(25), '\n',

#determine accuracy and %improvement from random
correct_matches=0
total_matches=len(predclassstr)


for i in range(0,len(predclassstr)):
	print classification_paths[i].center(25),'\t', predclassstr[i].center(25)
	if classification_classes[i]==predclassstr[i]:
		correct_matches+=1


accuracy=float(correct_matches)/total_matches
percent=100*accuracy/(1.0/(50*len(predclassstr)))

print 'accuracy =', accuracy*100,"%." , percent, "% better than guessing"

print '\a'
