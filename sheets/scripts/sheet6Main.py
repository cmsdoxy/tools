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

def IsGradStudent(status):
    if status in ['Doctoral Student', 'Non-Doctoral Student']: return 1
    return 0

def IsPublished(status):
    # hardcoded paper statuses
    s = ["SUB (Paper has been submitted to journal)",
         "ReSubmitted (null)", "RefComments (null)",
         "PUB (Published)", "ACCEPT (Paper is accepted)"]
    for i in s:
        if i in status: return 1
    return 0

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

# collect members with their information
dir = 'data/authors/'
authors = {}
for i in os.listdir(dir):
    if not '.html' in i: continue
    data = TableParser(dir + i)
    # remove .html filename extension and then replace USA2 -> USA
    country = i.replace('.html', '').replace('2', '')
    # merge tables if country already exists (for USA and USA2 lists)
    if authors.has_key(country):
        for i in data:
            authors[country].append(i)
    else:
        authors[country] =  data
# write authors as json file
# WriteJSON('data/authors.json', authors)

# load ANs
sheet2     = LoadJSON("data/sheet2.json")

# load CADI papers
sheet1     = LoadJSON("data/sheet1.json")
USALPC     = load_usa_lpc_authors_csv()

# collect authors from USA by institutes
USAANAuthors = {}
for author in authors['USA']:
    if USAANAuthors.has_key(author['InstCode']):
        USAANAuthors[author['InstCode']].append(author)
    else:
        USAANAuthors[author['InstCode']] = []
        USAANAuthors[author['InstCode']].append(author)

# USA Institution statistics
Institutes = {}
for institute in USAANAuthors:
    Institutes[institute] = {}
    numPhysicists         = 0
    numGradStudents       = 0
    numAN                 = 0
    # authors list to calculate number of authors
    authorsList           = []
    for author in USAANAuthors[institute]:
        # count number of physicists
        if author['ActivName'] == 'Physicist': numPhysicists += 1
        # count number of grad students
        if IsGradStudent(author['ActivName']): numGradStudents += 1
    for an in sheet2:
        if sheet2[an]['institute'] == institute: numAN += 1
        for author in sheet2[an]['authors']:
            if sheet2[an]['authors'][author]['institute'] == institute and author not in authorsList:
                authorsList.append(author)
    Institutes[institute]['# of physicists'] = numPhysicists
    Institutes[institute]['# of grad students'] = numGradStudents
    Institutes[institute]['# of AN'] = numAN
    Institutes[institute]['# of AN authors'] = len(authorsList)

CADIUSAbyInstitute = {}
for i in sheet1:
    entry = sheet1[i]

    # only published papers
    if not IsPublished(entry['status']): continue

    chairperson = {}
    if entry['chairperson']: chairperson[entry['chairperson']['fullname']]   = {'country' : entry['chairperson']['country'],  'institute' : entry['chairperson']['institute']}

    cadiContact = {}
    if entry['cadi_contact']: cadiContact[entry['cadi_contact']['fullname']] = {'country' : entry['cadi_contact']['country'], 'institute' : entry['cadi_contact']['institute']}

    ARCMembers  = entry['arc_members']

    authors = {}
    authors.update(chairperson)
    authors.update(cadiContact)
    authors.update(ARCMembers)

    for fname in authors:
        info = authors[fname]
        if not CADIUSAbyInstitute.has_key(info['institute']): CADIUSAbyInstitute[info['institute']] = {}
        CADIUSAbyInstitute[info['institute']][fname] = info

for institute in Institutes:
    if not CADIUSAbyInstitute.has_key(institute):
        Institutes[institute]['# of CADI authors'] = 0
        Institutes[institute]['# of CADI authors from USA'] = 0
        Institutes[institute]['# of CADI authors from LPC'] = 0
        continue

    Institutes[institute]['# of CADI authors'] = len(CADIUSAbyInstitute[institute])

    numCADIUSA = 0
    for i in CADIUSAbyInstitute[institute]:
        if CADIUSAbyInstitute[institute][i]['country'] == 'USA':
            numCADIUSA = numCADIUSA + 1
    Institutes[institute]['# of CADI authors from USA'] = numCADIUSA

    numCADILPC = 0
    for i in authors:
        if USALPC.has_key(i) and USALPC[i]: numCADILPC = numCADILPC + 1
    Institutes[institute]['# of CADI authors from LPC'] = numCADILPC

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
