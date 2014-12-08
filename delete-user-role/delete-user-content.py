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


if __name__ == '__main__':

    #variables
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")

    userName = raw_input("What users content do you want to remove?")

    t = excalibur.agolAdmin(user, pw)

    #delete user content:
    delCont = t.delUserContent(item)




