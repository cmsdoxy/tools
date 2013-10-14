# coding: utf-8
'''
Created on Sep 19, 2013

@author: MantYdze
@email mantas.stankevicius@cern.ch
'''


from Note import Note
from Author import Author

from BeautifulSoup import BeautifulSoup
import re, json

delim = " | "

JSON_DATA = {}

MAX_NUM_OF_ARC = 15 
MAX_NUM_OF_NOTES = 15

annotes_json = ""
country_institute_json = ""

def getCountry(institute_required):
    for country in country_institute_json.keys():
        for institute in country_institute_json[country]:
            if institute == institute_required:
                return country
    return ""

def person_info(html):
    person_soup = BeautifulSoup(html)
    person_raw = person_soup.find("a").renderContents()
    person = person_raw.split("(")
    
    fullname = person[0].strip()
    institute = person[1].replace(")","").strip()
        
    country = getCountry(institute)
    
    return Author(fullname, country, institute)

def note_info(html):
    note_soup = BeautifulSoup(html)
    code = note_soup.find("a").renderContents()
    code=code.strip()
    return Note("CMS AN-" + code, getSubmitterInfo(code))

def getSubmitterInfo(code):
    for tr in annotes:
        tds = tr.findAll("td")
        if tds[0].renderContents() == "CMS AN-"+code:
                # Submitter | Country | Institute             
            return Author(tds[5].renderContents().split("(")[0].strip(), tds[3].renderContents().strip(), tds[4].renderContents().strip()) 
        
def appendAuthor(target, author):
    if (author != None):
        target.append(author.fullname.decode("utf-8"))
        target.append(author.institute)
        target.append(author.country)
    else:
        target.append("")
        target.append("")
        target.append("")
    return target
        
def appendNote(target, note):
    if (note != None):
        target.append(note.code)
        target = appendAuthor(target, note.submitter)
    else:
        target.append("")
        target = appendAuthor(target, None)
    return target


json_file = open('scripts/country_institute.json', 'r')
country_institute_json = json.load(json_file)        
        
f = open("data/annotes.html", "rb");
annotesHTML = f.read()
annotes_soup = BeautifulSoup(annotesHTML)
annotes = annotes_soup.findAll("tr",{ "class" : re.compile(r"^(odd|even)$") })
f.close()

f = open("data/analysies.html", "r");
analysisListHTML = f.read()
f.close()

out = open("sheets/sheet1.csv", "w")


header = "Code | Status | Name | Date | CADI Contact | CADI Contact Institute | CADI Contact Country | ARC Chair | ARC Chair Institute | ARC Chair Country"
for i in range(1, MAX_NUM_OF_ARC+1):
    header += " | ARC Member "+i.__str__()+" name | ARC Member "+i.__str__()+" Institute | ARC Member "+i.__str__()+" Country"

header += " | Total # of ARC Members | Total # of ARC Members from USA "    
for i in range(1, MAX_NUM_OF_NOTES+1):
    header += " | AN "+i.__str__()+" # | AN "+i.__str__()+" Submitter | AN "+i.__str__()+" Submitter Institute | AN "+i.__str__()+" Submitter Country"
    
header += " | Total # of AN | Total # of AN Submitters from US"  

out.write(header+"\n")

soup = BeautifulSoup(analysisListHTML)
trs = soup.findAll("tr",{ "class" : re.compile(r"^(odd|even)$") })

