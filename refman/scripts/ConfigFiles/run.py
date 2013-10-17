from ConfigFiles import *
import sys

if len(sys.argv) == 3:
    PATH = sys.argv[1]
    OUTF = sys.argv[2]
    
    l = ConfigFiles(PATH, OUTF)
    
    l.CreateConfigFilePage()
else:
    print "parameter error. It must be like this: run.py /doc/html/ output.html"
