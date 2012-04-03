import datetime
import random
import numpy
from scipy.stats import norm
t= str( datetime.datetime.now())
f= open("population_[%s].txt" %(t), "w")

###############################################################################


class Bear:
	bear_num = 0    					# Bear Num is the total number of bears that have ever lived
	current_bear_num = 0				# Current bear num is not unique to each bear, it is more like a current count of bears in population
	bear_list=[]						# contains living bears
	male=[]								# living male bears
	female=[]							# living female bears
	
	def __init__ (self,name) :
		"""
		create a bear instance
		"""
		self.name = name
		self.my_num = Bear.bear_num
		
		Bear.bear_list.append(self)   #all bears that were ever created
		self.age=0
		Bear.bear_num +=1
		Bear.current_bear_num +=1
		self.gender=bool(random.getrandbits(1))
		
		self.cub_num=0
		self.lastcub=0
		self.lifespan = int( numpy.random.normal(35,5) )
		f.write("Made bear #%i (%s) \n \n" %(self.my_num,self.name))
		
	def __del__(self):
		"""
		delete bear instance
		"""
		
		if len(Bear.bear_list)>0:
			if self in Bear.bear_list:
				Bear.bear_list.remove(self)
		if len(Bear.male)>0 and self.gender==False:
			if self in Bear.male:
				Bear.male.remove(self)
		elif len(Bear.female)>0 and self.gender==True:
			if self in Bear.female:
				Bear.female.remove(self)
		

        
	def __str__(self):
		"""
		#print bear name
		"""
		f.write( "name = [%s] (age %s) my_number = [%i] (/ pop= %i) gender = [%s] #of cubs = %i, last cub born %i years ago \n" % (self.name, self.age, self.my_num,Bear.bear_num,self.gender,self.cub_num,self.lastcub))
		
	def __add__(self,other):
		"""
		 create offspring
		"""
		cub_name = "ChildOf_%i_%i_%i" % (self.my_num, other.my_num, Bear.bear_num) #the bear_num ensures each bear has a unique name
		cub = Bear(cub_name)
		cub.parents = (self,other)
		self.cub_num +=1
		other.cub_num +=1
		#f.write( "Bear #%i was born to Bear #%i and Bear #%i \n" %(cub.my_num,self.my_num,other.my_num))
		
		#return cub
	
	def death(self):
		"""
		kill a bear
		"""
		Bear.bear_list.remove(self)
		f.write("Bear %s (%s, age=%i) died \n" % (self.my_num, self.name, self.age))
		Bear.current_bear_num -= 1
	
	def gender_check(self):
		"""
		assign bear to appropriate gender list
		"""
		if self.gender ==True:
			Bear.female.append(self)
		else:
			Bear.male.append(self)	
		
	
######################################################################

																										

f.write( "Bear Colony, started with Adam, Eve, and Mary \n")


one=Bear("Adam"); two=Bear("Eve"); three=Bear("Mary")														#initial seeds

one.parents=('seed1','seed2');two.parents=('seed3','seed4');three.parents=('seed5','seed6')
																											#gender
one.gender=bool(0); two.gender=bool(1); three.gender=bool(1)
																											#add to appropriate gender list
one.gender_check(); two.gender_check(); three.gender_check();

one.age=-1; two.age=-1; three.age=-1																		#set pre-program age
																											#set number of offspring to 0
one.cub_num=0; two.cub_num=0; three.cub_num=0

f.write('\n')

########################################################################
#year 1

