README
3-4-12: HW4, AY 250, Radhika Rawat

3 files: 
server.py
client.py
audio.py
demo_bw.jpg
demo_color.png

3 folders:
server
soundfigures
sound_files


Assignment 1: Server/Client XMLRPC: I did not find a partner, so I wrote both parts of the connection. I've enclosed two image files (demo_bw.jpg and demo_color.png) to show how the program works on images of two different file types and modes. Right now, the two python files (client.py and server.py) have both image files in them so they'll run automatically on one of them without you needing to change anything. To test it on another image, provide the path in the client file. Examples of original, modified, and reconstructed files from both the client and server are saved in the "server" folder. They'll get saved there when the program runs. The name of the source image is a part of the final images so that it's easy to tell which file they came from.

Assignment 2: Audio recognition: The audio.py file will run using files from the sound_files folder. You can use raw input to choose which file to use from the sound_files folder, but you must omit the extension. The program will output the notes into the terminal window and open a plot of power vs. frequency to show the strongest frequencies in the audio file. The file will save the plots in the soundfigures folder. A log is also kept in that folder with each time that the program was run, the file it was run on, and the resulting note identification. Currently, the log file contains the results of my work. The other images in soundfigures right now are examples of what the plots look like.

Although the program sometimes identifies more than 3 notes, that is because I chose to use octaves to identify different notes as opposed to grouping all Cs together, all Ds together, etc. I thought it would be more useful. 

I got a lot of ideas from the web for this, in some cases copying code directly, so here are the websites that I took information from. I made sure I understand it, but here are the citations:

http://exnumerus.blogspot.com/search/label/Fourier
http://xoomer.virgilio.it/sam_psy/psych/sound_proc/sound_proc_python.html
http://www.swharden.com/blog/2009-01-21-signal-filtering-with-python/
http://bugs.python.org/issue4913


