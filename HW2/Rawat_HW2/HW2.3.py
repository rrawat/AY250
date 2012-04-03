def function(x):
	"must be one dimentional in input"
	"an example of the type of func that can be passed into one_D_sample() "
	return -x**2+10*x+10

import numpy as np
import scipy.stats
from scipy.stats import norm
import matplotlib
import matplotlib.pyplot as plt
import math



def one_D_sample(targetDist, referenceDist, n_samplesDesired, m):
	
	
	""" 
	this function uses rejection sampling to sample from the target Distribution using the reference distriubtion.
	Returns a list of samples, prints what m was, the percent of samples that were accepted.
	
	targetDistribution must take one input,
	referenceDistribution must be scipy.stats object
	n_samples must be an integer
	"""
	
	target=targetDist
	ref=referenceDist
	n=n_samplesDesired
	

	samples = []					#accepted, useful samples
	rejects=[]						#non-useful samples
		
	while len(samples) < n:			#run the script to test new sample while number is not met
		x = ref.rvs(size=1)[0]
		u = scipy.stats.uniform.rvs(size=1)
		
		if u < (target(x)/float(m*ref.pdf(x))): #rejection sampling algorithm
			# then x is a useful sample
			samples.append(x)
		else:
			rejects.append(x)
		
	p=100*(len(samples)/float(len(samples)+len(rejects)))
	
	
	print "samples: \n" , samples, "\n" "m=", m, "\n" "percent accepted", p
	return samples

one_D_sample(function, scipy.stats.norm(0,1), 20, 10)


#PART B: going to use 1D sampler to do this, since using 1D laplacian distrib

print "\n", "\n", "\n", '---Part B---' 

def laplace(x):
	import math
	b=1
	mu=0
	return (1/float(2*b))*math.exp((-(math.fabs(x-mu))/b))
	
	
#m:I used an arbitary, high number for m because while I know that m must be computed by comparing the maximum point of the target distribution to the minimum of the reference dist, I was not sure how to adjust for distributions that approach zero towards infinity. Thus, M is set.

m=20

#generate sample from rejection sampling	

laplacian_rej_sample = one_D_sample(laplace, scipy.stats.cauchy, 1000, m)	
				
#plot histogram of samples
fig=plt.figure()
ax=fig.add_subplot(111)
ax.hist(laplacian_rej_sample,bins=50) 

#over plot true Laplace pdf
x = np.arange(0,5,.005)
laplace_pdf = np.arange(0,5,.005)
for i in range(0,len(x)):
	laplace_pdf[i] = scipy.stats.laplace.pdf(float(x[i]))

ax.plot(x,900*laplace_pdf, 'r--', linewidth=3)
#show plot
plt.show()	
print "doing kolmogorov-smirnof test to compare rejection sampling output to real pdf of laplacian"



ks_statistic, pvalue = scipy.stats.ks_2samp(laplacian_rej_sample, laplace_pdf)
print "pvalue = ", pvalue
	
#cutoff=#
#if pvalue> cutoff:
#	print "hence, since the p-value is high, we cannot reject the hypothesis that the distributions of the two samples are the same...rejection did a good job"



####PartC


print "\n", "\n", "\n", '---Part C---' 

def one_D_sample_ptC(targetDist, referenceDist, n_samplesDesired, m):
	
	""" 
	This is just like the first function, but it allows ref.rvs to take in the degrees of freedom as an input, which is necessary for ttests.
	Returns a list of samples
	
	targetDistribution must take one input,
	referenceDistribution must be scipy.stats object
	n_samples must be an integer
	"""
	
	target=targetDist
	ref=referenceDist
	n=n_samplesDesired
	

	samples = []
	rejects=[]		
	
	while len(samples) < n:
		x = ref.rvs(df)[0]
		u = scipy.stats.uniform.rvs(size=1)
		
		if u < (target(x)/float(m*x)):
			# then x is a useful sample
			samples.append(x)
		else:
			rejects.append(x)
		
	p=100*(len(samples)/float(len(samples)+len(rejects)))
	
	
	print "samples: \n" , samples, "\n" "m=", m, "\n" "percent accepted", p
	return samples

df=2
laplacian_rej_sample_tTest_reference = one_D_sample_ptC(laplace,scipy.stats.t(df), 1000,m)	






####Part D
#the continuous prob distribution of my choice is the normal, gaussian distribution, mean 100, sd = 15. These are the parameters that correspond to the distribution of IQ scores.


print "\n", "\n", "\n", '---Part D---' 
#using a normal distribution, mean=100, stdev=15
def IQ_PDF(x):
	constant = (1./(15*np.sqrt(2*np.pi)))
	return constant * np.exp( -.5 * (x-100)**2   / (15.**2)  )

IQsample = one_D_sample(IQ_PDF, scipy.stats.uniform(0, 200), 5000, 2)

#plot samples
fig=plt.figure()
ax=fig.add_subplot(111)
ax.hist(IQsample,bins=50)

#plot reference dist
x = np.arange(0,5,.005)
laplace_pdf = np.arange(0,5,.005)


for i in range(0,len(x)):
	laplace_pdf[i] = scipy.stats.norm.pdf(float(x[i]), loc=100, scale=15)

ax.plot(x,1000*laplace_pdf, 'r--', linewidth=3)
plt.show()




