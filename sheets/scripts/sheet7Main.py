import json

def Read(fn):
    fh = open(fn)
    data = fh.read()
    fh.close()
    return data

def Write(fn, data):
    fh = open(fn, 'w')
    fh.write(data)
    fh.close()

def LoadJSON(fn):
    return json.loads(Read(fn))

def IsPublished(status):
    # hardcoded paper statuses
    s = ["SUB (Paper has been submitted to journal)",
         "ReSubmitted (null)", "RefComments (null)",
         "PUB (Published)", "ACCEPT (Paper is accepted)"]
    for i in s:
        if i in status: return 1
    return 0

def LoadNames(fn):
    csv   = Read(fn)
    lines = csv.split('\n')
    for line in lines:
        print line
    return []

def load_usa_lpc_authors_csv():
    usa_lpc_authors = {}
    f = open('data/LPCauthors-08April2014_fromLPCsurvey_mod.csv', 'r')
    lines = f.read().split("\n")
    for line in lines[1:]:
        columns = line.split("|")
        if len(columns) > 6:
            fname = columns[4].replace("\"", "").replace("'", "")
            name  = columns[3].replace("\"", "").replace("'", "")
            isLPC = False
            for i in range(5,7):  #lpc-fellows = 5, lpc-all = 6
                if columns[i]:
                    isLPC = True
                    break
            usa_lpc_authors[fname + " " + name] = isLPC
            usa_lpc_authors[name + " " + fname] = isLPC
    return usa_lpc_authors

# load cadi sheets
sheet1 = LoadJSON("data/sheet1.json")
USALPC = load_usa_lpc_authors_csv()

csv = "Code | # of authors | # of LPC authors | # of authors from USA \n"
for i in sheet1:
    entry = sheet1[i]

    if not IsPublished(entry['status']): continue

    chairperson = {}
    if entry['chairperson']: chairperson[entry['chairperson']['fullname']] = entry['chairperson']['country']
    numChairPerson = len(chairperson)

    cadiContact = {}
    if entry['cadi_contact']: cadiContact[entry['cadi_contact']['fullname']] = entry['cadi_contact']['country']
    numCadiContact = len(cadiContact)

    ARCMembers  = {}
    for j in entry['arc_members']:
        ARCMembers[j] = entry['arc_members'][j]['country']
    numARCMembers = len(ARCMembers)

    authors = {}
    authors.update(chairperson)
    authors.update(cadiContact)
    authors.update(ARCMembers)
    lpcAuthors = []
    for j in authors:
        if USALPC.has_key(j) and USALPC[j]: lpcAuthors.append(j)

    USAAuthors = []
    for j in authors:
        if authors[j] == 'USA': USAAuthors.append(i)

    csv = csv + ("%s | %s | %s | %s\n" % (i, len(authors), len(lpcAuthors), len(USAAuthors)))

Write('sheets/sheet7.csv', csv)
