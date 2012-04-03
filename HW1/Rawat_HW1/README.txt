README

Homework 1 - due 2-05-12
Radhika Rawat
AY 250


Files:

Part 1: Recreate an old figure
	
	lexical_score.txt		#data
	1_LexScoreimg.jpg		#original image
	1_Recreated_figure.py	#code
	1_LexScoreimg.png		#new image
	
	
Part 2: Reproduce the NY Stocks Plot

	2_stocks.png		#original image
	2_NYStocks.py		#code
	2_nystocks-new.png	#new image
	google_data.txt		#google data
	yahoo_data.txt		#yahoo data
	ny_temps.txt		#ny temperature data
	
	
	#Note: the size of the window has to be adjusted, but once the user drags the window appropriately, everything else should work.


Part 3: General Brushing Code
	
	3_brushing.py		#code
	Screen shot 2012-02-05 at 9.52.29 PM	#example figure/GUI
	
	##About Brushing.py: 

	##Brushing.py uses the same data file as Part 1 (lexicalscore.txt) and brushes on 4 subplots. Rectangles are drawn based on a user's click and unclick location within a subplot. Points spanned by the click (x and y directions) are shown in a different color, rather than changed opacity. Every time a new rectangle is drawn, all points will flash in the original yellow color (if the program is running slowly) before the appropriate ones turn red. I ran into some hardware problems, so rather than using "d" to remove rectangles/data, I used right click. The code to use "d" is still in the file, but commented out. In order to remove rectangles, it sometimes takes clicks in different parts inside the rectangle. Might be necessary to move around and click a few times. Throughout the code, lex is used to mean the recarray of the data.

	
	