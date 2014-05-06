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

def IsGradStudent2(member):
    if member['ActivName'] in ['Doctoral Student']: return True

def GetLPC(arr):
    l = []
    for i in arr:
        if IsLPC(i): l.append(i)
    return l

def GetPhysicists(arr):
    l = []
    for i in arr:
        if IsPhysicist(i): l.append(i)
    return l

def GetGradStudents(arr):
    l = []
    for i in arr:
        if IsGradStudent2(i): l.append(i)
    return l

def Get2012(arr):
    l = []
    for i in arr:
        if CheckDate(i['EXYear'], 'EXY'): l.append(i)
    return l

# Flintstone style coding (we didn't have enough time to keep it siple and stupid)
def FixName(name):
    if name == 'Smith Wesley': return 'Smith Wesley H.'
    elif name == 'Harris Robert': return 'Harris Robert M.'
    elif name == 'Bhat Pushpalatha': return 'Bhat Pushpalatha C.'
    elif name == 'Ulmer Keith Arthur': return 'Ulmer Keith'
    elif name == 'Albrow Michael Glen': return 'Albrow Michael'
    elif name == 'Fisher Matthew Ira': return 'Fisher Matthew'
    elif name == 'Hill Christopher Scott': return 'Hill Christopher'
    elif name == 'Breto Rangel Guillermo': return 'Breto Guillermo'
    elif name == 'Duarte Javier Mauricio': return 'Duarte Javier'
    elif name == 'Tonjes Marguerite Belt': return 'Tonjes Marguerite'
    elif name == 'Hidas Dean Andrew': return 'Hidas Dean'
    elif name == 'Cervantes Valdovinos Mayra Daniela': return 'Cervantes Mayra'
    elif name == 'Cepeda Maria Luisa': return 'Cepeda Maria'
    elif name == 'Gray Richard Carl': return 'Gray Richard'
    elif name == 'Baumgartel Darin Carl': return 'Baumgartel Darin'
    elif name == 'Tran Nhan': return 'Tran Nhan Viet'
    elif name == 'Rosenfield Matthew': return 'Rosenfield Matt'
    elif name == 'Newman Harvey': return 'Newman Harvey B.'
    elif name == 'Keller Jason Daniel': return 'Keller Jason'
    elif name == 'Jenkins Charles Merrill': return 'Jenkins Merrill'
    elif name == 'Winer Brian': return 'Winer Brian L.'
    elif name == 'Branson James': return 'Branson James G.'
    elif name == 'Hirschauer James Francis': return 'Hirschauer James'
    elif name == 'Ellison John': return 'Ellison John Anthony'
    elif name == 'Zenz Seth': return 'Zenz Seth Conrad'
    elif name == 'Valuev Viatcheslav': return 'Valuev Vyacheslav'
    elif name == 'Chauhan Sushil Singh': return 'Chauhan Sushil'
    elif name == 'Yoo Hwidong': return 'Yoo Hwi Dong'
    elif name == 'Roe Jeffrey Kyle': return 'Roe Jeffrey'
    elif name == 'Lawson Philip Daniel': return 'Lawson Philip'
    elif name == 'Dasu Sridhara Rao': return 'Dasu Sridhara'
    elif name == 'Kenny Raymond Patrick': return 'Kenny III Raymond Patrick'
    elif name == 'Gomez Jaime Arturo': return 'Gomez Jaime'
    elif name == 'Abdoulline Salavat': return 'Abdullin Salava'
    elif name == 'Gulhan Doga Can': return 'Gulhan Doga'
    elif name == 'Padley Paul': return 'Padley Brain Paul'
    elif name == 'Evans David Lewis': return 'Evans David'
    elif name == 'Edwards-bruner Christopher Ryan': return 'Bruner Christopher'
    elif name == 'Wuerthwein Frank Karl': return 'Wuerthwein Frank'
    return name

def FindMember(memberName):
    memberName = FixName(memberName)
    for i in data:
        if '%(NameCMS)s %(NamfCMS)s' % i == memberName: return i
        elif '%(NamfCMS)s %(NameCMS)s' % i == memberName: return i
    return {}

def IsPublished(status):
    # hardcoded paper statuses
    s = ["SUB (Paper has been submitted to journal)",
         "ReSubmitted (null)", "RefComments (null)",
         "PUB (Published)", "ACCEPT (Paper is accepted)"]
    for i in s:
        if i in status: return 1
    return 0

