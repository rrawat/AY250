#audio program

import pyaudio
import aifc
import matplotlib.pyplot as plt
import matplotlib as mp
import numpy as np
import struct
import scipy, math
import datetime 
from scipy import stats


#user inputs name of file WITHOUT the extension
file_input = raw_input("type the name of the audiofile to analyze (omit extension) -->")

file = "%s.aif" %file_input
audio = aifc.open("sound_files/%s" % file, "r")


#open log file for the results
f = open("soundfigures/log.txt", "a")


f.write('%s \n' %datetime.datetime.now())
f.write("sound file: %s \n" %file)
f.close()

#define audio vars
Frate =  audio.getframerate(), #frequency (Hz) sampling rate
Frames = audio.getnframes() #total number of frames
width = audio.getsampwidth() 
channels = audio.getnchannels()


#referenced http://bugs.python.org/issue4913 for these methods. 

audio_data =  audio.readframes(Frames) 

unpacked_audio_data = struct.unpack("<%uh" % (len(audio_data) / width), audio_data) #now in base 16


#normalize for number of channels
listed_data= []
if channels >1:
	for i in xrange(channels):
		listed_data.append([unpacked_audio_data[audiobit] for audiobit in xrange(0,len(unpacked_audio_data),channels)])
else:
	listed_data = [unpacked_audio_data]
#strip extra listing
data_list=listed_data[0]

#do fast fourier transformation
data_array=np.array(data_list)
fft=scipy.fft(data_array)

#get power of signal at each frequency
n=len(data_list)
power_list=(abs(fft)/float(n))**5


# **from the website cited above** : ensures the lengths of the input for the FFT and the freq_array are equal.
if n % 2 > 0:
    power_list[1:len(power_list)] = power_list[1:len(power_list)] * 2
else:
	power_list[1:len(power_list) -1] = power_list[1:len(power_list) - 1] * 2

#divide sampling rate by number of points sampled (rate of change: frequency) to scale according to number of data points 

freq_array = np.arange(0, len(np.log10(power_list)), 1.0) *(Frate[0] / float(n))

#power, scaled from decibels (log10)
y_array = np.log10(power_list)

#plot frequency vs power
plt.figure()
plt.subplot(111)
plt.plot(freq_array,y_array , color='b')
plt.xlabel('Frequency, Hz')
plt.ylabel('Power')

plt.xlim((200, 990))
plt.ylim((np.mean(y_array),0.5+np.max(y_array)))




#get frequencies corresponging to power maxima to identify dominant notes
frequencies=[]
def findmaxima(lower_limit=0,upper_limit=990): #lower and upper bounds of frequency range
	limit = mp.mlab.prctile(y_array[low:high,],100) 	
	for i in xrange(freq_array.shape[0]):
		if freq_array[i]<lower_limit:
			continue
		if freq_array[i]>upper_limit:
			pass
		elif y_array[i] > limit:
			frequencies.append(freq_array[i,])
findmaxima()

notes=[]
notefrequencies=[1318,1244,1174,1108,1046,987,932,880,830,783,739,698,659,622,587,554,523,493,466,440,415,391,369,349,329,311,293,277,261,246,233,220,207,195,184,174,164,155,146,138,130,123,116,110,103,97]

notenames=['E6','D6S','D6','C6S','C6','B5','A5S','A5','G5S','G5','F5S','F5','E5','D5S','D5','C5S','C5','B4','A4S','A4','GS4','G4','FS4','F4','E4','DS4','D4','CS4','C4','B3','AS3','A3','GS3','G3','FS3','F3','E3','DS3','D3','CS3','C3','B2','AS2','A2','GS2','G2']



for i in range(1,len(frequencies)):
	for note in notefrequencies:
		if math.fabs(frequencies[i] - note) <3:
			notes.append(notenames[notefrequencies.index(note)])


#eliminate notes from noisy peaks
for a in notes:
	if notenames.index(a)==(len(notenames)-1):
		
		pass
	else:
		b=notenames[notenames.index(a)+1]
		if b in notes:
			if notes.count(a)<notes.count(b):
				while a in notes:
					notes.remove(a)
			elif notes.count(b)<notes.count(a):
				while b in notes:
					notes.remove(b)	
#return only unique note names
def unique_ify(seq):
    contained = set()
    contained_add = contained.add
    return [ x for x in seq if x not in contained and not contained_add(x)]

print "This audio file contains the following notes:", unique_ify(notes)


f = open("soundfigures/log.txt", "a")
f.write("Notes:%s" %(str(unique_ify(notes))))
f.write(" \n \n")

f.close()


plt.savefig("soundfigures/%s.png"%file_input)


