#!/usr/bin/env python
"""
AY 250 - Scientific Research Computing with Python
Homework Assignment 5 Solutions
Author: Christopher Klein


ADAPTED FOR HW 8 BY RADHIKA RAWAT. 

I took out irrelevant portions and added path manipulations to access the new data (lines 25-40, 106, 127).

"""


import sqlite3
import datetime
import urllib2
from bs4 import BeautifulSoup
from numpy import loadtxt, array
from os import listdir, system
import os, sys
from pylab import *


###DEFINE PATH TO TEXTFILE AND PREDICTION DATA


path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
	sys.path.insert(1, path)

PATH_TO_AY250= '../../AY250'

txt_path = os.path.join(path, 'Homework_5_Solutions')

pred_path=os.path.join(PATH_TO_AY250, "Rawat_HW8")


print "\n", "Location of candidate data: \n", txt_path , "\n"
print "Location of prediction data: \n " , pred_path, "\n \n"

sys.path.append(txt_path), sys.path.append(pred_path)



--------------------------------------------------------------------------------
# If the datafile candidate_info.txt is available, can use that to avoid the 
# long/tedious wikipedia scraping. (This won't download the pictures, though.)
use_stored_candidate_data = True

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

# ------------------------	  RACES	  ------------------------------------------
# We create the "races" table and fill it with data for each of the three races.
sql_cmd = """CREATE TABLE races (
	race_id INTEGER PRIMARY KEY AUTOINCREMENT,
	race_name TEXT, 
	election_date DATE, 
	data_url TEXT)"""
cursor.execute(sql_cmd)
races_data = [
				("2012 Republican Presidential Nominee", "2012-08-30", "http://www.intrade.com/v4/markets/?eventId=84328"), 
				("2012 Presidential Election", "2012-08-30", "http://www.intrade.com/v4/markets/?eventId=84326"), 
				("2012 Republican VP Nominee", "2012-11-06", "http://www.intrade.com/v4/markets/?eventId=90482")]
for data in races_data:
	sql_cmd = ("INSERT INTO races (race_name, election_date, data_url) VALUES " + str(data))
	cursor.execute(sql_cmd)

# ------------------------	  CANDIDATES   -------------------------------------
# Ok, next we want to add and populate a table for the candidates.
sql_cmd = """CREATE TABLE candidates (
	candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT, 
	birth_date DATE, 
	party TEXT, 
	home_town TEXT, 
	home_state TEXT, 
	photo_link TEXT)"""
cursor.execute(sql_cmd)

if use_stored_candidate_data:
	stored_candidate_data = loadtxt( os.path.join(txt_path, "candidate_info.txt"), dtype = str)
	for data in stored_candidate_data:
		data_list = data.tolist()[1:]
		data_tuple = (data_list[0], data_list[1], data_list[2], data_list[3],
					  data_list[4], data_list[5])
		sql_cmd = ("""INSERT INTO candidates (name, birth_date, party, 
			home_town, home_state, photo_link) VALUES """ + str(data_tuple))
		cursor.execute(sql_cmd)

# ------------------------	  PREDICTIONS	------------------------------------
# Lastly, we create the predictions table and fill it in.
sql_cmd = """CREATE TABLE predictions (prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
	race_id INT,
	candidate_id INT,
	closing_date DATE, 
	open_value FLOAT, 
	low_value FLOAT, 
	high_value FLOAT, 
	close_value FLOAT, 
	volume INT,
	FOREIGN KEY (race_id) REFERENCES races(race_id),
	FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id))"""
cursor.execute(sql_cmd)

#race_prediction_data = "race_prediction_data" #"Homework_8_race_prediction_data"


