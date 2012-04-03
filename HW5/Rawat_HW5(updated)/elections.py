import sqlite3 #http://docs.python.org/library/sqlite3.html
import matplotlib
#import pyplot
import numpy
from scipy import stats
from bs4 import BeautifulSoup
import urllib2
from PIL import Image
import os
from urllib import urlretrieve
import numpy as np
import csv

import datetime
from matplotlib.dates import date2num

from bs4 import BeautifulSoup
import urllib2

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import matplotlib
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pylab




#create database

connection=sqlite3.connect('/candidates.db')
cursor=connection.cursor()



#a) create "Races" table, and populate it with the race's name, election date, and data url


	
cursor.execute("""CREATE TABLE race_db (id INTEGER PRIMARY KEY AUTOINCREMENT, race_id TEXT, election_date DATE, data_url TEXT)""")


race_data = [ ("RepVP", "08/27/12", "http://www.intrade.com/v4/markets/?eventId=90482"), ("RepNom", "08/27/12","http://www.intrade.com/v4/markets/?eventId=84328"), ("PresElect", "01/20/13", "http://www.intrade.com/v4/markets/?eventId=84326")] 

for race in race_data: 
	sql_cmd = ("INSERT INTO race_db (race_id, election_date, "+" data_url) VALUES " +str(race)) 			
	cursor.execute(sql_cmd)
	connection.commit()




###############################################################

#b) download prediction data for 3 races for all named condidates. (Repub pres nominee, pres election, repub vp nominee) #already done: provided. So, just access the path. /race_prediction_data folder, and formatted as Fistname_Lastname_Race.csv. Race= RepNom, RepVPNom, PresElect

###############################################################
#c) create "Candidates" table and populate it automatically with biographical data from wikipedia using BeautifulSoup to parse. Include home town, home state, party affiliation, birth date, and a link to a local file containing a photo of the candidate




def unique_ify(seq):
	contained = set()
	contained_add = contained.add
	return [ x for x in seq if x not in contained and not contained_add(x)]




path="race_prediction_data/"
files=[]
for f in os.listdir(path):
	fpath = os.path.join(path, f)
	files.append(fpath)

#create list of candidates
candidate_list=[]
for candidate_file in files:
	if "DS_Store" in str(candidate_file):
		files.remove(candidate_file)
	else:
		full_name_list= (str(candidate_file).split("/")[1]).split("_")[:-1]
		if "Jr" in full_name_list:
			full_name_list.remove("Jr")
		
		#convert to full name to ensure no duplicates
		a=""
		for name_part in full_name_list:
			a+=name_part + "_"
		cand_name= a[:-1]
		candidate_list.append(cand_name)
candidate_list= unique_ify(candidate_list)

#create class to store candidate info

