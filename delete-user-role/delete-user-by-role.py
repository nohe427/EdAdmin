#-------------------------------------------------------------------------------
# Name:             Remove users from organizaiton based on role
# Purpose:          Parse through users based on role and remove them from t
#                   the organizaiton, including deleting all content and groups
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
import re ## DBUG
################################################################################
#Warning, This script is designed to remove all content regardless of delete
#protection. Please use carefully or remove the protected content sections

#creates a list of users with the role to be deleted
def listUserRole(userDict, role):
    userlist=[]
    for item in userDict:
            if item['role'] == role:
                userlist.append(item['username'])

    return userlist

if __name__ == '__main__':

    #can hardcode username, password and role if scheduling as a task
    #Input Variables
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")
    role = raw_input("What role do you want to delete?")

    #Calls AGOL admin class
    t = excalibur.agolAdmin(user, pw)

    #exchanges custom Role Name for Role ID
    SelectedRole = t.roleAssign(role)

    #get list of users to be removed based on Role
    userlist = listUserRole(t.userDict, SelectedRole)

    print "\nTOTAL USERS TO BE DELETED: " + str(len(userlist))
    print userlist

    for item in userlist:

        #delete all user content:
        delCont = t.delUserContent(item)

        #delete user owned groups
        delGroup = t.delUserGroups(item)

        #delete user from AGOL (will be able to reuse name)
        #uncomment if you want to actually remove username
        #delUsers = t.delUser(item)


