'''
Created on Oct 10, 2013

@author: ali.mehmet.altundag@cern.ch

'''

from BeautifulSoup import BeautifulSoup                                             
import csv, os, re, copy, json

countries = ["Armenia", "Austria", "Belarus", "Belgium",
             "Brazil", "Bulgaria", "China", "Colombia",
             "Croatia", "Cyprus", "Czech Republic", "Egypt",
             "Estonia", "Finland", "France", "Georgia",
             "Germany", "Greece", "Hungary", "India",
             "Iran", "Ireland", "Italy", "Korea", "Lithuania",
             "Malaysia", "Mexico", "Netherlands", "New Zealand",
             "Pakistan", "Poland", "Portugal", "Russia",
             "Serbia", "Spain", "Switzerland", "Taiwan", "Thailand",
             "Turkey", "Ukraine", "United Kingdom", "USA", "Uzbekistan"]

def parseANotes():
    f = open("data/annotes.html")
    source = f.read()
    f.close()
    bs     = BeautifulSoup(source)
    tr     = bs.findAll("tr", {})
         
    CMSNoteIDIndex  = 0#0
    TitleIndex      = 6#1
    submitDateIndex = 1#2
    CountryIndex    = 2#3
    InstCodeIndex   = 3#4
    SubmitterIndex  = 4#5
    NauthIndex      = 5#6
        
    # Data format:
    # [[CMSNoteID, Title, submitDate, Country, InstCode, Submitter, Nauth], ... ]
    CMSANNotes = []
    
    for i in tr[1:len(tr)]:
        cells = i.findChildren('td')
        CMSANNotes.append([cells[CMSNoteIDIndex].text.encode('utf-8'),
                    cells[TitleIndex].text.replace('\n', ' ').replace('\r', ' ').encode('utf-8'),
                    cells[submitDateIndex].text.encode('utf-8'),
                    cells[CountryIndex].text.encode('utf-8'),
                    cells[InstCodeIndex].text.encode('utf-8'),
                    cells[SubmitterIndex].text.encode('utf-8'), 
                    cells[NauthIndex].text.encode('utf-8')])
    return CMSANNotes

parsedANotes = parseANotes()

def parseMemberInfo(fileName):
    f = open(fileName)
    source = f.read()
    f.close()
        
    bs     = BeautifulSoup(source)
    tr     = bs.findAll("tr", {})
        
    # first cells for labels
    cells           = tr[0].findChildren('th')
    counter         = 0
    NameCMSIndex = NamfCMSIndex = InstituteIndex = CountryIndex = 0
    NameCERNIndex = NamfCERNIndex = None
        
    for i in cells:
        if "NameCMS".lower() in i.text.lower():
            NameCMSIndex    = counter
        elif "NamfCMS".lower() in i.text.lower():
            NamfCMSIndex    = counter
        elif "InstCode".lower() in i.text.lower():
            InstituteIndex  = counter
        elif "Country".lower() in i.text.lower():
            CountryIndex    = counter
        elif "NameCERN".lower() in i.text.lower():
            NameCERNIndex = counter
        elif "NamfCERN".lower() in i.text.lower():
            NamfCERNIndex = counter
        counter += 1

    # Data format:
    # [[NameCMS, NamfCMS, Institute, Country], ... ]
    data = []
        
    user_id = 0
    # pass titles
    for i in tr[1:len(tr)]:
        cells           = i.findChildren('td')
        data.append([cells[NameCMSIndex].text.encode('utf-8'),
                    cells[NamfCMSIndex].text.encode('utf-8'),
                    cells[InstituteIndex].text.encode('utf-8'),
                    cells[CountryIndex].text.encode('utf-8'),
                    "%s_%d" % (fileName,user_id)
                    ])
        if NamfCERNIndex != None and NamfCERNIndex != None and cells[NameCERNIndex].text != "" and cells[NamfCERNIndex].text != "":
            data.append([cells[NameCERNIndex].text.encode('utf-8'),
                        cells[NamfCERNIndex].text.encode('utf-8'),
                        cells[InstituteIndex].text.encode('utf-8'),
                        cells[CountryIndex].text.encode('utf-8'),
                        "%s_%d" % (fileName,user_id)
                    ])
        user_id = user_id + 1
    return data

