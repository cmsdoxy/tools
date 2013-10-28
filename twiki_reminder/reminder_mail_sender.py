'''
Created on Dec 3, 2010

@author: MantYdze
'''
import sys
import os
import subprocess

TITLE = "Twiki Reminder Service"

def getMessage(user_email):
    message = '''
    Dear Twiki User,
    
    this is an automatic reminder of twiki pages you own. The aim of this reminder is to help you to maintain your pages and
    to encourage you to delete the out-of-date information. With some care and discipline we can improve the documentation.
    See your report in http://twikireminderservice.web.cern.ch/TwikiReminderService/reports/'''+user_email+'''_report.html
    There are three lists:
    
    - List 1 contains all twiki pages of which you are marked as a responsible.
    Note that according to the CMS Twiki policy(*) all twiki pages in the CMS web should have a responsible person defined.
    As this is often not the case, we also list the pages without a responsible:
    - which you last edited (list 2) 
    - which you have created (list 3). 
    If you consider being responsible of these pages please add your name as instructed in (**).
    The pages which have not been edited in last six months are marked with a red font. 
    Please have a look if they are still needed and delete them if appropriate.
    Note that you can delete the pages that are not needed by clicking on \"More topic actions\" on the bottom of the each page and choosing
    Delete. As this operation takes some time, the report offers a possibility of a delete request. The topics will then be deleted centrally.
        
    
    Many thanks for your collaboration and kind regards,
    
    CMS User Support

    Not at CERN anymore? Unsubscribe  http://twikireminderservice.web.cern.ch/TwikiReminderService/unsubscribe/form.php?sender='''+user_email+'''
    
    (*) https://twiki.cern.ch/twiki/bin/view/CMS/CMSTwikiPolicy
    (**) https://twiki.cern.ch/twiki/bin/view/CMS/CMSTwikiPolicy#Rules_concerning_the_page_conten
    '''
    return message

def getListOfUsers():
    input = open(sourceFile, "r")
    users = input.read()
    input.close()
    
    return users.split("\n")

def sendEmail(user_email):
    try:
        message = getMessage(user_email)
        
        p1 = subprocess.Popen(['echo', message], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['mutt','-s',TITLE,user_email], stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0]
    
        print "Sent to %s" % (user_email)
        return True;
    except:
        print sys.exc_info()
        return False

if len(sys.argv) > 1:
    global sourceFile
    sourceFile = sys.argv[1]
    
    sentEmails = 0
#    sendEmail("mantas.stankevicius@cern.ch")

    
    users = getListOfUsers()
    for user_email in users:
        if (sendEmail(user_email)):
            sentEmails = sentEmails + 1
    
    print "("+sentEmails.__str__()+") Emails sent"
        
else:
    print "Not enough parameters: file.py sourceFile"
