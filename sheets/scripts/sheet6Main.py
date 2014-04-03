import json

def Read(fn):
    fh = open(fn)
    data = fh.read()
    fh.close()
    return data

def LoadJSON(fn):
    return json.loads(Read(fn))

sheet1     = LoadJSON("data/sheet1.json")
sheet2     = LoadJSON("data/sheet2.json")

# hardcoded paper statuses 
CADIStatus = ["PUB (Published)", "SUB (Paper has been submitted to journal)", 
              "ReSubmitted (null)", "ACCEPT (Paper is accepted)", "RefComments"]

for i in sheet1:
    if sheet1[i]["status"] in CADIStatus:
        print sheet1[i]["status"], i
