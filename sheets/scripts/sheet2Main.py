'''
Created on Oct 10, 2013

@author: ali.mehmet.altundag@cern.ch

'''

from BeautifulSoup import BeautifulSoup                                             
import csv, os, re, copy

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
         
    CMSNoteIDIndex  = 0
    TitleIndex      = 1
    submitDateIndex = 2
    CountryIndex    = 3
    InstCodeIndex   = 4
    SubmitterIndex  = 5
    NauthIndex      = 6
        
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

print "ANotes parsing for associating..."
parsedANotes = parseANotes()
print "Done"

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
print "Members information parsing..."
for i in countries:
    #The USA has special situation, it has two pages and these pages have to be merge
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
print "Done"

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

# String functions
def clearSpaceCharacters(str_):
    # input: " Mehmet Altundag   "
    # Output: "Mehmet Altundag"
    indexA = 0
    indexB = len(str_) - 1
    while(str_[indexA] == " "):
        indexA = indexA + 1
    while(str_[indexB] == " "):
        indexB = indexB - 1
    return str_[indexA:indexB+1]

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
    if str_.capitalize() in l:
        return True
    else:
        return False

def parseName(str_):
    if '//' in str_ or '\\' in str_ or '{' in str_ or '}' in  str_:
        return False # Latex text
    else:
        result = []
        str_ = str_.replace(" and ", ', ').replace('\n', ' ').replace('\r', ' ')
        str_ = re.sub(r'\([^)]*\)', '', str_)
        str_ = re.sub(r'\$[^)]*\$', '', str_)
        result = str_.replace(", ", ",").split(',')
        if len(result) == 1:
            result = result[0].split(",")
        nr = []
        for i in result:
            if  digitTest(i) or i == "" or blackList(i):
                if i != "": pass
            else:
                nr.append(i)
        return nr

def match(parsed_name):
    rownumbers = []
    if not parsed_name:
        return False
    for i in parsed_name:
        counter = 0
        matchFlag =  0
        multiName = []
        nameRow = None
        i = clearSpaceCharacters(i)
        for j in parsedMemberInfo:
            # Ex: Meric Taze
            if j[1].lower() + ' ' + j[0].lower() == i.lower():
                nameRow = counter
                matchFlag =  matchFlag + 1
                multiName.append(j[4])
            # Ex: Taze Meric
            #if j[0].lower() + ' ' + j[1].lower() == i.lower():
            #    nameRow = counter
            #    matchFlag =  matchFlag + 1
            #    multiName.append(j[4])
            # Ex: M. Taze
            if j[1][0].lower() + '. ' + j[0].lower() == i.lower():
                nameRow = counter
                matchFlag =  matchFlag + 1
                multiName.append(j[4])
            # Ex: T. Meric
            if j[0][0].lower() + '. ' + j[1].lower() == i.lower():
                nameRow = counter
                matchFlag =  matchFlag + 1
                multiName.append(j[4])
            
            # Ex: M.Taze
            if j[1][0].lower() + '.' + j[0].lower() == i.lower():
                nameRow = counter
                matchFlag =  matchFlag + 1
                multiName.append(j[4])
            # Ex: T.Meric
            if j[0][0].lower() + '.' + j[1].lower() == i.lower():
                nameRow = counter
                matchFlag =  matchFlag + 1
                multiName.append(j[4])
            counter += 1
        if matchFlag == 1 or (matchFlag == 2 and multiName[0] == multiName[1]):
            rownumbers.append(nameRow)
    return rownumbers


def createCSV():
    csvfile         = open('sheets/sheet2.csv', 'wb')
    writer          = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['', "CMSNoteID", "Title", "submitDate", "Country",
                     "InstCode", "Submitter", "Nauth", "NauthUSA", "Sum of Found",
                     "Sum of Match", "Sum of Not Match", ''])

#    length  = len(parsedANotes)
#    counter = 0

    for i in parsedANotes:
        authors         = []
        authors_line    = []
        
        NauthUSA    = 0
        authorCount = int(i[6])

        authors     = parseName(getNameFromFile(i[0]))
        matchResult = match(authors)

        if authors:
            somofFound = len(authors)
        else:
            somofFound = 0

        if matchResult:
            sumofMatch = len(matchResult)
        else:
            sumofMatch = 0

        if matchResult == False:
            #print i[0], 'Latex', authors
            for j in range(authorCount):
                authors_line.append("#not_found(latex)#")
                authors_line.append("#not_found(latex)#")
                authors_line.append("#not_found(latex)#")
        else:
            if len(matchResult) == authorCount:
                #print i[0], 'Perfect!'
                for j in matchResult:
                    if parsedMemberInfo[j][3] == 'USA': NauthUSA += 1
                    authors_line.append(parsedMemberInfo[j][0] + ' ' + parsedMemberInfo[j][1])
                    authors_line.append(parsedMemberInfo[j][2])
                    authors_line.append(parsedMemberInfo[j][3])
            else:
                #print i[0], True, "OK!"
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
        #print i[0]
        writer.writerow(["", i[0], i[1], i[2], i[3], i[4], i[5], i[6], str(NauthUSA), str(somofFound), str(sumofMatch), str(somofFound - sumofMatch) ] + authors_line + [""])
#        counter += 1
#        
#        if counter % (length/100) == 0:
#            print "#"
        
    csvfile.close()

print "Associating..."
createCSV()
print "Done"
# ---------------------------------- #