class Candidate:
	def __init__(self,full_name_string):

		self.first=full_name_string.split("_")[0]
		if self.first=="Lindsay":
			self.first="Lindsey"
		
		self.last=full_name_string.split("_")[-1]
		if self.first=='Barack':
			self.url='http://en.wikipedia.org/wiki/Obama'
		else:
			self.url='http://en.wikipedia.org/wiki/%s_%s'%(self.first,self.last)
		
		self.md="undef"
		self.town='undef'
		self.state='undef'
		

		self.soup=Candidate.get_soup(self)	
		#retrieve info from wikipedia
		Candidate.get_img(self)
		Candidate.get_birthdate(self)
		Candidate.get_location(self)
		Candidate.get_party(self)
		
		#print self.first, self.last, self.town, self.state, self.birthdate, self.party
	
	
	#begin giant list of parsing functions
	def get_soup(self):
		"""gets BeautifulSoup object of html"""
		url=self.url
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		response = opener.open(url)
		html = response.read()
		response.close()
		soup = BeautifulSoup(html)

	def get_img(self):
		"""gets img url"""
		soup=self.soup
		
		imgs=soup.findAll(attrs={"width" : "220"})
		img=str(imgs)
		if "src" in img:
			path= img.split('src="')[1].split('"')[0]
			img_url="http:"+path
			return img_url
		else:
			return "http:"+'//upload.wikimedia.org/wikipedia/en/b/bc/Wiki.png'
	
	def get_birthdate(self):
		"""parses wikipedia for birthdate"""
		if self.first in ["Hillary"]:
			if self.last in ["Clinton"]:
				 self.birthdate='1947-10-26'
				 return
		if self.last=="Biden":
			self.birthdate='1942-11-20'
			return
		if self.last=="Bolton":
			self.birthdate='1948-11-20'
			return
		if self.last=="Huntsman":
			self.birthdate='1960-03-26'
			return
		if self.last=="Dobbs":
			self.birthdate="September 24, 1945"
			return
		
		soup=self.soup
		bday_class=soup.find("span", {"class":"bday"})
		try: birthdate= str(bday_class).split(">")[1].split("<")[0]	
		except:	
			url='http://en.wikipedia.org/wiki/%s_%s_(politician)'%(self.first,self.last)
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			response = opener.open(url)
			html = response.read()
			response.close()
			soup = BeautifulSoup(html)
			bday_class=soup.find("span", {"class":"bday"})
			birthdate= str(bday_class).split(">")[1].split("<")[0]	
		finally:
			self.birthdate= birthdate
		
	def get_location(self):
		"""gets birth town and state (location) from wikipedia"""
		if self.first in ["Hillary"]:
			if self.last in ["Clinton"]:
				 self.town='Chicago'
				 self.state="Illinois"
				 return
				 
		if self.last=="Biden":
			self.town='Scranton'
			self.state='Pennsylvania'
			return
		if self.last=="Bolton":
			self.town="Baltimore"
			self.state="Maryland"
			return
		if self.last=="Huntsman":
			self.town="Redwood City"
			self.state="California"
			return
		if self.last=="Dobbs":
			self.town="Childress County"
			self.state="Texas"
			return
		if self.last=="Bloomberg":
			self.town="Boston"
			self.state="Massachusetts"
			return
		if self.last=="McChrystal":
			self.town="Fort Leavenworth"
			self.state="Kansas"
			return
		try:
			soup=self.soup
			items=soup.findAll("td")
			for n in range(len(items)):
				item=str(items[n])
				if 'class="bday"' in item:
					links= item.split("<a href=")
					for n in range(len(links)):
						link=str(links[n])
						if "title" in link:
							string=str(link).split(">")[1]
							if "," in string:
								town= string.split("<")[0].split(", ")[0]
								
								state=string.split("<")[0].split(", ")[1]
							else:
								if self.town=='undef':
									town=string.split("<")[0]
									state=link.split(">")[2].split(", ")[1]
					 			else: pass
					 			
			self.town=town
			self.state=state


		except:
			try:
				soup=self.soup
				items=soup.findAll("td")
				for n in range(len(items)):
					
					item=str(items[n])
					
					if 'class="bday"' in item:
					
						breaks= item.split("<br/>")
						
						for n in range(len(breaks)):
							link=str(breaks[n])
							if "title" in link:
								string=str(link).split(">")[1]
								if "," in string:
									town= string.split("<")[0].split(", ")[0]
									
									state=string.split("<")[0].split(", ")[1]
								else:

									if self.town=='undef':
										town=string.split("<")[0]
										if "=" in town:
											town=town.split("=")[-1]
										state=link.split(">")[2].split(", ")[1]
										if "=" in state:
											state=state.split("=")[-1]
						 			else: pass
						 			
				self.town=town
				self.state=state
			
			except:
				try: 
					soup=self.soup
					items=soup.findAll("td")
					for n in range(len(items)):
					
						item=str(items[n])
						if 'class="bday"' in item:
					
							links= item.split("<a href=")
					
							link=str(links[1])

							if "title" in link:
					
								string=str(link).split(">")[1]
					
								town= string.split("<")[0]								
								state=links[2].split(">")[1].split("<")[0]
					
					self.town=town
					self.state=state			 			


				except:
					
					try:
						soup=self.soup
						items=soup.findAll("td")
						for n in range(len(items)):
						
							item=str(items[n])
							if 'class="bday"' in item:
								links= item.split("<a href=")
								link=str(links[1])
								#print link, "\n \n"
								if "title" in link:
									string=str(link).split(">")[1]
									town= string.split("<")[0]	
									state=link.split("</a>")[1].split(",")[1]
								else:
									pass
						self.town=town
						self.state=state	
		 			
					except:
						try:
							items=soup.findAll("td")
							for n in range(len(items)):
							
								item=str(items[n])
							
								if 'class="bday"' in item:
									breaks= item.split("<br/>")
									break1=str(breaks[1])
									town= break1.split("</td>")[0]
									state=town
							self.town=town
							self.state=state
						except:
							url='http://en.wikipedia.org/wiki/%s_%s_(politician)'%(self.first,self.last)
							opener = urllib2.build_opener()
							opener.addheaders = [('User-agent', 'Mozilla/5.0')]
							response = opener.open(url)
							html = response.read()
							response.close()
							soup = BeautifulSoup(html)
							
							
							items=soup.findAll("td")
							for n in range(len(items)):
		
								item=str(items[n])
								if 'class="bday"' in item:
					
									links= item.split("<a href=")
			
									for n in range(len(links)):
										link=str(links[n])
										
										if "title" in link:
							
											string=str(link).split(">")[1]
											if "," in string:
												town= string.split("<")[0].split(", ")[0]
												
												state=string.split("<")[0].split(", ")[1]
											else:
												if self.town=='undef':
													try:
					
														town=string.split("<")[0]
														state=link.split(">")[2].split(", ")[1]
													except:
														if '<br/>' in link:
			
															new_str= link.split("<br/>")[1].split(">")[1]
															town= new_str.split(", ")[0]
															state= new_str.split(", ")[1].split("<")[0]
															
									 				finally: pass
			#						 				
									 			else: pass			
							self.town=town
							self.state=state
						finally: pass
					finally: pass
				finally: pass			
			finally: pass
		finally: pass
		
		
	def get_party(self):
		"""assign the candidate's party from the wikipedia page"""
		if self.first in ['Clarence', 'David', "John", "Jon", "Lou", "Stanley"]:
			if self.last in ['Thomas', 'Petraeus', "Bolton","Dobbs", "Huntsman", "McChrystal"]:
				self.party='Republican'
				return
		if self.first in ["Hillary", "Joe"]:
			if self.last in ["Clinton", "Biden"]:
				 self.party='Democratic'
				 return
		try:
			soup=self.soup
			items=soup.findAll("tr")
			for n in range(len(items)):
				item=str(items[n])
				if "Political party" in item:
					parties=['Republican', 'Democratic', 'Independent', 'Independant', 'Tea', 'Reform']
					ind_list=[]
					for party in parties:
						if party in item:
							ind_list.append(item.index(party))
					party= parties[ind_list.index(min(ind_list))]
					
			self.party= party	
		except:
			url='http://en.wikipedia.org/wiki/%s_%s_(politician)'%(self.first,self.last)
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			response = opener.open(url)
			html = response.read()
			response.close()
			soup = BeautifulSoup(html)
				
			items=soup.findAll("tr")
			for n in range(len(items)):
				item=str(items[n])
				if "Political party" in item:
					parties=['Republican', 'Democratic', 'Independent', 'Independant', 'Tea', 'Reform']
					ind_list=[]
					for party in parties:
						if party in item:
							ind_list.append(item.index(party))
					party= parties[ind_list.index(min(ind_list))]
			self.party= party	
		finally:
			pass
			
		
	
