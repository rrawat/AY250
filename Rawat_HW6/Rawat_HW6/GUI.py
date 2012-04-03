
import urllib
from bs4 import BeautifulSoup
import urllib2
from Tkinter import *
from PIL import Image as Image
from PIL import ImageTk as ImgTk
from PIL import ImageOps
import tkMessageBox



#-------------------- transformations

class Transform:
	"""performs all transformations necessary on PIL objects"""
	def __init__(self, PILobj):

		self.size=PILobj.size
		self.PIL=PILobj
		
	def PIL2TK(self):
		"""turn a PIL into a Tkinter image"""
		return ImgTk.PhotoImage(self.PIL)

	def resize(self, height,width):
		"""resize an image to fit within the given height and width dimensions"""
		y0=self.size[0]
		x0=self.size[1]
		h=height
		w=width
		
		y2=h
		x2=float(h)*x0/y0	
		
		if x2>w:
			x2=w
			y2=float(w)*y0/x0
			
		resizedPIL=self.PIL.resize((int(y2), int(x2)))
		return resizedPIL
		
	def rotate90(self):
		"""rotate the image 90 degrees clockwise"""
		return self.PIL.rotate(90)
		
	def flipRtoL(self):
		"""flip the image horizontally"""
		return self.PIL.transpose(Image.FLIP_LEFT_RIGHT)
		
	def invert(self):
		"""invert the colors of the image"""
		return ImageOps.invert(self.PIL)
		
#----------------Search functionality

class Search_url:
	"""take in the user query, search for the image, and save it to the directory"""
	def __init__(self, entry_string):
		self.querystr=entry_string.replace(" ", "+")
		
		#construct search query url
		self.url='https://www.google.com/search?tbm=isch&q=%s'%(self.querystr)
		
		#get img url
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		response = opener.open(self.url)
		self.html = response.read()
		response.close()
		self.soup = BeautifulSoup(self.html)
		self.soup.findAll('img')
		self.imgs=self.soup.findAll('img')
		self.img=str(self.imgs[1])
		self.src=self.img.split("src=")[1]
		self.imgurl=self.src.split('"')[1]
		
		#set file name for downloaded image
		self.filename="%s.gif" %self.querystr
		
	def download_img(self):
		"""download the image, save to directory"""
		imgurl=self.imgurl
		image=urllib.URLopener()
		image.retrieve(imgurl, self.filename)



#---------------make a root window
root = Tk() ; root.title("HW6: Google Image Search & 3 Transformations")


#---------------make the image window
imgWindow=Label(root,relief=SUNKEN)
imgWindow.grid(row=2, columnspan=3, rowspan=3)



#----------PUT IN THE SEARCH BAR

def displayText():
	""" Display the Entry text value. """

	global entryWidget, imgWindow, PILobject

	if entryWidget.get().strip() == "":
		#error message
		tkMessageBox.showerror("Search Bar: entry error", "Enter a text query for the image search")
	
	else: 
		button.configure(state=DISABLED)
		button.update_idletasks()	
		
		#get img url from Search_url class
		print "entry string = ", entryWidget.get().strip()
		string=entryWidget.get().strip()
		imgurl=Search_url(string).imgurl
		disp_url.set(imgurl)
						
		#download img
		Search_url(string).download_img()
		
		#update the image
		path2=Search_url(string).filename
		PILobject=Image.open(path2)
			#resize image
		ResizedPIL=Transform(PILobject).resize(200,300)
			#convert to Tkimage
		img2 = Transform(ResizedPIL).PIL2TK() #ImgTk.PhotoImage(PILobject)
			#save image to label attributes for storage
		imgWindow.configure(image = img2)
		imgWindow.image = img2
		
		#reset button to normal (responsive)
		button.configure(state=NORMAL)
		
		#update display
		root.update()
			
		

root["padx"] = 40
root["pady"] = 20	   

# Create a text frame to hold the text Label and the Entry widget
textFrame = Frame(root)
textFrame.grid(row=0, sticky=W)

#Create a Label in textFrame
entryLabel = Label(textFrame)
entryLabel["text"] = "Enter an image query:"
entryLabel.pack(side=LEFT)

# Create an Entry Widget in textFrame
entryWidget = Entry(textFrame)
entryWidget["width"] = 50
entryWidget.pack(side=LEFT)


#create search button
button = Button(textFrame, text="Search", command=displayText)
button.pack(side=RIGHT) 

#-----------------URL field

disp_url = StringVar()
#disp_url = the text displayed in the url field

def report_url(*args):
	#displayed in interpreter when the image changes
	print "URL:", disp_url.get(), "\n"
	
disp_url.set("Image URL") ;
disp_url.trace("w",report_url)

url_field  = Message(root,width=400,justify=LEFT,textvariable=disp_url,relief=SUNKEN)
url_field.grid(row=1, columnspan=2)



#-------------------- action buttons

def rotation():
	"""changes the active image to the rotated version of the current one"""
	global action_1, PILobject
	
	action_1.configure(state=DISABLED)
	action_1.update_idletasks()	
	
	#update the image
	rotatedPIL=Transform(PILobject).rotate90()
	ResizedPIL=Transform(rotatedPIL).resize(200,300)	
	img2 = Transform(ResizedPIL).PIL2TK()
	
	#img2 = Transform(invertedPIL).PIL2TK() #ImgTk.PhotoImage(PILobject)
	imgWindow.configure(image = img2)
	imgWindow.image = img2
	
	#set new base image to new img
	PILobject=ResizedPIL
		
	#reset button to normal (responsive)
	action_1.configure(state=NORMAL)
	
	#update display
	root.update()
	
def inversion():
	"""changes the active image to an inversion of the current one."""
	global action_2, PILobject
	
	action_2.configure(state=DISABLED)
	action_2.update_idletasks()	
	
	#update the image
	invertedPIL=Transform(PILobject).invert()
	ResizedPIL=Transform(invertedPIL).resize(200,300)	
	img2 = Transform(ResizedPIL).PIL2TK()
	
	#img2 = Transform(invertedPIL).PIL2TK() #ImgTk.PhotoImage(PILobject)
	imgWindow.configure(image = img2)
	imgWindow.image = img2
	
	#set new base image to new img
	PILobject=ResizedPIL
		
	#reset button to normal (responsive)
	action_2.configure(state=NORMAL)
	
	#update display
	root.update()
		
def flipping():
	"""changes the active image to a flipped version of the current one"""

	global action_3, PILobject
	
	action_3.configure(state=DISABLED)
	action_3.update_idletasks()	
	
	#update the image
	flippedPIL=Transform(PILobject).flipRtoL()
	ResizedPIL=Transform(flippedPIL).resize(200,300)
	img2 = Transform(ResizedPIL).PIL2TK()
	
	#img2 = Transform(invertedPIL).PIL2TK() #ImgTk.PhotoImage(PILobject)
	imgWindow.configure(image = img2)
	imgWindow.image = img2
	
	#set new base image to new img
	PILobject=ResizedPIL
	
	#reset button to normal (responsive)
	action_3.configure(state=NORMAL)
	
	#update display
	root.update()
		
#create action buttons
action_1=Button(root, text='Rotate', command=rotation)
action_1.grid(row=2, column=1)
action_2=Button(root,text='Invert', command=inversion)
action_2.grid(row=3, column=1)
action_3=Button(root, text='Flip', command=flipping)
action_3.grid(row=4, column=1)


root.mainloop()