def IsLPC(member):
    name = "%s %s" % (member['NamfCMS'], member['NameCMS'])
    if USALPC.has_key(name) and USALPC[name]: return True
    return False

def CheckDate(entry, format):
    if format == 'AN':
        entry = entry[len('CMS AN-'):entry.find('/')]
        entry = int(entry)
    elif format == 'EXY':
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

# load ANs
sheet2     = LoadJSON("data/sheet2.json")

# load CADI papers
sheet1     = LoadJSON("data/sheet1.json")
USALPC     = load_usa_lpc_members_csv()
Sheet      = {}

# add all USA institutes
for row in data:
    if not row['InstCode'] in Sheet: Sheet[row['InstCode']] = {}

# find all physicists & grad students
Physicists = {}
Grads = {}
GP    = {}
for inst in Sheet:
    Physicists[inst] = []
    Grads[inst] = []
    GP[inst]    = []
for row in data:
    if IsPhysicist(row) and not row in Physicists[row['InstCode']]: Physicists[row['InstCode']].append(row)
    if IsGradStudent(row) and not row in Grads[row['InstCode']]:    Grads[row['InstCode']].append(row)
    if (IsPhysicist(row) or IsGradStudent(row)) and not row in GP[row['InstCode']]: GP[row['InstCode']].append(row)
# count them
for inst in Sheet:
    Sheet[inst]['# of physicists'] = len(Physicists[inst])
    Sheet[inst]['# of physicists from LPC'] = len(GetLPC(Physicists[inst]))
    Sheet[inst]['# of grad students'] = len(Grads[inst])
    Sheet[inst]['# of grad students from LPC'] = len(GetLPC(Grads[inst]))
    Sheet[inst]['USCMS (grads & physicisits)'] = len(GP[inst])

# CADI columns
CADIEntries = {}
CADIAuthors = {}
for inst in Sheet:
    CADIEntries[inst] = []
    CADIAuthors[inst] = []
for CADIEntry in sheet1:
    # skip the paper if it is not published
    if not IsPublished(sheet1[CADIEntry]['status']): continue
    for AN in sheet1[CADIEntry]['notes']:
        ANInfo = sheet2[AN]
        for author in ANInfo['authors']:
            auth = FindMember(author)
            if ANInfo['authors'][author]['country'] != 'USA': continue
            if not auth:
                print 'Warning: "%s" not found! Task dump: CADI -> %s -> %s' % (author, CADIEntry, AN); continue
            if not auth      in CADIAuthors[auth['InstCode']] and (IsGradStudent2(auth) or IsPhysicist(auth)):
                CADIAuthors[auth['InstCode']].append(auth)
            if not CADIEntry in CADIEntries[auth['InstCode']] and (IsGradStudent2(auth) or IsPhysicist(auth)):
                CADIEntries[auth['InstCode']].append(CADIEntry)
for inst in Sheet:
    Sheet[inst]['# of CADI entries'] = len(CADIEntries[inst])
    Sheet[inst]['# of CADI entries [2012 - )'] = 0
    for entry in CADIEntries[inst]:
        if CheckDate(sheet1[entry]['date'], 'CEntry'): Sheet[inst]['# of CADI entries [2012 - )'] += 1

    Sheet[inst]['# of CADI authors'] = len(CADIAuthors[inst])
    Sheet[inst]['# of CADI authors PHY'] = len(GetPhysicists(CADIAuthors[inst]))
    Sheet[inst]['# of CADI authors GRAD'] = len(GetGradStudents(CADIAuthors[inst]))

    Sheet[inst]['# of CADI authors [2012 - )'] = len(Get2012(CADIAuthors[inst]))
    Sheet[inst]['# of CADI authors [2012 - ) PHY'] = len(GetPhysicists(Get2012(CADIAuthors[inst])))
    Sheet[inst]['# of CADI authors [2012 - ) GRAD'] = len(GetGradStudents(Get2012(CADIAuthors[inst])))

    Sheet[inst]['# of CADI authors from LPC'] = len(GetLPC(CADIAuthors[inst]))
    Sheet[inst]['# of CADI authors from LPC PHY'] = len(GetPhysicists(GetLPC(CADIAuthors[inst])))
    Sheet[inst]['# of CADI authors from LPC GRAD'] = len(GetGradStudents(GetLPC(CADIAuthors[inst])))

    Sheet[inst]['# of CADI authors from LPC [2012 - )'] = len(Get2012(GetLPC(CADIAuthors[inst])))
    Sheet[inst]['# of CADI authors from LPC [2012 - ) PHY'] = len(GetPhysicists(Get2012(GetLPC(CADIAuthors[inst]))))
    Sheet[inst]['# of CADI authors from LPC [2012 - ) GRAD'] = len(GetGradStudents(Get2012(GetLPC(CADIAuthors[inst]))))

