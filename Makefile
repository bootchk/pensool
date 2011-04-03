
# No compiling, but clean, etc.

clean :
	find . -name *.pyc -exec rm {} +
	find . -name *.py~ -exec rm {} +
	

# make programmer's docs from source submodule into the doc directory
# ??? works better if cd to source first
# Formatting in docstrings is ReST, at least in has fewer warnings than epytext format
docs : 
	cd source
	epydoc --verbose --graph all ../source/ --output ../doc/html --docformat restructuredtext
	cd ../doc
	rst2html UserManual.txt UserManual.html