#organize data for database table, and while iterating through candidates, assign to north, south, and republican lists for use in parts e and f
cand_db_data=[]
md=39.722201	
north=[]
south=[]
repubs=[]
for candidate in candidate_list:
	instance=Candidate(candidate)
	entry_for_db=(instance.first, instance.last, instance.birthdate, instance.party, instance.town, instance.state, instance.get_img())
	cand_db_data.append(entry_for_db)
	#extract repub candidates
	if instance.party=='Republican':
		repubs.append(instance.last)
		
	replace=[" ","\n","<br"]
	for char in replace:
		if char in instance.town:
			instance.town=str(instance.town).replace(char, "_")	
		if char in instance.state:
			instance.state=str(instance.state).replace(char, "_")
	url= 'http://where.yahooapis.com/geocode?q=%s,+%s'%(instance.town,instance.state)
	response = urllib2.urlopen(url) # open the url as before
	html = response.read()
	response.close()
	soup = BeautifulSoup(html)
	lat_tag = soup.findAll("latitude")
	lat=str(lat_tag).split(">")[1].split("<")[0]
	
	#mark north/south in candidate attributes, and extract
	if float(lat)> md:
		instance.md = "N"
		north.append(instance)
	else:
		instance.md ="S"
		south.append(instance)

#organize north and south candidates

north_names=[]
south_names=[]
	
for s in south:
	south_names.append(s.last)
for n in north:
	north_names.append(n.last)




#initiate sqlite3
connection=sqlite3.connect('/candidates.db')
cursor=connection.cursor()

#create table
sql_cmd="""CREATE TABLE candidates_db (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, birth DATE, party TEXT, town TEXT, state TEXT, photo IMAGE) """
cursor.execute(sql_cmd)

