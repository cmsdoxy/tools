#!/bin/tcsh
set PATH = "/afs/cern.ch/work/a/aaltunda/public/www/doc/html/"

time python MPG/run.py $PATH index.html
echo
time python Class\ and\ Namespace\ Splitter/run.py $PATH annotated.html annotatedList_
echo
time python Config\ Files/run.py $PATH configfiles.html
echo
time python Class\ and\ Namespace\ Splitter/run.py $PATH namespaces.html namespacesList_ 
echo
time python Package\ Splitter/run.py $PATH pages.html packageDocumentation_
echo
