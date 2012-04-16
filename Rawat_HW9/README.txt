AY250 HW9: Parallelization
Radhika Rawat 
April 15, 2012

#-------------------- Before running the program --------------------

Before running hw9.py, start a cluster. I did this via starcluster:

$ starcluster start <<clustername>>
$ starcluster sshmaster <<clustername>> -u <<username (default=sgeadmin>>
##in a new terminal##
$ ipcluster start --n=4

Once it says "[IPClusterStart] Engines appear to have started successfully", 
open a new terminal and run the program from ipython.

#-------------------- The program --------------------

hw9.py takes the monte carlo alorithm provided in the assignment and 
implements it 
1. as is, 
2. using the multiprocessing method, and 
3. using IPclusters to parallelize.

The run times are measured as the number of darts increases from 10 to 
10^6, by factors of 10. 

To avoid errors, restart ipython between every run of the program. You may 
otherwise encounter "OSError: [Errno 24] Too many open files"


#-------------------- The graph --------------------

image15-7.07.png

Time:

As the number of darts increased from 10 to 10^6, the time taken for the 
non-parallelized function increased by powers of 10, while it remained constant
on the order of 10^-2 and 10^-3 s for the parallelized methods. This indicates
that the processes were not at their maximum load, so they could tolerate the 
workload without slowing down. Parallelizing also means absorbing the time taken
to split up the task, which explains the relatively higher time taken at low 
numbers of darts thrown; while the numbers weren't high, time was taken to divvy
up the task.

Rate:

The simple method had a constant rate, which makes sense considering it treats 
each dart the same way, and does so independently without regard for how many 
there are. In contrast, the parallel methods are able to divide the number of darts
among the processes, becoming more and more efficient as the number of darts increases. 

I tested the results using variable numbers of processes (multiprocessing)/actions (IPcluster), 
and got the same results. Various other combinations tried: 2-20 processes, 1-10 actions.

#-------------------- System info --------------------
Developed for Mac OS X 10.6.8, 2.7 GHz Intel Core i7, Dual core 

