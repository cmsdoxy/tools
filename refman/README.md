
----------------

**This is how "Instructions how to build Reference Manual" should look like**

`cmsrel CMSSW_7_0_0_pre6`

`cd CMSSW_7_0_0_pre6`

`cmsenv`

`git cms-addpkg Documentation`

`generate_reference_manual` [1]

-----------------

[1] later we will do executable available in PATH

-----------------

**common** directory must be placed in `vocms12:/data/doxygen/common`



**TODO:**

checkout CMSSW_7_0_0_pre6 source 

generate doxygen(1.8.5) (and preferably make a clean backup)

put your scripts to **CMSSW_XYZ/src/Documentation/ReferenceManualScripts/your_new_directory/**

create **CMSSW_XYZ/src/Documentation/ReferenceManualScripts/your_new_directory/**
***your_generate_reference_manual_script.sh*** 

**MUST** use absolute paths everywhere in your scripts.

navigate to CMSSW_XYZ directory

launch ```./src/Documentation/ReferenceManualScripts/your_new_directory/your_generate_reference_manual_script.sh```

***Dark magic*** 

indexpage created, namespaces/classes/packageDocumentation splitted, etc...

**I want to see ```your_generate_reference_manual_script.sh``` at least working on 24th Oct**





