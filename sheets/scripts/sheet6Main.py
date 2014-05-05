import json, os
from BeautifulSoup import BeautifulSoup

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

def WriteJSON(fn, data):
    Write(fn, json.dumps(data, indent = 1))

def TableParser(fn):
    html  = Read(fn)
    soup  = BeautifulSoup(html)
    table = soup.find('table')
    thead = table.find('thead')
    tbody = table.find('tbody')
    heads = []
    # extract headers
    for th in thead.findAll('th'): heads.append(th.text)

    # table content will be pushed into data list
    data  = []

    # extract table content
    for tr in tbody.findAll('tr'):
        counter = 0
        row = {}
        for td in tr.findAll('td'):
            row[heads[counter]] = td.text
            counter += 1
        data.append(row)
    return data

def IsPhysicist(member):
    if member['ActivName'] == 'Physicist' and  member['Author'] == '1': return True
    return False

def IsGradStudent(member):
    if member['ActivName'] in ['Doctoral Student'] and member['StatusCMS'] == 'CMS': return True
    return False

def FindMember(memberName):
    for i in data:
        if '%(NameCMS)s %(NamfCMS)s' % i == memberName: return i
    return {}

def IsPublished(status):
    # hardcoded paper statuses
    s = ["SUB (Paper has been submitted to journal)",
         "ReSubmitted (null)", "RefComments (null)",
         "PUB (Published)", "ACCEPT (Paper is accepted)"]
    for i in s:
        if i in status: return 1
    return 0

def CheckDate(entry, format):
    if format == 'AN':
        entry = entry[len('CMS AN-'):entry.find('/')]
        entry = int(entry)
    elif format == 'CADI':
        if len(entry) == 0: return True
        entry = int(entry[0:4])
    elif format == 'CEntry':
        if entry == '' or entry == 'NONE': return False
        entry = int(entry)
    if not type(entry) == int: return False
    if entry >= 2012: return True
    return False

def load_usa_lpc_members_csv():
    usa_lpc_members = {}
    LPC = Read('data/LPCauthors-08April2014_fromLPCsurvey_mod.csv').split('\n')
    for line in LPC[1:]:
        columns = line.split("|")
        if len(columns) > 6:
            fname = columns[4].replace("\"", "").replace("'", "")
            name  = columns[3].replace("\"", "").replace("'", "")
            isLPC = False
            for i in range(5,7):  #lpc-fellows = 5, lpc-all = 6
                if columns[i]:
                    isLPC = True
                    break
            usa_lpc_members[fname + " " + name] = isLPC
            usa_lpc_members[name + " " + fname] = isLPC
    return usa_lpc_members

data = TableParser('data/authors/USA2.html')
# write members as json file
# WriteJSON('data/members.json', members)

# load ANs
sheet2     = LoadJSON("data/sheet2.json")

# load CADI papers
sheet1     = LoadJSON("data/sheet1.json")
USALPC     = load_usa_lpc_members_csv()

# collect members from USA by institutes
Members = {}
for member in data:
    if Members.has_key(member['InstCode']):
        Members[member['InstCode']].append(member)
    else:
        Members[member['InstCode']] = []
        Members[member['InstCode']].append(member)

# USA Institution statistics
Institutes = {}
GradStudents = {}
Physicist    = {}
for institute in Members:
    Institutes[institute] = {}
    numPhysicists         = 0
    numGradStudents       = 0
    # members list to calculate number of members
    membersList           = []
    GradStudents[institute] = []
    Physicist[institute]    = []
    for member in Members[institute]:
        fname = "%s %s" % (member['NamfCMS'], member['NameCMS'])
        if IsPhysicist(member) and not fname in Physicist[institute]: Physicist[institute].append(fname)
        if IsGradStudent(member) and not fname in GradStudents[institute]: GradStudents[institute].append(fname)
    Institutes[institute]['# of physicists'] = len(Physicist[institute])
    Institutes[institute]['# of grad students'] = len(GradStudents[institute])

# CADI SECTION
# CADI members from CADI page
CADIAuthors = {}
CADIEntries = {}
for i in Institutes.keys():
    Institutes[i]['# of CADI papers'] = 0
    Institutes[i]['# of CADI papers [2012 - )'] = 0
    CADIAuthors[i] = {}
    CADIEntries[i] = []
for paper in sheet1:
    cadiLine   = sheet1[paper]
    # skip the paper if it is not published
    if not IsPublished(cadiLine['status']): continue
    ANs        = cadiLine['notes']
    # precess all ANs for the paper
    for AN in ANs:
        for member in sheet2[AN]['authors']:
            member_ = sheet2[AN]['authors'][member]
            # skip the member if he/she is not from USA
            if member_['country'] != 'USA': continue
            # do not add the same member into the CADI member pool of the institute
            if not member in CADIAuthors[member_['institute']]:
                dict_ = FindMember(member)
                dict_['Paper'] = [paper]
                CADIAuthors[member_['institute']][member] = dict_
            else:
                CADIAuthors[member_['institute']][member]['Paper'].append(paper)
            if not paper in CADIEntries[member_['institute']]: CADIEntries[member_['institute']].append(paper)

for inst in CADIEntries:
    Institutes[inst]['# of CADI papers'] =  len(CADIEntries[inst])
    for paper in CADIEntries[inst]:
        if CheckDate(sheet1[paper]['date'], 'CEntry'):
            Institutes[inst]['# of CADI papers [2012 - )'] += 1

for inst in CADIAuthors:
    Institutes[inst]['# of CADI Authors [2012 - )'] = 0
    for author in CADIAuthors[inst]:
        author_ = CADIAuthors[inst][author]
        if not 'EXYear' in author_.keys():
            continue
        if CheckDate(author_['EXYear'], 'CADI'): Institutes[inst]['# of CADI Authors [2012 - )'] += 1

for i in Institutes.keys():
    Institutes[i]['# of CADI authors'] = len(CADIAuthors[i])
    Institutes[i]['# of CADI authors from LPC'] = 0
    for j in CADIAuthors[i]:
        if not (USALPC.has_key(j) and USALPC[j]): continue
        Institutes[i]['# of CADI authors from LPC'] += 1

# AN SECTION
for i in Institutes.keys():
    Institutes[i]['# of ANs'] = 0
    Institutes[i]['# of ANs [2012 - )'] = 0
for AN in sheet2:
    institutes = {}
    for member in sheet2[AN]['authors']:
        member_ = sheet2[AN]['authors'][member]
        if not member_['institute'] in institutes.keys(): institutes[member_['institute']] = AN
    for i in institutes:
        if not i in Institutes.keys(): continue
        Institutes[i]['# of ANs'] += 1
        if CheckDate(institutes[i], 'AN'):
            Institutes[i]['# of ANs [2012 - )'] += 1

csv = ""
#write institute statistics
if Institutes:
    sampleKey = Institutes.keys()[0]
    headers   = Institutes[sampleKey].keys()
    csv = "Institutes|" + "|".join(headers) + "\n"
    for i in Institutes:
        csv = csv + i
        for j in headers:
            csv = csv + "|%s" % (Institutes[i][j])
        csv = csv + "\n"
Write('sheets/sheet6.csv', csv)