parsedMemberInfo = []
for i in countries:
    #The USA has special situation, it has two pages and these pages have to be merged
    if i == "USA":
        continue
    parsedMemberInfo = parsedMemberInfo + parseMemberInfo("data/authors/%s.html" % i)
    
# Merge USA pages
USA1   = parseMemberInfo("data/authors/USA.html")
USA2   = parseMemberInfo("data/authors/USA2.html")
USAMerged = copy.deepcopy(USA1)

def ishas(list_, item):
    for i in list_:
        if i[0] == item[0] and i[1] == item[1]:
            return True
    return False

for i in USA2:
    if not ishas(USA1, i):
        USAMerged.append(i)
parsedMemberInfo = parsedMemberInfo + USAMerged

def getNameFromFile(fileName):
    f = open("data/detail_pages/%s.html" % fileName.replace('/', '_'))
    source  = f.read()
    f.close()
    bs    = BeautifulSoup(source)
    font  = bs.findAll("font", {})
        
    authorsIndex = 0
    for i in font:
        if "Authors".lower() in i.text.lower():
            authorsIndex = authorsIndex +1
            break
        authorsIndex = authorsIndex + 1
        
    return font[authorsIndex].text.replace(u"~",  " ").encode('utf-8')

def digitTest(str_):
    if "0" in str_: return True
    if "1" in str_: return True
    if "2" in str_: return True
    if "3" in str_: return True
    if "4" in str_: return True
    if "5" in str_: return True
    if "6" in str_: return True
    if "7" in str_: return True
    if "8" in str_: return True
    if "9" in str_: return True
    return False

def blackList(str_):
    l = ['Armenia', 'Austria', 'Belarus', 'Belgium', 'Brazil', 'Bulgaria',
        'China', 'Colombia', 'Croatia', 'Cyprus', 'CzechRepublic', 'Egypt',
        'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece',
        'Hungary', 'India', 'Iran', 'Ireland', 'Italy', 'Korea', 'Lithuania',
        'Mexico', 'Netherlands', 'NewZealand', 'Pakistan', 'Poland', 'Portugal',
        'Russia', 'Serbia', 'Spain', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey',
        'Ukraine', 'UnitedKingdom', 'USA', 'Uzbekistan', 'UK and Perugia', 'Laboratory',
        'Moscow', 'IPN', 'USA ', 'CA', 'Riverside', 'Piscataway', 'Boulder', 'College',
        'London', 'Charlottesville', 'VA.', 'In', 'Geneva', 'Santa Barbara', 'NJ USA',
        'FL', 'Imperial College', 'Perugia', 'Gainesville', 'Florida', 'U.S.A.', 'Los Angeles',
        'CMG+INFN-MIB ', 'Indiana', 'Tallahasse', "Princeton", "Univ.", "University"]
    if str_ in l:
        return True
    else:
        return False

def parseName(authors):
    names = []
    # remove new lines and some replacements
    authors = authors.replace('\n', ' ').replace(" and ", ', ').replace('\r', ' ').replace('%', '')
    # clean up latex statements
    authors = re.sub(re.compile(r'\\[^\\]*?(\{.*?\}){1,}', flags = re.MULTILINE), ',', authors)
    authors = re.sub(re.compile(r'\{.*?\}', flags = re.MULTILINE), '', authors)
    authors = re.sub(re.compile(r'\(.*?\)', flags = re.MULTILINE), '', authors)
    authors = re.sub(re.compile(r'\$.*?\$', flags = re.MULTILINE), '', authors)
    # clean up whitespaces
    authors = re.sub(re.compile(r'\s{1,}', flags = re.MULTILINE), ' ', authors)
    for name in authors.split(','):
        if name == '': continue
        name = name.replace('.', '. ')
        name = re.sub(r'\s{2,}', ' ', name)
        name = name.rstrip().lstrip().replace('\\', '').replace('{', '').replace('}', '')
        if not blackList(name) and name.count(' ') > 0:  names.append(name)
    return names