# Date,Open,Low,High,Close,Volume
race_prediction_data_filenames = listdir(os.path.join(pred_path, "Homework_8_race_prediction_data")) ##### NEW PREDICTIONS
for filename in race_prediction_data_filenames:

	if filename[-4:] == ".csv":			# make sure it is a CSV file
		race_code = filename.split("_")[-1].split(".")[0]
		# We assign the correct race_id by the code in the filename.
		race_id = 0
		if race_code == "RepNom": race_id = 1
		if race_code == "PresElect": race_id = 2
		if race_code == "RepVPNom": race_id = 3
		# Extract the candidate_name the same way as before.
		candidate_name_list = filename.split("_")[:-1]
		candidate_name = ""
		for fraction in candidate_name_list:
			candidate_name += fraction + "_"
		candidate_name = candidate_name[:-1]
		# Use the candidate_name to query the candidates table and get the 
		# candidate_id
		sql_cmd = """SELECT candidate_id FROM candidates WHERE name = '""" + candidate_name + """'"""
		cursor.execute(sql_cmd)
		candidate_id = array(cursor.fetchall())[0][0]
		# Read in the predictions data file                                                   ##### NEW PREDICTIONS
		prediction_data = loadtxt(os.path.join(pred_path, "Homework_8_race_prediction_data/") + filename, 
			skiprows=1, delimiter=",", dtype=str) 
		for entry in prediction_data:
			month = entry[0].split()[0].lstrip('"')
			# Need to convert the abbreviated month into the string number.
			month_num = "0"
			if month == "Jan": month_num = "1"
			if month == "Feb": month_num = "2"
			if month == "Mar": month_num = "3"
			if month == "Apr": month_num = "4"
			if month == "May": month_num = "5"
			if month == "Jun": month_num = "6"
			if month == "Jul": month_num = "7"
			if month == "Aug": month_num = "8"
			if month == "Sep": month_num = "9"
			if month == "Oct": month_num = "10"
			if month == "Nov": month_num = "11"
			if month == "Dec": month_num = "12"
			day = entry[0].split()[1]
			year = entry[1].lstrip().rstrip('"')
			# closing_date format is year-month-day
			closing_date = year + "-" + month_num + "-" + day
			open_value = entry[2]
			low_value = entry[3]
			high_value = entry[4]
			close_value = entry[5]
			volume = entry[6]
			data = (race_id, candidate_id, closing_date, open_value, low_value, 
				high_value, close_value, volume)
			sql_cmd = ("""INSERT INTO predictions (
						race_id,
						candidate_id,
						closing_date,
						open_value,
						low_value,
						high_value,
						close_value,
						volume) VALUES """ + str(data))
			cursor.execute(sql_cmd)




# ------------------------	  PLOTS	  ------------------------------------------
# Now we are ready to answer the two plotting questions.

# Define a function to run a query for us to return the prediction history for
# a specified candidate in a specified race. This is good for probing the 
# data in a general sense, but we only use it once to determine Obama's 
# prediction history for plot (f).
def prediction_history(q_candidate_name, q_race_id, cursor):
	sql_cmd = """SELECT candidates.name as name, 
						races.race_name as race, 
						predictions.close_value as price, 
						predictions.closing_date as day 
				FROM predictions 
					JOIN candidates on candidates.candidate_id = predictions.candidate_id 
					JOIN races on races.race_id = predictions.race_id
				WHERE 
					races.race_id = """ + q_race_id + """ 
					and candidates.name = '""" + q_candidate_name + """'"""
				   
	cursor.execute(sql_cmd)
	db_info = array(cursor.fetchall())
	days = []
	predictions = []
	for entry in db_info:

		prediction = float(entry[2])
		predictions.append(prediction)

		year_num = int(entry[3].split("-")[0])
		month_num = int(entry[3].split("-")[1])
		day_num = int(entry[3].split("-")[2])
		day = datetime.date(year_num, month_num, day_num)
		days.append(day)
	return days, predictions


# For question (f), we look at the Presidential Election predictions and 
# compare P(Obama Wins) vs 1-P(anyone else wins).
obama_days, obama_predictions = prediction_history("Barack_Obama", "2", cursor)


#define function to get imported for HW 8

def hw8(candidate):
	""" returns date range, prediction history for a given candidate. Candidate format must be "Barack_Obama" """
	return prediction_history(candidate, "2", cursor)

