README
Radhika Rawat AY250, HW5


elections.py creates a database with election information. 


a)	Created a database table called "race_db" with each race?s name, election date, and data URLb)	Didn't need to download race data (provided in folder called race_prediction_data)
c)	Created ?candidates? database table, created a class to store biographical information parsed from wikipedia. Some pages did not follow a consistent format, so I inputted the info manually. d)	Created a database table called ?predictions? 
e)	Plotted as a function of time the probability of a candidate with home state north or south of the Mason-Dixon Line winning each race.

Red: Republican VP Nomination
Cyan: Republican Nomination for president
Blue: Presidential election

Hor. line: south
^: north
magenta line: repub for pres election
wide red line: obama for pres
f)	"In an efficient market P(Obama wins) = 1 - Sum P(repub wins) for all time. For the presidential election, find a few dates over the past year where this is farthest from being true.What was happening on those dates? What can you say about the efficiency of such trading markets?"



The outlier dates are as follows:

2011-02-24 00:00:00+00:00
2011-02-25 00:00:00+00:00
2011-02-26 00:00:00+00:00
2011-02-27 00:00:00+00:00
2011-02-28 00:00:00+00:00
2011-03-02 00:00:00+00:00
2011-03-03 00:00:00+00:00
2011-03-04 00:00:00+00:00
2011-03-30 00:00:00+00:00
2011-03-31 00:00:00+00:00
2011-05-02 00:00:00+00:00

End of Feb/Beginning of March: possibility of government shutdown
5/2: Death of Osama Bin Laden

The meaning: such markets are highly influenced by current events and can be made inefficient if there is a huge influx/efflux of "votes"