for tr in trs:
    if len(tr.findAll("td")) > 2:
        
        analysis_name = ""        
        analysis_url = ""
        analysis_code = ""
        date = ""
        status = ""
        cadi_contact = None
        chairperson = None
        arc_members = []
        arc_members_usa = 0
        notes = []
        notes_usa = 0
        
        arc_member_list = []
        
        tds = tr.findAll("td")
        
        #TITLE
        analysis_url = tds[0].find("a")["href"]
        
        #DATE    
        date = tds[2].renderContents()
        
        #STATUS
        status = tds[6].find("span").renderContents()
        
        #ARC_MEMBERS
        arc_members_raw = tds[7].renderContents().strip()
        if (arc_members_raw != "no ARC"):
            arc_members_raw = "einam ieskot memberiu"
        
        
        parts = analysis_url.split("&")
        id = parts[2].replace("value=","")

        # GET FROM LOCAL
        inp = open("data/analysies/id_"+id+".html", "r")
        analysisHTML = inp.read()
        inp.close()

        analysisSoup = BeautifulSoup(analysisHTML)
        atrs = analysisSoup.findAll("tr")
        
        for atr in atrs:
            atds = atr.findAll("td")
            
            #Analysis name
            if (atds[0].renderContents().strip() == "Analysis Name:"):
                analysis_name = atds[1].renderContents()
                
            #Analysis CODE
            if (atds[0].renderContents().strip() == "Code:"):
                analysis_code = atds[1].renderContents()
            
            #CADI CONTACT
            if (atds[0].renderContents().strip() == "Contact:"):
                contact_a = atds[1].find("a")
                if (contact_a != None):
                    cadi_contact = person_info(atds[1].renderContents())
            
            # ARC_MEMBERS
            if (atds[0].renderContents().strip() == "ARC:"):
                arc = atds[1].renderContents().strip()
                if arc != "":
                    arc_member_list = arc.split(",")
                    
                    for arc_mem in arc_member_list:
                        if (arc_mem.find("Chairperson") != -1):
                            chairperson = person_info(arc_mem)
                            if (chairperson.country.strip() == "USA"):
                                arc_members_usa +=1
                        else:
                            member = person_info(arc_mem) 
                            if (member.country.strip() == "USA"):
                                arc_members_usa +=1
                            arc_members.append(member)
                    
            # NOTES
            if (atds[0].renderContents().strip() == "notes:"):
                notes_raw = atds[1].renderContents().strip()
                if notes_raw != "":
                    notes_list = notes_raw.split(",")
                    
                    for note in notes_list:
                        note = note_info(note) 
                        if (note.submitter.country.strip() == "USA"):
                            notes_usa +=1
                        notes.append(note)

#        creating line info'
        output_line = []
        output_line.append(analysis_code)                                   # analysis code
        output_line.append(status)                                          # analysis status
        output_line.append(analysis_name)                                   # analysis name
        output_line.append(date)                                            # analysis date
        
        output_line = appendAuthor(output_line, cadi_contact)               # cadi contact
        
        output_line = appendAuthor(output_line, chairperson)                # ARC MEMBER CHAIRPERSON
        
        for member in arc_members:                                          # ARC members
            output_line = appendAuthor(output_line, member)
        
        for i in range(len(arc_members)+1, MAX_NUM_OF_ARC+1):               # fill empty columns
            output_line = appendAuthor(output_line, None)
                
        output_line.append(len(arc_member_list).__str__())                  # number of ARC MEMBERS
        output_line.append(arc_members_usa.__str__())                       # number of ARC MEMBERS from USA
        
        for note in notes:
            output_line = appendNote(output_line, note)                     # list of notes
        
        for i in range(len(notes)+1, MAX_NUM_OF_NOTES+1):                   # fill empty columns
            output_line = appendNote(output_line, None)
         
        output_line.append(len(notes).__str__())                            # number of notes
        output_line.append(notes_usa.__str__())                             # number of notes where submitter is from USA
        
#        print output_line
        out.write(" | ".join([s.encode('utf-8') for s in output_line]))
        

        out.write("\n")
        
        #JSON object
        
        output_data = {}
        output_data["status"] = status
        output_data["analysis_name"] = analysis_name
        output_data["date"] = date
        
        json_cadi_contact = {}
        if (cadi_contact != None):
            json_cadi_contact["fullname"] = cadi_contact.fullname
            json_cadi_contact["country"] = cadi_contact.country
            json_cadi_contact["institute"] = cadi_contact.institute
        
        output_data["cadi_contact"] = json_cadi_contact
        
        json_chairperson = {}
        if (chairperson != None):
            json_chairperson["fullname"] = chairperson.fullname
            json_chairperson["country"] = chairperson.country
            json_chairperson["institute"] = chairperson.institute
        
        output_data["chairperson"] = json_chairperson
        
        output_data["arc_members_num"] = len(arc_member_list)
        output_data["arc_members_usa"] = arc_members_usa
        
        json_arc_members={}
        for arc_member in arc_members:
            json_arc_member = {}
            json_arc_member["country"] = arc_member.country
            json_arc_member["institute"] = arc_member.institute
            json_arc_members[arc_member.fullname] = json_arc_member 
            
        output_data["arc_members"] = json_arc_members
        
        output_data["notes_num"] = len(notes)
        output_data["notes_usa"] = notes_usa
        
        json_notes={}
        for note in notes:
            json_note = {}
            json_note["fullname"] = note.submitter.fullname
            json_note["country"] = note.submitter.country
            json_note["institute"] = note.submitter.institute
            
            json_notes[note.code] = json_note 
            
        output_data["notes"] = json_notes
    
    if (analysis_code != ""):    
        JSON_DATA[analysis_code] = output_data 

#print json.dumps(JSON_DATA,indent=5)

json_o = open("data/sheet1.json", "wb")
json_o.write(json.dumps(JSON_DATA,indent=5))
json_o.close()
        
out.close()

print "Done"
