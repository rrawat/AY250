4-8-2012
HW8, AY250: Git, Argparse

Radhika Rawat

----

1. 

To clone the AY250 repository, move to the desired location in your interpreter, and then type 

git clone git@github.com:rrawat/AY250.git 

This will create a local clone in your active directory.

All homework files have been inserted into the repository.

2. A commit log for a separate programming project has been included: commit_log.txt

3. I edited the solutions to HW 5 and renamed the file "Homework_5_HW8_version.py" . It is in the directory Rawat_HW5/Rawat_HW5_2/Homework_5_Solutions. The candidate data are accessed from the text file: candidate_info.txt, instead of parsing wikipedia, for speed. When running Argparse.py, which is in the Rawat_HW8 directory, the relevant functions are imported from Homework_5_HW8_version.py, and as specified on lines 41 and 42 ofHomework_5_HW8_version.py, the path of the candidate_info text file and the candidate data are printed to make it easier to tell where the information came from. 

Inputs to argparse should be in the format:

run Argparse.py -c Candidate -d YYYY-MM-DD -p

where the -p argument is optional. Candidate name can either be entered as First, Last, or First_Last. Date must be entered as YYYY-MM-DD. -p indicates that a plot will be displayed showing the plot of the prediction probability for the given candidate over time. The specified date is highlighed in red. If -p is omitted, no plot will be displayed, but the closing value will still print.

If you enter a candidate who is not in the list or a date in an incorrect range, a helpful message will be shown without an error being thrown. 