# AN columns
ANs       = {}
ANAuthors = {}
for inst in Sheet:
    ANs[inst]              = []
    ANAuthors[inst]        = []
for AN in sheet2:
    ANInfo = sheet2[AN]
    for author in ANInfo['authors']:
        if ANInfo['authors'][author]['country'] != 'USA': continue
        auth = FindMember(author)
        if not auth:
            print 'Warning: "%s" not found! Task dump: AN -> %s' % (author, AN); continue
        if not auth in ANAuthors[auth['InstCode']] and (IsGradStudent2(auth) or IsPhysicist(auth)): ANAuthors[auth['InstCode']].append(auth)
        if not AN   in ANs[auth['InstCode']] and (IsGradStudent2(auth) or IsPhysicist(auth)): ANs[auth['InstCode']].append(AN)
for inst in Sheet:
    Sheet[inst]['# of ANs'] = len(ANs[inst])
    Sheet[inst]['# of ANs [2012 - )'] = 0
    for AN in ANs[inst]:
        if CheckDate(AN, 'AN'): Sheet[inst]['# of ANs [2012 - )'] += 1

    Sheet[inst]['# of AN Authors'] = len(ANAuthors[inst])
    Sheet[inst]['# of AN Authors PHY'] = len(GetPhysicists(ANAuthors[inst]))
    Sheet[inst]['# of AN Authors GRAD'] = len(GetGradStudents((ANAuthors[inst])))


    Sheet[inst]['# of AN Authors [2012 - )'] = len(Get2012(ANAuthors[inst]))
    Sheet[inst]['# of AN Authors [2012 - ) PHY'] = len(GetPhysicists(Get2012(ANAuthors[inst])))
    Sheet[inst]['# of AN Authors [2012 - ) GRAD'] = len(GetGradStudents(Get2012(ANAuthors[inst])))

    Sheet[inst]['# of AN Authors from LPC']  = len(GetLPC(ANAuthors[inst]))
    Sheet[inst]['# of AN Authors from LPC PHY']  = len(GetLPC(GetPhysicists(ANAuthors[inst])))
    Sheet[inst]['# of AN Authors from LPC GRAD']  = len(GetLPC(GetGradStudents(ANAuthors[inst])))

    Sheet[inst]['# of AN Authors from LPC [2012 - )']  = len(Get2012(GetLPC(ANAuthors[inst])))
    Sheet[inst]['# of AN Authors from LPC [2012 - ) PHY']  = len(Get2012(GetPhysicists(GetLPC(ANAuthors[inst]))))
    Sheet[inst]['# of AN Authors from LPC [2012 - ) GRAD']  = len(Get2012(GetGradStudents(GetLPC(ANAuthors[inst]))))

# CADI & ARC -special section-
CADIPool       = []
ARCPool        = []
LPCANCARC      = {} #  LPC authors have not contributed to any ARC
LPCANCCADI     = {} #  LPC authors have not contributed to any CADI
for CADIEntry in sheet1:
    if not IsPublished(sheet1[CADIEntry]['status']): continue
    Entry = sheet1[CADIEntry]
    ARCMembers = Entry['arc_members']
    if 'country' in Entry['chairperson'].keys():
        ARCMembers[Entry['chairperson']['fullname']] = {'country' : Entry['chairperson']['country'], 'institute' : Entry['chairperson']['institute']}
    # CADI Line -> ARC
    for arc in ARCMembers:
        if Entry['arc_members'][arc]['country'] != 'USA': continue
        ARCInfo = FindMember(arc)
        if not ARCInfo:
            print 'Warning: "%s" not found! Task dump: ARC/CADI (ARC side) Pool -> %s' % (arc, CADIEntry); continue
        if not ARCInfo in ARCPool: ARCPool.append(ARCInfo)
    # CADI Line -> Notes
    for AN in Entry['notes']:
        ANInfo = sheet2[AN]
        for author in ANInfo['authors']:
            auth = FindMember(author)
            if ANInfo['authors'][author]['country'] != 'USA': continue
            if not auth:
                print 'Warning: "%s" not found! Task dump: ARC/CADI (CADI side) -> %s -> %s' % (author, CADIEntry, AN); continue
            if not auth in CADIPool: CADIPool.append(auth)