def match(names):
    IDs = []   # row numbers
    for i in names:
        i = i.lower()
        counter = 0
        for j in parsedMemberInfo:
            firstName = j[1].lower()
            lastName  = j[0].lower()
            c0        = "%s %s" % (firstName, lastName)        # FIRST LAST
            c1        = "%s %s" % (lastName, firstName)        # LAST FIRST
            c2        = "%s, %s" % (lastName[0], firstName)    # L, FIRST
            c3        = "%s. %s" % (firstName[0], lastName)    # F. LAST
            c4        = None
            if firstName.count(' ') > 0:
                lfname= firstName.split(' ')
                fname = []
                for k in lfname:
                    fname.append(k[0])
                fname = '. '.join(fname) + '.'
                c4    = fname + ' ' + lastName                 # F1. F2. LAST

            if c0 == i:
                IDs.append(counter)
                break
            elif c3 == i:
                IDs.append(counter)
                break
            elif c4 and c4 == i:
                IDs.append(counter)
                break
            elif c2 == i:
                IDs.append(counter)
                break
            elif c1 == i:
                IDs.append(counter)
                break
            counter = counter + 1
        print "%s -> %s |  %s |  %s | %s | %s" % (i, c0, c1, c2, c3, c4)
    return IDs

def createCSV():
    csvfile         = open('sheets/sheet2.csv', 'wb')
    json_data       = {}
    writer          = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['', "CMSNoteID", "Title", "submitDate", "Country",
                     "InstCode", "Submitter", "Nauth", "NauthUSA", "Sum of Found",
                     "Sum of Match", "Sum of Not Match", ''])

    for i in parsedANotes:
        authors         = []
        authors_line    = []
        
        NauthUSA    = 0
        authorCount = int(i[6])

        authors     = parseName(getNameFromFile(i[0]))
        matchResult = match(authors)

        if authors: somofFound = len(authors)
        else: somofFound = 0

        if matchResult: sumofMatch = len(matchResult)
        else: sumofMatch = 0

        if len(matchResult) == authorCount:
            for j in matchResult:
                if parsedMemberInfo[j][3] == 'USA': NauthUSA += 1
                authors_line.append(parsedMemberInfo[j][0] + ' ' + parsedMemberInfo[j][1])
                authors_line.append(parsedMemberInfo[j][2])
                authors_line.append(parsedMemberInfo[j][3])
        else:
            subCounter = 0
            for j in matchResult:
                if parsedMemberInfo[j][3] == 'USA': NauthUSA += 1
                authors_line.append(parsedMemberInfo[j][0] + ' ' + parsedMemberInfo[j][1])
                authors_line.append(parsedMemberInfo[j][2])
                authors_line.append(parsedMemberInfo[j][3])
                subCounter += 1
            for j in authors:
                if matchResult == []:
                    authors_line.append(j)
                    authors_line.append("#not_found#")
                    authors_line.append("#not_found#")
                    subCounter += 1
            for j in range(authorCount-subCounter):
                    authors_line.append("#not_found#")
                    authors_line.append("#not_found#")
                    authors_line.append("#not_found#")

        writer.writerow(["", i[0], i[1], i[2], i[3], i[4], i[5], i[6], str(NauthUSA), str(somofFound), str(sumofMatch), str(somofFound - sumofMatch) ] + authors_line + [""])
        
        json_data[i[0]] = {
            "title"     : i[1],
            "date"      : i[2],
            "country"   : i[3],
            "institute" : i[4],
            "fullname"  : i[5],
            "nauth"     : i[6],
            "nauth_usa" : NauthUSA
        }
        json_data[i[0]]["authors"] = {}
        for j in range(len(authors_line)/3):
            json_data[i[0]]["authors"][authors_line[j*3]] = {"institute" : authors_line[j*3 + 1], "country" : authors_line[j*3 + 2]}
        
    csvfile.close()
    json_file = open("data/sheet2.json", 'w')
    json_file.write(json.dumps(json_data, indent = 1))
    json_file.close()

createCSV()
print "Done"
