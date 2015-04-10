#-------------------------------------------------------------------------------
# Name:            Remove users from organizaiton based on a spreadsheet with usernames
# Purpose:         Remove users from organization , (including content) with a spreadsheet of usernames.
#                  Username must be the first column of the spreadsheet, and in the proper case.
#
#
# Author:     Kelly Gerrow
#
# Created:     23/06/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#import xml.dom.minidom as DOM
import os, os.path
import sys
import urllib2, urllib, requests
import json, excalibur
################################################################################
#Warning, This script is designed to remove all content regardless of delete
#protection. Please use carefully or remove the protected content sections

def readLine(openedfile):
        #Reads file and splits contents by comma
        line = openedfile.readline()
        line = line.strip()
        splitstring = line.split(",")
        return splitstring

if __name__ == '__main__':

    #Username and Password
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")
    t = excalibur.agolAdmin(user, pw)

    userFile = raw_input("Where is your user CSV file located? ex. c:\manageAgol\user.csv ")

   #Open CSV file and Read first header line
    openedfile = open(userFile, 'r')
    openedfile.readline()

    while True:
            line = readLine(openedfile)
            print len(line[0])
            if len(line[0]) < 1:
                break
            else:

               #delete user content:
                delCont = t.delUserContent(line[0])

                #delete user groups
                delGroup = t.delUserGroups(line[0])


               #delete user
                delUsers = t.delUser(line[0])


