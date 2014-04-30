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
USAAuthors = {}
for author in authors['USA']:
    if USAAuthors.has_key(author['InstCode']):
        USAAuthors[author['InstCode']].append(author)
    else:
        USAAuthors[author['InstCode']] = []
        USAAuthors[author['InstCode']].append(author)

# USA Institution statistics
Institutes = {}
GradStudents = {}
for institute in USAAuthors:
    Institutes[institute] = {}
    numPhysicists         = 0
    numGradStudents       = 0
    # authors list to calculate number of authors
    authorsList           = []
    GradStudents[institute] = []
    for author in USAAuthors[institute]:
        # count number of physicists
        if author['ActivName'] == 'Physicist': numPhysicists += 1
        # count number of grad students
        if IsGradStudent(author['ActivName']):
            fname = "%s %s" % (author['NamfCMS'], author['NameCMS'])
            if not fname in GradStudents[institute]: GradStudents[institute].append(fname)
    Institutes[institute]['# of physicists'] = numPhysicists
    Institutes[institute]['# of grad students'] = len(GradStudents[institute])

# CADI SECTION
# CADI authors from CADI page
CADIAuthors = {}
for i in Institutes.keys():
    Institutes[i]['# of CADI papers'] = 0
    CADIAuthors[i] = []
for paper in sheet1:
    cadiLine   = sheet1[paper]
    # skip the paper if it is not published
    if not IsPublished(cadiLine['status']): continue
    ANs        = cadiLine['notes']
    institutes = []
    # precess all ANs for the paper
    for AN in ANs:
        for author in sheet2[AN]['authors']:
            author_ = sheet2[AN]['authors'][author]
            # skip the author if he/she is not from USA
            if author_['country'] != 'USA': continue
            # do not add the same institute more than one time
            if not author_['institute'] in institutes: institutes.append(author_['institute'])
            # do not add the same author the CADI author pool of the institute
            if not author in CADIAuthors[author_['institute']]: CADIAuthors[author_['institute']].append(author)
    for i in institutes:
        Institutes[i]['# of CADI papers'] += 1

for i in Institutes.keys():
    Institutes[i]['# of CADI authors'] = len(CADIAuthors[i])
    Institutes[i]['# of CADI authors from LPC'] = 0
    for j in CADIAuthors[i]:
        if not (USALPC.has_key(j) and USALPC[j]): continue
        Institutes[i]['# of CADI authors from LPC'] += 1

# AN SECTION
for i in Institutes.keys():
    Institutes[i]['# of AN'] = 0
for AN in sheet2:
    institutes = []
    for author in sheet2[AN]['authors']:
        author_ = sheet2[AN]['authors'][author]
        if not author_['institute'] in institutes: institutes.append(author_['institute'])
    for i in institutes:
        if not i in Institutes.keys(): continue
        Institutes[i]['# of AN'] += 1

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
