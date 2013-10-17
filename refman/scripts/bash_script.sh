#!/bin/tcsh
set PATH = "/afs/cern.ch/work/a/aaltunda/public/www/doc/html/"

time python MainPageGenerator/run.py $PATH index.html
echo
time python ClassNamespaceSplitter/run.py $PATH annotated.html annotatedList_
echo
time python ConfigFiles/run.py $PATH configfiles.html
echo
time python ClassNamespaceSplitter/run.py $PATH namespaces.html namespacesList_ 
echo
time python PackageSplitter/run.py $PATH pages.html packageDocumentation_
echo
