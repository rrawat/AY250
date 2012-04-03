README
Radhika Rawat
HW7, AY 250

http://127.0.0.1:8000/


This is a program that takes in a Bibtex file that the user uploads, in conjunction with a collection name that groups all bib entries in the Bibtex file and allows the user to query a database of Bibtex entries.

1. Uploading a Bibtex file
In views.bibtexprocessingfunction, the Bibtex file gets parsed by a program I downloaded from the internet called bibparse.py (http://bkarak.wizhut.com/www/programs/biblio-py/bibtex-py/index.html). The collection is shown at http://127.0.0.1:8000/upload, with a grey background. All collections are set to the default view where only the collection name is visible, so that multiple collections that are present can be seen easily. To see the files in the collection from the uploads page, click on the collection. Clicking causes a javascript toggle (upload.html) which then displays all of the entries in that collection with a light green background. Collections are sorted so that the most recent one is on top.

2. Querying the Database
From http://127.0.0.1:8000/queryresultspg, the user can enter an SQL query to search the database. Some examples are provided:
SELECT * FROM bibtex_BibtexEntry 
SELECT * FROM bibtex_BibtexEntry where Pages = "515-520"

The database is bibtex_BibtexEntry. The query is sent to views.queryresults, where all elements of the BibTexEntry class are searched. Results are returned to the html page and are shown in with a light green background.
 
**notes: 

-bibparse.py has some problems with finding the "year" field. However, I still put in the functionality, so that if another parser was used, it should show the "Year" field.
-any field that is not filled is shown as blank.