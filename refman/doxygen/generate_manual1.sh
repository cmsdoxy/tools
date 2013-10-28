#!/bin/tcsh

cmsenv

set CMSSW_BASE = `echo $CMSSW_BASE`
set VER     = `echo $CMSSW_VERSION`
set SOURCE  = $CMSSW_BASE/src
set SCRIPTS = $CMSSW_BASE/src/Documentation/ReferenceManualScripts/doxygen/scripts
set DOXY    = $SCRIPTS/doxyfiles
set DOC     = $CMSSW_BASE/doc

if (-e $DOC) then
    rm -Rf $DOC
    mkdir $DOC
endif

rm $DOXY/configfile.conf

sed -e 's|@CMSSW_IN@|'$SOURCE'|g' -e 's|@CMSSW_OUT@|'$DOC'|g' -e 's|@DOXY_PATH@|'$DOXY'|g' $DOXY/configfile > $DOXY/configfile.conf

time doxygen $DOXY/configfile.conf

time python $SCRIPTS/MainPageGenerator/run.py $DOC/html/ index.html $VER
echo
time python $SCRIPTS/ClassNamespaceSplitter/run.py $DOC/html/ annotated.html annotatedList_
echo
time python $SCRIPTS/ConfigFiles/run.py $DOC/html/ configfiles.html
echo
time python $SCRIPTS/ClassNamespaceSplitter/run.py $DOC/html/ namespaces.html namespacesList_
echo
time python $SCRIPTS/PackageSplitter/run.py $DOC/html/ pages.html packageDocumentation_
