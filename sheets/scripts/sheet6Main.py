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
