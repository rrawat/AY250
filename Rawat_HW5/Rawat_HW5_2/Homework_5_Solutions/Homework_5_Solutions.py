#!/usr/bin/env python
"""
AY 250 - Scientific Research Computing with Python
Homework Assignment 5 Solutions
Author: Christopher Klein
"""

import sqlite3
import datetime
import urllib2
from bs4 import BeautifulSoup
from numpy import loadtxt, array
from os import listdir, system
from pylab import *

# If the datafile candidate_info.txt is available, can use that to avoid the 
# long/tedious wikipedia scraping. (This won't download the pictures, though.)
use_stored_candidate_data = True

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

# ------------------------    RACES   ------------------------------------------
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

# ------------------------    CANDIDATES   -------------------------------------
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
    stored_candidate_data = loadtxt("candidate_info.txt", dtype = str)
    for data in stored_candidate_data:
        data_list = data.tolist()[1:]
        data_tuple = (data_list[0], data_list[1], data_list[2], data_list[3],
                      data_list[4], data_list[5])
        sql_cmd = ("""INSERT INTO candidates (name, birth_date, party, 
            home_town, home_state, photo_link) VALUES """ + str(data_tuple))
        cursor.execute(sql_cmd)
else:
    # We extract all the candidate names (name format First_Last or 
    # First_Middle_Last or however many middle names there are).
    candidate_names = []
    race_prediction_data_filenames = listdir("race_prediction_data")
    for filename in race_prediction_data_filenames:
        if filename[-4:] == ".csv":         # make sure it is a CSV file
            candidate_name_list = filename.split("_")[:-1] # pull out list of 
                                                           # name fractions
            candidate_name = ""
            # add name fractions to reassemble full name
            for fraction in candidate_name_list:
                candidate_name += fraction + "_"
            candidate_name = candidate_name[:-1] # remove the last "_"
        # Finally, append to list as long as that name is unique in the list.
        if candidate_name not in candidate_names:
            candidate_names.append(candidate_name)
    
    # Here we build up the data we will insert into the "candidates" table. 
    # Wikipedia scraping adapted from Katherine De Kleer's homework submission.
    print '%PREDICT ELECTIONS: crawling wikipedia & parsing html'
    # To access wikipedia, we have to pretend to be a browser.
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    candidates_data = []
    for candidate_name in candidate_names:
        # Define name for output image file
        outfile = candidate_name + '.jpg'
        # We need to reformat some candidate names into proper search names for
        # wikipedia.
        search_name = candidate_name
        if candidate_name == "Allen_West":
            search_name = 'Allen_West_(politician)'
        if candidate_name == 'John_Bolton':
            search_name = 'John_R._Bolton'
        if candidate_name == "Jon_Huntsman":
            search_name = 'Jon_Huntsman,_Jr.'
        if candidate_name == "Lindsay_Graham":
            search_name = 'Lindsey_Graham'
    
        # open wikipedia page and grab thml data
        wikipage = 'http://en.wikipedia.org/w/index.php?title='+search_name+'&printable=yes'   
        infile=opener.open(wikipage)
        page=infile.read()
        soup = BeautifulSoup(''.join(page))
        trlist = soup.findAll('tr')
    
        skip = True
        gotbday=False
        gotparty=False
        gotpic=False
        for line in trlist:
            if (gotbday==False) and ('bday' in str(line)):
                # get birthday
                if ('Biden' in candidate_name) and (skip==True):
                    # special case: skip first birthday listing
                    skip=False
                    continue
                if 'title' in str(line):
                    # parse various formatting cases for birthdate, hometown, and homestate
                    birthdate = str(line).split('bday">')[1].split('</span>')[0]
                    gotbday = True
                    homeline1 = str(line).split('bday">')[1].split('title')
                    if len(homeline1)==2:
                        homeline1=homeline1[-1]
                        if (homeline1[0]+homeline1[1])=='="':
                            hometown=homeline1.split('="')[1].split(',')[0].split('"')[0]
                            homestate=homeline1.split('="')[1].split(', ')[1].split('">')[0].split('<')[0]
                    else: 
                        if len(homeline1)==3:
                            hometown=homeline1[-2].split('=>')[0].split('="')[1].split(',')[0].split('">')[0]
                            homestate=homeline1[-1].split('=>')[0].split('="')[1].split(',')[0].split('">')[0]
                            if 'United' in homestate:
                                homestate=homeline1[-2].split('=>')[0].split('="')[1].split(', ')[1].split('">')[0]
                        else:
                            if len(homeline1)==4:
                                hometown=homeline1[-3].split('=>')[0].split('="')[1].split(',')[0].split('">')[0]
                                homestate=homeline1[-3].split('=>')[0].split('="')[1].split(', ')[1].split('">')[0]
                else: 
                    birthdate = str(line).split('bday">')[1].split('</span>')[0].split()[0]
                    gotbday = True
                    if birthdate == '1937-04-05':
                        hometown = 'New York City'
                        homestate = "New York"
                    else:
                        hometown = str(line).split('U.S.')[-2].split(',')[1].split('\n')[-1]
                        homestate = str(line).split('U.S.')[-2].split(', ')[-2]
                if ('New York' in homestate) or ('Long Island' in homestate):
                    homestate = 'New York'
            if ('Political party' in str(line)) and (gotparty==False):
                # parse and collect political party affiliation
                affiliation = 'none'
                if 'title' in str(line):
                    affiliation = str(line).split('title="')[1].split('">')[1].split('</a>')[0]
                else:
                    affiliation = str(line).split('<td')[1].split('>')[0]
                # standardize political party formatting
                if ('Republican' in affiliation):
                    affiliation = 'Republican'
                if ('Democrat' in affiliation.split(' ')[0]):
                    affiliation = 'Democrat'
                if (affiliation=='' or affiliation=='none'):
                    affiliation = 'Independent'
                gotparty=True
    
        # Here we download the images.
            if ('.jpg' in str(line)) and (gotpic==False):
                picurl='http:'+str(line).split('src="')[1].split('"')[0]
                print "Fetching pic from", picurl
                picfile = opener.open(picurl)
                picpage = picfile.read()
                output = open('pictures/'+outfile,'wb')
                output.write(picpage)
                output.close()
                gotpic=True
        
        # Write out the info to a list, which will then be looped over to insert 
        # into the database.
        candidates_data.append((candidate_name, birthdate, affiliation, 
                                hometown, homestate, outfile))
        print "Finished Collecting:"
        print "\t", candidate_name, birthdate, affiliation, hometown, homestate, outfile
    
    # Then, insert the candidate data.
    for data in candidates_data:
        sql_cmd = ("""INSERT INTO candidates (name, birth_date, party, 
                        home_town, home_state, photo_link) VALUES """ + str(data))
        cursor.execute(sql_cmd)