def year(n,end):
	"""
	run the nth year of mating, birth, and death activity in the population
	"""
	f.write( "\n \n \n YEAR %i \n \n \n" %n)
		
	if len(Bear.bear_list) >0:															 
		f.write( "\n -------DEATHS------ \n")
		#deaths:
		for a in Bear.bear_list:
													
			
																									
			if a.age > a.lifespan:									
											
				Bear.death(a)															
				del(a)
			else:	
				a.age +=1
		
	
	
				
	###############

	
	def mating():
		"""
		mate elibigle bears
		"""
		f.write( "\n -------MATING------ \n")
		
		mated=[]
		mating_females=[]
		mating_males=[]
		non_mating_females=[]
		non_mating_males=[]
		
		list=[]
		
		for a in Bear.bear_list:														#check bear age and years since last cub-->append to mating lists
			if a.age>=5 and a.gender==True and a.lastcub>=5: 
				mating_females.append(a)
				
			elif a.age>=5 and a.gender==False and a.lastcub>=5: 
				mating_males.append(a)
			else:
				if a.gender==True:
					non_mating_females.append(a)
				else:
					non_mating_males.append(a)
				
		if len(mating_females) > 0 and len(mating_males) >0:

			def next_element(male,male_list,orig_index):
				"""
				generic function to return the next element of a list
				"""
				
				i0=orig_index
				index0=male_list.index(male)
				if index0==i0:
					return 0
				else:
					if index0==len(male_list)-1:
						index1=-1
					else:
						index1=index0+1
					return male_list[index1]
			
			###############
			
			def choose_mate(female_list,male_list):
				"""
				identify a suitable mate for every female in the population based on parents and age. If there is one, they mate. If there are no eligible males for a given female, the female is marked as nonmating, and the male is allowed to be processed for any other eligible female. Any males that do not mate are then marked as nonmating.
				"""
				non_mating_males=[]
				non_mating_females=[]
				if len(female_list)==0:											#if eligible female list length is 0, exit.
					return
				for a in female_list: 											#go through the female bears over 5 years old
					if len(male_list)>0: 										#if there are multiple male bears over 5 years old
						 														#take the whole list of bears
						non_sib_males=[]
						for b in male_list:
							if b not in mated:			#identify the ones that don't have the same parents and put them in a new list
								if a.parents==b.parents:
									filler=[]
								else:
									non_sib_males.append(b)
					else:														#if there aren't any, mark the female as nonmating, this year.
						non_mating_females.append(a)
																			
					if len(non_sib_males)>0 :									#if there were non sibling male bears for the female bear, test their age range.
						b = random.choice(non_sib_males) 							#choose a random male bear
						i0 = non_sib_males.index(b) 								#mark that male bear's index
						if a.age-b.age>10 or b.age-a.age>10: 					#if their ages are more than 10 years apard, take the next bear in the eligible list
							potential_male = next_element(b,non_sib_males,i0) 
							if potential_male==0:								#if it's the same bear, move just the female bear into the nonmating list
								non_mating_females.append(a)					#this doesn't actually impact the function. It just keeps track of the females that didn't mate. This is not done for the males in this program.
	
						elif a.age-b.age<=10 or b.age-a.age<=10: 				#if the non-sibling bears are within 10 years of age, mate them
							f.write( "Bear #%i(%s) mated with Bear #%i(%s) \n" %(a.my_num, a.name ,b.my_num, b.name))#, (%s, age=%i)b.name,b.age) )
							
							#make a new cub, 'c' b/c father_bear + mother_bear -> new cub
							c=a+b												
							
							# reset years since last cub to 0
							a.lastcub=0
							b.lastcub=0
																				#increase cub count by 1
							a.cub_num+=1
							b.cub_num+=1										
							#f.write( c )										#print cub details
							mated.append(a)										#mark both parents as having mated
							mated.append(b)
							if b in male_list:
								male_list.remove(b)
								non_sib_males.remove(b)
							if a in female_list:
								female_list.remove(a)
							

			choose_mate(mating_females,mating_males)
		f.write( "\n --NONMATING BEARS-- \n")
		for a in Bear.bear_list:												#for any nonmated bears, print that they didn't mate this year
			if a not in mated:
				f.write("Bear #%i %s (age=%i) did not mate in year %i \n" %(a.my_num, a.name,a.age, n))
				a.lastcub+=1

	
	###############
	
	
	mating()
	
	###############
	
	if len(Bear.bear_list) >0:													#If there are still more bears, keep running the program until 														the end year. If not, print that there are no more bears left, and exit the program.
		if n<end:
			n+=1
			year(n,end)
		else:
			f.write( '\n \n %i years have now passed.' %end)
			return
	else:
		f.write( "no more bears")
		return
	return
	
	###############	
		
########################################################################
	
end=150																			#end year is set to 150
year(0,end)																		#run year program
f.close()
