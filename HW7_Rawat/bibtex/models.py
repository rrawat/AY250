from django.db import models
from django import forms
# Create your models here.

class Car(models.Model):
    manufacturer = models.CharField(max_length=250)

class UploadFileForm(forms.Form):
	"""Uploads the .bib file"""
	title = forms.CharField(max_length=50)
	file=forms.FileField() # file  = forms.FileField()

class Collections(models.Model):
	"""stores the names of all collections"""
	name=models.CharField(max_length=50)


	
class BibtexEntry(models.Model):
	"""bibtex info for each entry in the .bib file"""
	Adsnote = models.CharField(max_length=500,null=True)					#{Provided by the SAO/NASA Astrophysics Data System}	
	Adsurl = models.CharField(max_length=500,null=True) 	#{http://adsabs.harvard.edu/abs/1998A%26A...330..515F},
	Author = models.CharField(max_length=500,null=True)
	Date_Modified = models.CharField(max_length=500,null=True)
	Date_Added = models.CharField(max_length=500,null=True)					#{2010-03-30 13:55:36 -0700},
	Journal =models.CharField(max_length=500,null=True) 		#{\aap},
	Keywords = models.CharField(max_length=500,null=True)		#{STARS: VARIABLES: RR LYRAES, GALAXY: GLOBULAR CLUSTERS, GALAXIES: MAGELLANIC CLOUDS},
	Month = models.CharField(max_length=500,null=True) 		#feb,
	Pages = models.CharField(max_length=500,null=True)			#{515-520},
	Title = models.CharField(max_length=500,null=True)		#{{The absolute magnitudes of RR Lyraes from HIPPARCOS parallaxes and proper motions}},
	Volume =models.CharField(max_length=500,null=True)	#330,
	Year = models.CharField(max_length=500,null=True)		#1998,
	Editor = models.CharField(max_length=500,null=True)
	Booktitle = models.CharField(max_length=500,null=True)
	Doi = models.CharField(max_length=500,null=True)
	Collection = models.ForeignKey(Collections, related_name='entries')
	
	
	
