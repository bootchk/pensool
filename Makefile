
# No compiling, but clean, etc.
# Note need tabs as separators, not indented spaces

clean :
	echo cleaning up in $PWD
	find . -name *.pyc -exec rm {} +
	find . -name *.py~ -exec rm {} +
	

# make programmer's docs from source submodule into the doc directory
# ??? works better if cd to source first
# Formatting in docstrings is ReST, at least in has fewer warnings than epytext format
docs :
	echo Making docs/html and UserManual.html
	cd source; epydoc --verbose --graph all --output ../doc/html --docformat restructuredtext ../source/
	cd doc; rst2html UserManual.txt UserManual.html