#populate table
for candidate in cand_db_data:
	sql_cmd = ("INSERT INTO candidates_db (first_name, last_name, birth, party, town, state, "+" photo) VALUES " +str(candidate)) 			
	cursor.execute(sql_cmd)
	connection.commit()




#d) Create a database table called ?predictions? and populate it with the 
#prediction data (from b).  You should include date, price, and volume. For each 
#row of prediction entry, create a row in the table with two additional foreign 
#key columns indicating to which candidate and race the prediction data is 
#related.



conn = sqlite3.connect("/candidates.db")
curs = conn.cursor()

curs.execute("CREATE TABLE predictions (col1 TEXT, col2 FLOAT, col3 FLOAT, candidate_last TEXT, race TEXT, FOREIGN KEY (race) REFERENCES race_db(race_id),  FOREIGN KEY(candidate_last) REFERENCES candidate (last_name));")

path="race_prediction_data/"
files=[]
for f in os.listdir(path):
	fpath = os.path.join(path, f)
	files.append(fpath)

for filename in files:
	if "DS_Store" in str(filename):
		files.remove(filename)

	else:
		with open(filename,'rb') as infile:
			# csv.DictReader uses first line in file for column headings by default
			dr = csv.DictReader(infile, delimiter=',')
			cand_name=(str(filename).split(".")[-2]).split("_")[-2]
		
			race=(str(filename).split(".")[-2]).split("_")[-1]
				
			to_db = [(i['Date'], i['Close'], i['Volume'], cand_name, race) for i in dr]
		
		
		curs.executemany("INSERT INTO predictions (col1, col2, col3, candidate_last, race) VALUES (?, ?, ?, ?,?);", to_db)
		conn.commit()


	
#e) Use your database to plot as a function of time the probability of a 
#candidate with home state north or south of the Mason-Dixon Line winning 
#each race.

#
	
#create plot

f = plt.figure()

ax = f.add_subplot(111)

race_list=['RepVPNom', 'RepNom', 'PresElect']
for race1 in race_list:

	race1_dates_n=[]
	race1_data_n=[]
	race1_dates_s=[]
	race1_data_s=[]
	
	cursor.execute('select * from predictions')
	for row in cursor:
		for s in south_names:
			if s in row:
				if race1 in row:
					race1_dates_s.append(row[0])
					race1_data_s.append(row[1])
	
		for n in north_names:
			if n in row:
				if race1 in row:
					race1_dates_n.append(row[0])
					race1_data_n.append(row[1])
		
	months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	num_MM=['01','02','03','04','05','06','07','08','09','10','11','12']
	
	#for north candidates
	race1_d_n=[]
	
	for a in race1_dates_n:
		for m in months:
			if m in a:
				b=a.split("'")[0]
				MM=num_MM[months.index(str(b).split(" ")[0])]
				D=str(b).split(" ")[1].split(",")[0]
				if len(D)==1:
					DD="0%s"%D
				else:
					DD=D
				YYYY=str(b).split(" ")[2]
				b=date2num(datetime.datetime(int(YYYY),int(MM),int(DD)))
				race1_d_n.append(b)
				#print b
	
	#unique_ify the dates
	race1_dates_u_n=unique_ify(race1_d_n)
	#find all with same date, append corresp data to new list
	race1_data_u_n=[]
	for date in race1_dates_u_n:
		indexes=[i for i, y in enumerate(race1_dates_u_n) if y==date]
		sumdata=0
		for a in indexes:
			sumdata=sumdata+race1_data_n[a]
		race1_data_u_n.append(sumdata/float(100))
	
	
	
	color=['r', 'c', 'b']
	scattercolor=color[race_list.index(race1)]
	ax.scatter(race1_dates_u_n,race1_data_u_n, s=20, c=scattercolor, marker='_', edgecolors=scattercolor)
	
	
	#for south candidates
	race1_d_s=[]
	
	for a in race1_dates_s:
		for m in months:
			if m in a:
				b=a.split("'")[0]
				MM=num_MM[months.index(str(b).split(" ")[0])]
				D=str(b).split(" ")[1].split(",")[0]
				if len(D)==1:
					DD="0%s"%D
				else:
					DD=D
				YYYY=str(b).split(" ")[2]
				b=date2num(datetime.datetime(int(YYYY),int(MM),int(DD)))
				race1_d_s.append(b)
				#print b
	
	#unique_ify the dates
	race1_dates_u_s=unique_ify(race1_d_s)
	#find all with same date, append corresp data to new list
	race1_data_u_s=[]
	for date in race1_dates_u_s:
		indexes=[i for i, y in enumerate(race1_dates_u_s) if y==date]
		sumdata=0
		for a in indexes:
			sumdata=sumdata+race1_data_s[a]
		race1_data_u_s.append(sumdata/float(100))
	
	

	color=['r', 'c', 'b']
	scattercolor=color[race_list.index(race1)]

	ax.plot(race1_dates_u_s,race1_data_u_s,c=scattercolor, lw=0, marker='^')
	



