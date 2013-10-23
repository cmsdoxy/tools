#!/bin/tcsh

setenv CURRENT $PWD
set SOURCE = `python -c 'import os; p = os.environ["CURRENT"]; print os.path.split(os.path.split(os.path.split(p)[0])[0])[0]'`
set BASE   = `python -c 'import os; p = os.environ["CURRENT"]; print os.path.split(os.path.split(os.path.split(os.path.split(p)[0])[0])[0])[0]'`

if (-e $BASE/doc) then
    rm -Rf $BASE/doc
    mkdir $BASE/doc
endif

cd doxygen

sed -e 's|@CMSSW_IN@|'$SOURCE'|g' -e 's|@CMSSW_OUT@|'$BASE'|g' configfile > configfile.conf

chmod +rwx doxygen
./doxygen configfile.conf

time python $CURRENT/MainPageGenerator/run.py $BASE/doc/html/ index.html
echo
time python $CURRENT/ClassNamespaceSplitter/run.py $BASE/doc/html/ annotated.html annotatedList_
echo
time python $CURRENT/ConfigFiles/run.py $BASE/doc/html/ configfiles.html
echo
time python $CURRENT/ClassNamespaceSplitter/run.py $BASE/doc/html/ namespaces.html namespacesList_
echo
time python $CURRENT/PackageSplitter/run.py $BASE/doc/html/ pages.html packageDocumentation_
