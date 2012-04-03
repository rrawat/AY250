HW0README.txt

Created by Radhika Rawat for AY 250


------FILES-----
In HW0.zip, there are three files: HW0README.txt (this file), hw0.py, and population_[2012-01-29 16/13/53.927352].txt.

hw0.py is the program.

The population_[2012-01-29 16/13/53.927352].txt file is an example of the output from the program. Year-wise, it lists the bears that die, the bears that mate and the cubs they form, and the bears that do not mate, organized respectively.

--FUNCTIONALITY--

hw0.py can be run from the command line. It is set to create a text file and write the activities of a bear population over 150 years. In order to change the number of years of the simulation, change the value of the "end" variable in line 268 to any integer value greater than 0.

Bears are named according to their parents and their bear number in the population. This way, even bears with the same parents will have unique names, since each bear has a unique bear number. These names are only referenced in the first mention of the bear - when it is listed as the cub of a mating pair. After that, for the sake of conciseness, the bear is referenced by bear number. 

-There are extensive inline comments, which should clarify how the program works. 

-The general flow is as follows:
For each year(line 114), if there are bears in the population, the program determines the probability of each bear dying at its current age based on a cumulative density function. If the bear dies, its death is displayed, and it is excluded from mating.

-In order to determine mating eligibility(line 140), bear age is first tested(154), and bears are assigned to appropriate gender lists. For each female bear(186), the eligibility of males is then tested. Every male bear that does not have the same parents as the given female bear is assigned to a list(203), which is then randomly chosen from until a bear of age within 10 years of hers is found(207). Both bears mate(219), and the cub is returned. If there are no eligible males for a given female, she does not mate. Once all females have been tested, non-mating males and females are displayed.

-This process repeats each year until the "end" year has been reached.

