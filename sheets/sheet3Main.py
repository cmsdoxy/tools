'''
Created on Sep 23, 2013

@author: MantYdze
@email: mantas.stankevicius@cern.ch
'''

import json

analysies_json = ""
annotes_json = ""
output = ""

print "Generating sheet3...",

json_file = open('data/sheet1.json', 'r')
analysies_json = json.load(json_file)
    
json_file = open('data/sheet2.json', 'r')
annotes_json = json.load(json_file)
    
analysis_codes = analysies_json.keys()
analysis_codes.sort()

# going through all cadi analysies
for analysis_code in analysis_codes:
    nauth_total = 0
    nauth_usa_total = 0
    
    institutes = {}
    institutes_usa = 0
    
    notes_ids = analysies_json[analysis_code]["notes"].keys()
    
    for note_id in notes_ids:
        if (annotes_json.has_key(note_id)):
            note = annotes_json[note_id]
            
            nauth_total += int(note["nauth"])
            nauth_usa_total += int(note["nauth_usa"])
            
            authors = note["authors"]
            
            for author_key in authors.keys():
                author = authors[author_key]
                if (not institutes.has_key(author["institute"])):
                    institutes[author["institute"]] = author["country"]
                    if author["country"] == "USA":
                        institutes_usa += 1
    
    output_line = []
    output_line.append(analysis_code)
    output_line.append(", ".join(notes_ids))
    output_line.append(nauth_total.__str__())
    output_line.append(nauth_usa_total.__str__())
    output_line.append(", ".join(institutes.keys()))
    output_line.append(len(institutes).__str__())
    output_line.append(institutes_usa.__str__())
    
    output+= " | ".join(output_line) + "\n"

header = " Analysis code | AN Notes | # Authors | # Authors from USA | Institutes | # Institutes | # Insitutes from USA\n"    
f = open("sheets/sheet3.csv","w")
f.write(header+output)
f.close()

print "Done"