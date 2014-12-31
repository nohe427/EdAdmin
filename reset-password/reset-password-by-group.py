#-------------------------------------------------------------------------------
# Name:             Reset a Users Password from an existing account
# Purpose:          Reset a users Password in a specific group
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




if __name__ == '__main__':

    #variables to generate username and password
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")

    #usernames to reset passwords
    groupName = raw_input("What group of users passwords do you want to reset?")
    #passW = ("What should the password be?")
    passW = 'password1'
    #call Class
    t = excalibur.agolAdmin(user, pw)
    #Create userlist from group users
    #get Group ID based on GroupName input
    groupId = t.groupAssign(groupName)
    #get list of users in group. Returns 3 values, admins, owner, users
    grouplist = t.listGroupUsers(groupId)
    print grouplist[2]

    #loop through user list and reset password
    for user in grouplist[2]:
        #reset users password
        t.updateUser(user,"","","","","","", passW)




