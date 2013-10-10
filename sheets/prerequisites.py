'''
Created on Oct 10, 2013

@author: mantas.stankevicius@cern.ch
@author: ali.mehmet.altundag@cern.ch

'''

from BeautifulSoup import BeautifulSoup                                             
import cookielib, urllib, urllib2, getpass, os, re

# Source: http://stackoverflow.com/questions/13925983/login-to-website-using-urllib2-python-2-7

class Login:
    def __init__(self):
        # The action/ target from the form
        authentication_url = """https://cms.cern.ch/iCMS/analysisadmin/loginnice?url='/jsp/page.jsp?mode=news'"""
        
        # Store the cookies and create an opener that will hold them
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

        # Add our headers
        self.opener.addheaders = [('User-agent', 'RedditTesting')]

        # Install our opener (note that this changes the global opener to the one
        # we just made, but you can also just call opener.open() if you want)
        urllib2.install_opener(self.opener)

        # Input parameters we are going to send
        payload = {
            'username':None,
            'password':None,
            'login':'login'
            }
        
        print "Please enter your login and password"

        if not payload['username']:
            payload['username'] = raw_input("Username:")

        if not payload["password"]:
            payload["password"] = getpass.getpass()

        # Use urllib to encode the payload
        data = urllib.urlencode(payload)

        # Build our Request object (supplying 'data' makes it a POST)
        req = urllib2.Request(authentication_url, data)

        # Make the request and read the response
        resp = urllib2.urlopen(req)

        self.contents = resp.read()
    def getPage(self, url):
        return urllib2.urlopen(url).read()

    def getLoginResponse(self):
        return self.contents

# ----------------- TEST ----------------- #

def fetchAnalysies():
    print "Fetching takes a while because CADI is slow. You have to wait about 10 mins. Time to take a break :)"
    print "Fetching list of analysies...",
    
    data = handle.getPage('http://cms.cern.ch/iCMS/analysisadmin/analysismanagement?ALL=true')
    f = open("data/analysies.html", "w")
    f.write(data)
    f.close()
    
    print "Done"
    
    # creating analysies folder where all fetched analysies will be stored
    if not os.path.exists("data/analysies"):
        os.makedirs("data/analysies")
    
    print "Downloading analysies... ",
    
    soup = BeautifulSoup(data)
    trs = soup.findAll("tr",{ "class" : re.compile(r"^(odd|even)$") })
    
    for tr in trs:
        if len(tr.findAll("td")) > 2:
            tds = tr.findAll("td")
            analysis_url = tds[0].find("a")["href"]
            
            parts = analysis_url.split("&")
            id = parts[2].replace("value=","")
            #download analysis details page
            analysisHTML = handle.getPage("http://cms.cern.ch"+analysis_url)
            
            o = open("data/analysies/id_"+id+".html", "w")
            o.write(analysisHTML)
            o.close()
            
    print "Done"
    
def fetchANotes():
    data = handle.getPage('http://cms.cern.ch/iCMS/user/annotes')
    f = open("data/annotes.html", "w")
    f.write(data)
    f.close()

handle = None

print "Checking for prerequisites..."

if not os.path.exists("data"):
    os.makedirs("data")
    
if not os.path.exists("sheets"):
    os.makedirs("sheets")

if not os.path.isfile("data/analysies.html"):
    handle = Login()
    fetchAnalysies()
    
if not os.path.isfile("data/annotes.html"):
    if handle == None:
        handle = Login()
    fetchANotes()

print "Checking finished"

# ----------------- TEST ----------------- #