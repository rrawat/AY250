# Create your views here.

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.http import Http404   #page not found error(usage: raise Http404)
from models import *
from settings import SITE_ROOT
import os
from django.views.decorators.csrf import csrf_exempt
from bibparse import parse_bib

@csrf_exempt
def queryresults(request):
	"creates the query page, which takes an sql query and displays search results"
	
	try:
		querystr=str( request.GET['query'])
		results=[]
		for p in BibtexEntry.objects.raw(querystr):
			results.append(p)
	except:
		results=[]
	finally:
		return render_to_response(
			'queryresultspg.html', 				#template name
			{'resultlist': results}					#template variables, e.g.use 'poll' in template to refer to p
				)

@csrf_exempt
def bibtexprocessingfunction(request):
	"""takes in bibtex file, creates BibtexEntry instances with populated attributes"""
	try:
		collectionid=request.POST['collection']
		
		if collectionid == '': raise() #if no query given, cause no response
		c=Collections()
		c.name=collectionid
		c.save()
		
		print c
		
		bib= request.FILES['bibtexfile'].read()
		name='bibfile'
		f=open(name, 'w')
		f.write(bib)
		f.close()
		
		print bib
	
		for entry in parse_bib(name):
			bibent=BibtexEntry()
			print entry.data, "\n"
			for attribute in ['Author', 'Journal', 'Title', 'Keywords', 'Adsnote', 'Adsurl', 'Doi', 'Pages','Editor','Booktitle', 'Year']:
				try:
					setattr(bibent,attribute, entry.data[attribute])
				except:
					setattr(bibent,attribute, "")
				finally:
					pass
			
			try: #have to put Date_mod and Date_added into a new section because the parsed fields include dashes (not supported by py)
				bibent.Date_Modified= bibent.data['Date-Modified']
			except:
				pass
			finally:
				pass
			try:
				bibent.Date_Added= bibent.data['Date-Added']
			except:
				pass
			finally:
				pass
			
			bibent.Collection=c
			bibent.save()
	except:
		pass
	finally:
		pass	
	return HttpResponseRedirect(
		'/upload')



def upload(request):
	"""sends collection data objects to upload url"""
	collections=Collections.objects.all().order_by("-id")
	
	return render_to_response(
		'upload.html',
		{'collections':collections }
		)
