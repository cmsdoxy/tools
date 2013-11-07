#!/bin/tcsh

cmsenv

set CMSSW_BASE = `echo $CMSSW_BASE`
set VER     = `echo $CMSSW_VERSION`
set SOURCE  = $CMSSW_BASE/src
set SCRIPTS = $CMSSW_BASE/src/Documentation/ReferenceManualScripts/doxygen/scripts
set DOXY    = $CMSSW_BASE/src/Documentation/ReferenceManualScripts/doxygen/doxyfiles
set DOC     = $CMSSW_BASE/doc

if (-e $DOC) then
    rm -Rf $DOC
    mkdir $DOC
endif

rm $DOXY/configfile.conf

sed -e 's|@CMSSW_IN@|'$SOURCE'|g' -e 's|@CMSSW_OUT@|'$DOC'|g' -e 's|@DOXY_PATH@|'$DOXY'|g' $DOXY/configfile > $DOXY/configfile.conf

time doxygen $DOXY/configfile.conf

time python $SCRIPTS/MainPageGenerator.py $DOC/html/ index.html $VER
echo
time python $SCRIPTS/Splitter.py $DOC/html/ annotated.html annotatedList_
echo
time python $SCRIPTS/ConfigFiles.py $DOC/html/ configfiles.html
echo
time python $SCRIPTS/Splitter.py $DOC/html/ namespaces.html namespacesList_
echo
time python $SCRIPTS/PackageSplitter.py $DOC/html/ pages.html packageDocumentation_
