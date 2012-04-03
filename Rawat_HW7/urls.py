from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	# url(r'^$', 'HW7_Rawat.bibtex.views.home'),
	# url(r'^home$', 'HW7_Rawat.bibtex.views.home'),
	url(r'^$', 'HW7_Rawat.bibtex.views.upload'),
	url(r'^home$', 'HW7_Rawat.bibtex.views.upload'),
	url(r'^upload$', 'HW7_Rawat.bibtex.views.upload'),	
	url(r'^queryresultspg', 'HW7_Rawat.bibtex.views.queryresults'),	
	url(r'^bibtexprocessing$', 'HW7_Rawat.bibtex.views.bibtexprocessingfunction'),
	
    # Examples:
    # url(r'^$', 'HW7_Rawat.views.home', name='home'),
    # url(r'^HW7_Rawat/', include('HW7_Rawat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	
)