from Splitter import *

if len(sys.argv) > 3:
    path = sys.argv[1]
    file = sys.argv[2]
    prefix = sys.argv[3]
    s = Splitter(path, file, prefix)
    print "pages are creating..."
    s.CreatePages()
else:
    print "Not enough parameters: file.py PATH FILE PREFIX"
    print "Example: python run.py /doc/html/ annotated.html annotated_"