# ------------------------    PREDICTIONS   ------------------------------------
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

print "Inserting Prediction Data"
# Date,Open,Low,High,Close,Volume
race_prediction_data_filenames = listdir("race_prediction_data")
for filename in race_prediction_data_filenames:
    if filename[-4:] == ".csv":         # make sure it is a CSV file
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
        # Read in the predictions data file
        prediction_data = loadtxt("race_prediction_data/" + filename, 
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


# ------------------------    PLOTS   ------------------------------------------
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

# For question (e) we define states to be in the North or South.
north_states = ['Alaska',
 'Connecticut',
 'Delaware',
 'Idaho',
 'Illinois',
 'Indiana',
 'Iowa',
 'Maine',
 'Massachusetts',
 'Michigan',
 'Minnesota',
 'Montana',
 'Nebraska',
 'New Hampshire',
 'New Jersey',
 'New York',
 'North Dakota',
 'Ohio',
 'Oregon',
 'Pennsylvania',
 'Rhode Island',
 'South Dakota',
 'Vermont',
 'Washington',
 'Wisconsin',
 'Wyoming',
 'Washington D.C.']
south_states = ['Alabama',
 'Arizona',
 'Arkansas',
 'California',
 'Colorado',
 'Florida',
 'Georgia',
 'Hawaii',
 'Kansas',
 'Kentucky',
 'Louisiana',
 'Maryland',
 'Mississippi',
 'Missouri',
 'Nevada',
 'New Mexico',
 'North Carolina',
 'Oklahoma',
 'South Carolina',
 'Tennessee',
 'Texas',
 'Utah',
 'Virginia',
 'West Virginia']
# Then we run queries to get the prediction data. We query on specific dates, 
# the days for which Obama has data (makes it a bit simpler).
obama_days, obama_predictions = prediction_history("Barack_Obama", "2", cursor)

rep_nom_north = []
rep_nom_south = []
for day in obama_days:
    year_num = str(day.year)
    month_num = str(day.month)
    day_num = str(day.day)
    date_string = year_num + "-" + month_num + "-" + day_num
    sql_cmd = """SELECT predictions.close_value as price,
                        candidates.home_state as state
                FROM predictions 
                    JOIN candidates on candidates.candidate_id = predictions.candidate_id 
                    JOIN races on races.race_id = predictions.race_id
                WHERE
                    races.race_id = 1
                    and predictions.closing_date = '""" + date_string + """'
                    """
    cursor.execute(sql_cmd)
    db_info = array(cursor.fetchall())
    north_predictions = []
    south_predictions = []
    for entry in db_info:
        if entry[1] in north_states:
            north_predictions.append(float(entry[0]))
        else:
            south_predictions.append(float(entry[0]))
    rep_nom_north.append(sum(north_predictions))
    rep_nom_south.append(sum(south_predictions))
plot(obama_days, rep_nom_north, label="North")
plot(obama_days, rep_nom_south, label="South")
legend()
savefig("plot_e_RepNom.pdf")
close("all")

rep_pres_north = []
rep_pres_south = []
for day in obama_days:
    year_num = str(day.year)
    month_num = str(day.month)
    day_num = str(day.day)
    date_string = year_num + "-" + month_num + "-" + day_num
    sql_cmd = """SELECT predictions.close_value as price,
                        candidates.home_state as state
                FROM predictions 
                    JOIN candidates on candidates.candidate_id = predictions.candidate_id 
                    JOIN races on races.race_id = predictions.race_id
                WHERE
                    races.race_id = 2
                    and predictions.closing_date = '""" + date_string + """'
                    """
    cursor.execute(sql_cmd)
    db_info = array(cursor.fetchall())
    north_predictions = []
    south_predictions = []
    for entry in db_info:
        if entry[1] in north_states:
            north_predictions.append(float(entry[0]))
        else:
            south_predictions.append(float(entry[0]))
    rep_pres_north.append(sum(north_predictions))
    rep_pres_south.append(sum(south_predictions))
plot(obama_days, rep_pres_north, label="North")
plot(obama_days, rep_pres_south, label="South")
legend()
savefig("plot_e_Pres.pdf")
close("all")

rep_vpnom_north = []
rep_vpnom_south = []
for day in obama_days:
    year_num = str(day.year)
    month_num = str(day.month)
    day_num = str(day.day)
    date_string = year_num + "-" + month_num + "-" + day_num
    sql_cmd = """SELECT predictions.close_value as price,
                        candidates.home_state as state
                FROM predictions 
                    JOIN candidates on candidates.candidate_id = predictions.candidate_id 
                    JOIN races on races.race_id = predictions.race_id
                WHERE
                    races.race_id = 3
                    and predictions.closing_date = '""" + date_string + """'
                    """
    cursor.execute(sql_cmd)
    db_info = array(cursor.fetchall())
    north_predictions = []
    south_predictions = []
    for entry in db_info:
        if entry[1] in north_states:
            north_predictions.append(float(entry[0]))
        else:
            south_predictions.append(float(entry[0]))
    rep_vpnom_north.append(sum(north_predictions))
    rep_vpnom_south.append(sum(south_predictions))
plot(obama_days, rep_vpnom_north, label="North")
plot(obama_days, rep_vpnom_south, label="South")
legend()
savefig("plot_e_RepVPNom.pdf")
close("all")



# For question (f), we look at the Presidential Election predictions and 
# compare P(Obama Wins) vs 1-P(anyone else wins).
obama_days, obama_predictions = prediction_history("Barack_Obama", "2", cursor)
# For the "anyone else wins" we basically query for all the other candidates,
# but we will do one query per day of obama's prediction history.
obama_predictions_2 = []
for day in obama_days:
    year_num = str(day.year)
    month_num = str(day.month)
    day_num = str(day.day)
    date_string = year_num + "-" + month_num + "-" + day_num
    sql_cmd = """SELECT predictions.close_value as price
                FROM predictions 
                    JOIN candidates on candidates.candidate_id = predictions.candidate_id 
                    JOIN races on races.race_id = predictions.race_id
                WHERE
                    races.race_id = 2
                    and predictions.closing_date = '""" + date_string + """'
                    and candidates.name <> 'Barack_Obama'"""
    cursor.execute(sql_cmd)
    db_info = array(cursor.fetchall())
    obama_predictions_2.append(db_info.sum())

efficiency = array(obama_predictions) - array(obama_predictions_2)
plot(obama_days, efficiency, label="Market (In)Efficiency")
legend()
savefig("plot_f.pdf")
close("all")
# Looking at the plot, we see fast, high peaks around early May, 2011. This was
# when the Navy Seals caught and killed Osama Bin Laden, which in turn led to 
# the prediction market over-valuing Obama.

cursor.close()