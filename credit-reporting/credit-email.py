#-------------------------------------------------------------------------------
# Name:        Credit Consumption Notifier
# Purpose:     Will email org admin when credit threshold is passed
#
# Author:      kell6873
#
# Created:     30/12/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#import xml.dom.minidom as DOM
import os, os.path
import sys
import urllib2, urllib, requests
import excalibur
import json, time, datetime, string, smtplib, os
from cookielib import CookieJar
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


#email address
def eMAIL(gTo, gSubject, gMsg):
   gHOST    = "SMTP.ESRI.COM"
   gFrom    = "email@esri.com" #enter senders email address
   BODY  = string.join((
           "From: %s" % gFrom,
           "To:   %s" % gTo,
           "Subject: %s" % gSubject,
           "",
           gMsg), "\r")
   eMsg = smtplib.SMTP(gHOST)
   eMsg.sendmail(gFrom,gTo,BODY)

def generateEmail(credituserDict):
   subject = 'Credit Report from ArcGIS Online Organization ' +t.orgName
   greetingMessage = 'Hello Friend, \n\nSome users in your organization have used more than the threshold set by your organization. There are currently ' +str(round(t.availCredits,2)) + ' available in your organization. '+str(round(totalCreds,2))+ ' credits were used in the past 24 hours.'
   creditmessage = '\nToday, '+str(tileGen) + ' credits were consumed generating tiles and '+ str(featServ)+ ' credits were consumed from Feature Service storage. The following users used over ' + str(creditThreshold) + ' credits'+ str(credituserDict)
   signoff = '\nThanks, \nYour friendly credit reporter'
   message = greetingMessage+creditmessage+signoff
   eMAIL(email, subject, message)



if __name__ == '__main__':

     #Username and Password
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")
    creditThreshold = raw_input('How many credits do you want to be notified about? ex. 1000')
    email = raw_input('Who is receiving this email?')
    t = excalibur.agolAdmin(user, pw)

    #loop through total credit usage
    credituserDict= {}

    totalCreds= 0
    for item in t.creditDict['data']:
            try:
                for x in item['credits']:
                   totalCreds += float(x[1])

            except KeyError:
                pass
    servicecreds = t.creditService()
    tileGen = servicecreds[1]
    featServ = servicecreds[0]

    #create a dictionary of usernames and credits
    for user in t.userDict:
        num = t.userCredit(user['username'])
        print num
        if num >= float(creditThreshold):
            credituserDict[user['username']] = num
    print credituserDict

    if len(credituserDict)>0:
        generateEmail(credituserDict)




