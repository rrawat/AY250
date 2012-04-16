import sys
import os
from time import time
from random import uniform
from math import sqrt
from multiprocessing import Process, Value, Pool

def dart_algorithm(num_of_throws):
	'''implements the monte carlo dart algorithm. Takes in number of darts to throw and returns\
	the number of darts in the circle and the calculation time. '''
	
	start_time = time()
	darts_in_circle = 0
	for i in xrange(num_of_throws):
		x,y = uniform(0,1),uniform(0,1)
		if sqrt( (x-.5)**2 + (y-.5)**2 ) < .5 :
			darts_in_circle += 1
	end_time = time()		
	return darts_in_circle
	
	
#--------------------------------- Multiprocessing Method ---------------------------------	


def multiprocessing_method(n_of_darts, n_of_pools = 10):
	'''Uses 10 processes to split the work of dart_algorithm. Since the processes are independent, \
	I split the number of darts over the number of processes, and used the pool function. Instead of \
	looping over the number of processes, which would be time-consuming, I wrote them explicitly.'''
	
	global Pool_darts_in_circle,Pool_time
	Pool_darts_in_circle = 0
	Pool_time = 0
	
	pool = Pool(processes=n_of_pools)  
	darts_per_pool = n_of_darts/n_of_pools

	start=time()
	result1 = pool.map_async(dart_algorithm, [darts_per_pool])
	result2 = pool.map_async(dart_algorithm, [darts_per_pool])
	result3 = pool.map_async(dart_algorithm, [darts_per_pool])
	result4 = pool.map_async(dart_algorithm, [darts_per_pool])
	result5 = pool.map_async(dart_algorithm, [darts_per_pool])
	result6 = pool.map_async(dart_algorithm, [darts_per_pool])
	result7 = pool.map_async(dart_algorithm, [darts_per_pool])
	result8 = pool.map_async(dart_algorithm, [darts_per_pool])
	result9 = pool.map_async(dart_algorithm, [darts_per_pool])
	result10 = pool.map_async(dart_algorithm, [darts_per_pool])
	end=time()
	
	Pool_darts_in_circle = result1.get()[0] + result2.get()[0]+result3.get()[0] +\
	result4.get()[0]+result5.get()[0]+result6.get()[0]+ result7.get()[0]+ \
	result8.get()[0]+ result9.get()[0]+ result10.get()[0]
	


	Pool_time += end-start
	pool.close()
	pool.join()
	
	pi = 4 * Pool_darts_in_circle / float(n_of_darts)
	# print "multiprocessing pi approximation= ", pi
	return Pool_time
	
#--------------------------------- IPcluster Method ---------------------------------	
def sim_for_IP(num_of_throws):
	'''Does generally the same thing as the dart_algorithm function, but imports the modules \
	as is required for the IPcluster method. Takes in the number of darts thrown and returns \
	the number of darts in the circle.'''

	from random import uniform
	from math import sqrt
	darts_in_circle = 0
	for i in xrange(num_of_throws):
		x,y = uniform(0,1),uniform(0,1)
		if sqrt( (x-.5)**2 + (y-.5)**2 ) < .5 :
			darts_in_circle += 1
	return darts_in_circle

def IPcluster_method(n_of_darts):
	"""Uses 5 actions to perform the work of sim_for_IP in parallel, with each one computing the \
	number of darts in the circle for 1/5 the total number of darts thrown. Elapsed time is measured \
	as the time it takes for the processes to complete."""
	from IPython import parallel
	rc = parallel.Client()
	print n_of_darts
	start=time()
	res1=rc[:].map_async(sim_for_IP, [n_of_darts/5])
	res2=rc[:].map_async(sim_for_IP, [n_of_darts/5])
	res3=rc[:].map_async(sim_for_IP, [n_of_darts/5])
	res4=rc[:].map_async(sim_for_IP, [n_of_darts/5])
	res5=rc[:].map_async(sim_for_IP, [n_of_darts/5])	
	end=time()
	darts_in_circle=res1.get()[0] +res2.get()[0]+res3.get()[0]+res4.get()[0]+res5.get()[0]
	

	pi = 4 * darts_in_circle / float(n_of_darts)
	#print "IPcluster pi approximation= ", pi
	
	elapsed=end-start
	return elapsed

#--------------------------------- Simple Method ---------------------------------

def simple_method(n_of_darts):
	'''Measures time taken to complete dart_algorithm for the total number of throws without \
	any parallelization.'''

	darts_in_circle = 0
	start_time = time()
	darts_in_circle=dart_algorithm(n_of_darts)

	end_time = time()
	total_time = end_time - start_time
	pi = 4 * darts_in_circle / float(n_of_darts)
	#print "simple_method pi approximation= ", pi
	return total_time

		
		

#--------------------------------- Data Collection ---------------------------------


darts_thrown = []
simplelist = []
iplist = []
poollist = []
maxtime=10

for dart_throws in [10,100,1000, 10000, 100000,1000000]:
	darts_thrown.append(dart_throws)
	
	x = simple_method(dart_throws); simplelist.append(x)
	
	y= IPcluster_method(dart_throws); iplist.append(y)
	
	z = multiprocessing_method(dart_throws); poollist.append(z)
	
	if (x>maxtime) or (y>maxtime) or (z>maxtime):
		break
		
print "Finished data collection. Plotting."	



#--------------------------------- Plotting ---------------------------------


import matplotlib.pyplot as plt
import numpy as np
from numpy import log

darts = np.array(darts_thrown)
simple = np.array(simplelist)
ip = np.array(iplist)
pool = np.array(poollist)



fig=plt.figure()


#ax shows the solid lines corresponding to delta time v. total darts thrown, both on log scales

ax=fig.add_subplot(111)

ax.loglog()

ax.set_ylabel('Time(s): solid line')
ax.set_xlabel('Number of Darts Thrown')

ax.plot(darts,simple,'m', label='simple method', lw=2, marker='o', ms=5)
ax.plot(darts,ip,'orange', label ='IPcluster', lw=2, marker='o', ms=5)
ax.plot(darts,pool,'g', label = 'pool', lw=2,  marker='o', ms=5)

#ax2 shows dashed lines, xaxis is total darts thrown(logscale), yaxis is rate of throwning: darts/second

ax2=ax.twinx()

ax2.semilogy()
ax2.set_ylabel('Rate in Darts/Second: dashed line')


ax2.plot(darts,darts/simple, 'm--')
ax2.plot(darts,darts/ip,'y--')
ax2.plot(darts,darts/pool,'g--')

axline=ax.get_lines()

legend=ax.legend((axline[0],axline[1],axline[2]), ('Simple Method', 'IPcluster Method', 'Multiprocessing Method'), loc=2)

plt.show()

