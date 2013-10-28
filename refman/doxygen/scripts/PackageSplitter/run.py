from PackageSplitter import *
import os, sys

if len(sys.argv) == 4:
    PATH = sys.argv[1]
    OUTF = sys.argv[2]
    PREF = sys.argv[3]
    
    l = PackageSplitter(PATH, PREF)
    
    l.CreatePackagePage(OUTF)
else:
    print "parameter error. It must be like this:\nrun.py PATH FILE PREFIX\nExample: run.py /doc/html/ pages.html packageDocumentation_"
