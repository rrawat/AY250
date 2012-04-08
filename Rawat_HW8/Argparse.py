# Elections are coming up, and we want to re-use our code to see how things 
# are going!  Download the latest prediction data from Intrade into your 
# Week 8 homework folder.  Without moving the base code from your 
# Week 5 (databases) folder*, load the necessary functions from that code 
# into a new module for your Week 8 folder which parses command-line 
# input using argparse.  Allow the user to retrieve  information from the 
# database in a user-friendly way from the command line: e.g. 
# python ElectionPredictions.py -c Obama -d 2012-03-28 
# would print out the Barack Obama's closing value on March 28th. Include 
# an option -p or --plot  which shows a plot of all the predicted values for 
# the candidate over time, with the value at the speci!ed date highlighted.  
# Include the necessary checks to make sure the user's path is set correctly to 
# import the code from Week 5.



import os, sys
import argparse
import matplotlib.pyplot as plt
import datetime



path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
	sys.path.insert(1, path)
sys.path.append(os.path.join(path, 'Rawat_HW5/Rawat_HW5_2/Homework_5_Solutions'))

from Homework_5_HW8_version import * #old, working for previous data set: Homework_5_Solns


cand_list = ['Allen_West','Barack_Obama','Bill_McCollum',\
'Bob_Corker','Bob_McDonnell','Bobby_Jindal','Brian_Sandoval',\
'Buddy_Roemer','Carly_Fiorina','Cathy_McMorris_Rodgers',\
'Charlie_Crist','Chris_Christie','Clarence_Thomas','Colin_Powell',\
'Condoleezza_Rice','Dave_Heineman','David_Petraeus','Dick_Cheney',\
'Donald_Trump','Eric_Cantor','Fred_Thompson','Gary_Johnson',\
'George_Pataki','Haley_Barbour','Herman_Cain','Hillary_Clinton',\
'JC_Watts','Jeb_Bush','Jim_DeMint','Joe_Biden','Joe_Lieberman',\
'Joe_Scarborough','John_Boehner','John_Bolton','John_Kasich',\
'John_Thune','Jon_Huntsman_Jr','Jon_Huntsman','Jon_Kyl','Judd_Gregg',\
'Kelly_Ayotte','Lindsay_Graham','Lou_Dobbs','Luis_Fortuno',\
'Marco_Rubio','Mark_Sanford','Meg_Whitman','Michael_Bloomberg',\
'Michele_Bachmann','Mike_Huckabee','Mike_Pence','Mitch_Daniels',\
'Mitt_Romney','Newt_Gingrich','Nikki_Haley','Pat_Toomey','Paul_Ryan',\
'Rand_Paul','Rick_Perry','Rick_Santorum','Rob_Portman','Ron_Paul',\
'Roy_Moore','Rudy_Giuliani','Sarah_Palin','Scott_Brown',\
'Stanley_McChrystal','Susana_Martinez','Thad_McCotter','Tim_Pawlenty','Tom_Coburn']




#set default to no plotting
plot=0


#store user input
parser = argparse.ArgumentParser(description='Candidate Data')

parser.add_argument('-c', action='store', dest='cand_str', help='Store the Candidate name in the format First Last')
parser.add_argument('-d', action='store', dest='date_str', help='Store the date, in the format: YYYY-MM-DD')
parser.add_argument('-p', action='store_const', dest='plot', const=1, help='Store a constant value')
results = parser.parse_args()

cand_str, date_str, plot = results.cand_str, results.date_str, results.plot




#check if given name is in the candidate list
viable_cand=0

for cand in cand_list:
	if results.cand_str in cand:
		candidate=cand
		viable_cand=1

if viable_cand==0:
	print "Please enter a candidate in the candidate list (First, Last, or both with an underscore in between): \n \n", cand_list
	sys.exit()
	
	
date_s= str(date_str).split("-")

M=int(date_s[1])
YYYY=int(date_s[0])
D=int(date_s[2])


fn_date=(YYYY,M,D)
days, predictions = hw8(candidate)



def date_fn(func_date, day_range, preds, plot=0):
	""" takes in the user-provided date, the condidate data range (days\
	and corresponding closing values), and the plotting preference. Plot defaults\
	to 0, returning no figure, but when set to 1, it will show the closing price\
	over time, with the chosed date highlighted in red."""
	
	YYYY, M, D = func_date[0],func_date[1],func_date[2]
	date= datetime.date (YYYY,M,D)
	print min(day_range), max(day_range)
	if date not in day_range:
		print "Data for this candidate are only available between %s and %s . Please choose a date accordingly." %(str(min(day_range)),str(max(day_range)))
		return
	
	for day in day_range:
		if day == date:
			print "Candidate:", candidate, "\t", "Date:", day, "\t", "Closing Value", preds[day_range.index(day)]
			if plot == 1:
				f=plt.figure()
				ax=f.add_subplot(111)
				ax.plot(day_range, preds)
				ax.scatter(day,preds[day_range.index(day)], color = 'red', marker = 'o')
				plt.show()

try: date_fn(fn_date, days, predictions, plot)
except: print "Please choose a candidate who was considered for the elections."
finally: pass