for inst in Sheet.keys():
    CADI = GetLPC(Get2012(CADIAuthors[inst]))
    AN   = GetLPC(Get2012(ANAuthors[inst]))
    LPCANCARC[inst] = []
    LPCANCCADI[inst] = []
    for CA in CADI:
        if not CA in ARCPool and not CA in LPCANCARC[inst]: LPCANCARC[inst].append(CA)
        if not CA in CADIPool and not CA in LPCANCCADI[inst]: LPCANCCADI[inst].append(CA)
    for AA in AN:
        if not AA in ARCPool and not AA in LPCANCARC[inst]: LPCANCARC[inst].append(AA)
        if not AA in CADIPool and not AA in LPCANCCADI[inst]: LPCANCCADI[inst].append(AA)
for inst in LPCANCARC:
    ARCNames = ''
    for i in LPCANCARC[inst]:
        ARCNames = ARCNames + '%s %s, ' % (i['NamfCMS'], i['NameCMS'])
    if not ARCNames: ARCNames = '-'
    else: ARCNames = ARCNames[0:len(ARCNames)]

    CADINames = ''
    for i in LPCANCCADI[inst]:
        CADINames = CADINames + '%s %s, ' % (i['NamfCMS'], i['NameCMS'])
    if not CADINames: CADINames = '-'
    else: CADINames = CADINames[0:len(CADINames)]

    Sheet[inst]['# of Authors have not contributed any ARCs'] = len(LPCANCARC[inst])
    Sheet[inst]['# of Authors have not contributed any ARCs PHY'] = len(GetPhysicists(LPCANCARC[inst]))
    Sheet[inst]['# of Authors have not contributed any ARCs GRAD'] = len(GetGradStudents(LPCANCARC[inst]))

    Sheet[inst]['# of Authors have not contributed any CADI entries'] = len(LPCANCCADI[inst])
    Sheet[inst]['# of Authors have not contributed any CADI entries PHY'] = len(GetPhysicists(LPCANCCADI[inst]))
    Sheet[inst]['# of Authors have not contributed any CADI entries GRAD'] = len(GetGradStudents(LPCANCCADI[inst]))
    Sheet[inst]['Name List ARCs'] = ARCNames
    Sheet[inst]['Name List CADI entries'] = CADINames

csv = ""
# write sheet 6
if Sheet:
    instList = Sheet.keys()
    instList.sort()
    headers  = ["# of physicists", "# of physicists from LPC", "# of grad students", "# of grad students from LPC", "USCMS (grads & physicisits)",
                "# of CADI entries", "# of CADI entries [2012 - )", 
                "# of CADI authors", "# of CADI authors PHY", "# of CADI authors GRAD",
                "# of CADI authors from LPC", "# of CADI authors from LPC PHY", "# of CADI authors from LPC GRAD",
                "# of CADI authors [2012 - )", "# of CADI authors [2012 - ) PHY", "# of CADI authors [2012 - ) GRAD",
                "# of CADI authors from LPC [2012 - )", "# of CADI authors from LPC [2012 - ) PHY", "# of CADI authors from LPC [2012 - ) GRAD",
                "# of ANs",          "# of ANs [2012 - )",
                "# of AN Authors", "# of AN Authors PHY", "# of AN Authors GRAD",
                "# of AN Authors from LPC", "# of AN Authors from LPC PHY", "# of AN Authors from LPC GRAD",
                "# of AN Authors [2012 - )", "# of AN Authors [2012 - ) PHY", "# of AN Authors [2012 - ) GRAD",
                "# of AN Authors from LPC [2012 - )", "# of AN Authors from LPC [2012 - ) PHY", "# of AN Authors from LPC [2012 - ) GRAD",
                "# of Authors have not contributed any ARCs", "# of Authors have not contributed any ARCs PHY", "# of Authors have not contributed any ARCs GRAD",
                "# of Authors have not contributed any CADI entries", "# of Authors have not contributed any CADI entries PHY", "# of Authors have not contributed any CADI entries GRAD",
                "Name List ARCs", "Name List CADI entries"]
    csv = "Institutes|" + "|".join(headers) + "\n"
    for i in instList:
        csv = csv + i
        for j in headers:
            csv = csv + "|%s" % (Sheet[i][j])
        csv = csv + "\n"
Write('sheets/sheet6.csv', csv)
