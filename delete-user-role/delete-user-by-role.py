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

def GetCustomRoles(token):

    RolesURL = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/roles?f=json&token={}'.format(URLKey, token)
    response = requests.get(RolesURL)
    Roles = json.loads(response.text)['roles']
    CustomRolesDict = {}
    for role in Roles:
        CustomRolesDict[role['name']] = role['id']

    return CustomRolesDict

def listUserRole(userDict, role):
    userlist=[]
    for item in userDict:
            if item['role'] == role:
                userlist.append(item['username'])


##        # ========================== DREW TESTING ==============================
##        ''' Catch and report any invalid characters in the username.
##            Issue is most likely encoding. Change the encoding with the
##            'encoding' property of the response object.
##            (example: response.encoding = 'ISO-8859-1') -- Drew'''
##        response = requests.get(request) # default encoding is UTF-8
##        output = response.text
##        try:
##            jres = json.loads(output)
##        except ValueError as error_message:
##            char_position = re.findall(r'char (\d*)', str(error_message))[0]
##            invalid_char = output[int(char_position):int(char_position) + 1]
##            error_data = (response.encoding, invalid_char, char_position)
##            print "ValueError found:",
##            print "Encoding {0} found character {1} at position {2}".format(*error_data)
##        # ======================================================================

    return userlist




if __name__ == '__main__':

    #variables
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")

    role = raw_input("What role do you want to delete?")

    t = excalibur.agolAdmin(user, pw)

    SelectedRole = t.roleAssign(role)

    #get list of users to be removed
    userlist = listUserRole(t.userDict, SelectedRole)

    sort_list = sorted(userlist)
    for x in sort_list:
        print x
    print "\nTOTAL USERS: " + str(len(userlist))
    print userlist
     ## DBUG
##    raise SystemExit # NO, PYTHON, STOP!!!
    for item in userlist:

        #delete user content:
        delCont = t.delUserContent(item)

        #delete user groups
        delGroup = t.delUserGroups(item)

        #delete user
        delUsers = t.delUser(item)