##############obama : obama and repub lines overlap a lot, so I've made the obama line very wide so it can still be seen.

obama_prob=[]
race1 = race_list[2]

race1_dates_n=[]
race1_data_n=[]


cursor.execute('select * from predictions')
for row in cursor:
	if 'Obama' in row:
		if race1 in row:
			race1_dates_n.append(row[0])
			race1_data_n.append(row[1])
		
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
num_MM=['01','02','03','04','05','06','07','08','09','10','11','12']


race1_d_n=[]

for a in race1_dates_n:
	for m in months:
		if m in a:
			b=a.split("'")[0]
			MM=num_MM[months.index(str(b).split(" ")[0])]
			D=str(b).split(" ")[1].split(",")[0]
			if len(D)==1:
				DD="0%s"%D
			else:
				DD=D
			YYYY=str(b).split(" ")[2]
			b=date2num(datetime.datetime(int(YYYY),int(MM),int(DD)))
			race1_d_n.append(b)
			#print b

#unique_ify the dates
race1_dates_obama=unique_ify(race1_d_n)
#find all with same date, append corresp data to new list
race1_data_u_n=[]
for date in race1_dates_obama:
	indexes=[i for i, y in enumerate(race1_dates_obama) if y==date]
	sumdata=0
	for a in indexes:
		sumdata=sumdata+race1_data_n[a]
	race1_data_u_n.append(sumdata/float(100))
obama_prob=race1_data_u_n




#ax.scatter(race1_dates_u_n,race1_data_u_n, s=20, c=scattercolor, marker='o') #, edgecolors=scattercolor)
#, marker='^')

ax.plot(race1_dates_obama,obama_prob,c='r', lw=20)


#################################
#####################all republicans for pres election

repub_prob=[]
race1 = race_list[2]

race1_dates_n=[]
race1_data_n=[]

cursor.execute('select * from predictions')
for row in cursor:
	for r in repubs:
		if r in row:
			if race1 in row:
				race1_dates_n.append(row[0])
				race1_data_n.append(row[1])
	
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
num_MM=['01','02','03','04','05','06','07','08','09','10','11','12']


race1_d_n=[]

for a in race1_dates_n:
	for m in months:
		if m in a:
			b=a.split("'")[0]
			MM=num_MM[months.index(str(b).split(" ")[0])]
			D=str(b).split(" ")[1].split(",")[0]
			if len(D)==1:
				DD="0%s"%D
			else:
				DD=D
			YYYY=str(b).split(" ")[2]
			b=date2num(datetime.datetime(int(YYYY),int(MM),int(DD)))
			race1_d_n.append(b)


#unique_ify the dates
race1_dates_u_n=unique_ify(race1_d_n)
#find all with same date, append corresp data to new list
race1_data_u_n=[]
for date in race1_dates_u_n:
	indexes=[i for i, y in enumerate(race1_dates_u_n) if y==date]
	sumdata=0
	for a in indexes:
		sumdata=sumdata+race1_data_n[a]
	race1_data_u_n.append(sumdata/float(100))
repub_prob=race1_data_u_n
#


scattercolor='orange'
#ax.scatter(race1_dates_u_n,race1_data_u_n, s=20, c=scattercolor, marker='_', edgecolors=scattercolor)
ax.plot(race1_dates_u_n,race1_data_u_n,c='m', lw=0, marker='o')

##########################

	
ax.set_xlabel('Date in number format')
ax.set_ylabel('Probability of winning')
plt.show()



#f) In an ef?cient market P(Obama wins) = 1 - Sum P(repub wins) for all time.  
#For the presidential election, ?nd a few dates over the past year where this is 
#farthest from being true. What was happening on those dates? What can you say 
#about the ef?ciency of such trading markets?

outlier_dates=[]
for a in race1_dates_u_n:
	if a in race1_dates_obama:
		i_repub=race1_dates_u_n.index(a)
		i_obama=race1_dates_obama.index(a)
		psum=race1_data_u_n[i_repub]+obama_prob[i_obama]
		buf=0.27
		if psum>1+buf or psum<1-buf:
		outlier_dates.append(num2date(a))
			
