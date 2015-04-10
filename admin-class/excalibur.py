#-------------------------------------------------------------------------------
# Name:        AGOL Admin
# Purpose:     Admin AGOL
#
# Author:      Kelly
#
# Created:     09/11/2014
# Copyright:   (c) Kelly 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import requests
import json, time, datetime
import string, smtplib, os

class agolAdmin(object):
    #Initializes script reporting on needed values
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__token, self.__ssl= self.__getToken(username, password)
        if self.__ssl == False:
            self.__pref='http://'
        else:
            self.__pref='https://'
        self.__urlKey, self.__id, self.__Name, self.__FullName, self.__Email, self.__maxUsers, self.__availCredits = self.__GetAccount()
        self.__portalUrl = self.__pref+self.__urlKey
        self.__userDict = self.__userDictMethod()
        self.__roleDict = self.__roleDictMethod()
        self.__proDict = self.__proDictMethod()
        self.__creditDict = self.__creditDictMethod()
        self.__groupDict = self.__orgGroupMethod()


    #assigns Variables to names
    @property
    def token(self):
        return self.__token

    @property
    def portalUrl(self):
        return self.__portalUrl

    @property
    def orgID(self):
        return self.__id

    @property
    def orgName(self):
        return self.__Name

    @property
    def fullName(self):
        return self.__FullName
    @property
    def availCredits(self):
        return self.__availCredits

    @property
    def adminEmail(self):
        return self.__Email

    @property
    def maxUser(self):
        return self.__maxUsers

    @property
    def userDict(self):
        return self.__userDict

    @property
    def roleDict(self):
        return self.__roleDict

    @property
    def proDict(self):
        return self.__proDict
    @property
    def creditDict(self):
        return self.__creditDict
    @property
    def groupDict(self):
        return self.__groupDict
#----------------------------------------------------Account Information -----------------------------------------------
    #generates token
    def __getToken(self,adminUser, pw):
        data = {'username': adminUser,
            'password': pw,
            'referer' : 'https://www.arcgis.com',
            'expiration': '432000',
            'f': 'json'}
        url  = 'https://arcgis.com/sharing/rest/generateToken'
        jres = requests.post(url, data=data, verify=False).json()
        return jres['token'],jres['ssl']

    #generates account information
    def __GetAccount(self):
        URL= self.__pref+'www.arcgis.com/sharing/rest/portals/self?f=json&token=' + self.token
        response = requests.get(URL, verify=False)
        jres = json.loads(response.text)
        return jres['urlKey'], jres['id'], jres['name'], jres['user']['fullName'], jres['user']['email'], jres['subscriptionInfo']['maxUsers'], jres['availableCredits']

    #creates dictionary of role names and corresponding IDs
    def __roleDictMethod(self):
        roleVal = {'administrator':'org_admin', 'publisher':'org_publisher', 'user': 'org_user'}
        start = 1
        number = 50
        while start != -1:
            roleUrl= self.__pref+'www.arcgis.com/sharing/rest/portals/self/roles?f=json&start='+str(start)+'&num='+str(number)+'&token=' + self.token
            response = requests.get(roleUrl, verify = False)
            jres = json.loads(response.text)
            for item in jres['roles']:
                roleVal[str(item['name'])] = str(item['id'])
            start =jres['nextStart']
        return roleVal

    #creates a dictionary of Usernames and related information
    def __userDictMethod(self):

        start = 1
        number = 200
        #retreive information of all users in organization
        userDict = []
        while start != -1:
            listURL ='{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(self.portalUrl)
            request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+self.token
            response = requests.get(request, verify = False)
            jres = json.loads(response.text)
            for row in jres['users']:
                userDict.append(row)
            start =jres['nextStart']
        return userDict
    def __orgGroupMethod(self):
        start = 1
        number = 50
        #retreive information of all users in organization
        groupDict = []
        while start != -1:
            groupURL =self.portalUrl+'.maps.arcgis.com/sharing/rest/community/groups?q=orgid%3A'+self.orgID+'&start='+str(start)+'&num='+str(number)+'&f=json&token='+self.token
            response = requests.get(groupURL, verify = False)
            jres = json.loads(response.text)
            for row in jres['results']:
                groupDict.append(row)
            start =jres['nextStart']
        return groupDict

    #Creates dictionary with users level of pro licensing
    def __proDictMethod(self):
        url = '{}.maps.arcgis.com/sharing/rest/content/listings/2d2a9c99bb2a43548c31cd8e32217af6/userEntitlements'.format(self.portalUrl)
        request = url +"?f=json&token="+self.token
        response = requests.get(request, verify=False)
        jres = json.loads(response.text)
        return jres

    def __creditDictMethod(self):
    #queries non -service based credits for the past day
        startTime =int(time.time()) -86400
        EndTime = int(time.time())
        str_ST = str(startTime) + '000'
        str_ET =str(EndTime) + '000'
        creditURL =self.__pref+'www.arcgis.com/sharing/rest/portals/{}/usage?'.format(self.orgID)
        request ="f=json&startTime="+str_ST+"&endTime="+str_ET+"&period=1d&vars=credits%2Cbw%2Cnum%2Cstg&groupby=username&token=" +self.token
        req = creditURL+request
        response = requests.get(req, verify = False)
        jres = json.loads(response.text)
        return jres

#------------------------------Assign Values and IDs for input -----------------------------------------------
    #Assign a name or ID for a user role
    def roleAssign(self,roleInput):

        for key,val in self.roleDict.iteritems():
         if key.lower() == roleInput.lower():
             return val
         if val.lower() == roleInput.lower():
            return key

    def groupAssign(self,groupInput):
        groupVal={}
        for item in self.groupDict:
            groupVal[str(item['title'])] = str(item['id'])

        for key,val in groupVal.iteritems():
         if key.lower() == groupInput.lower():
             return val
         if val.lower() == groupInput.lower():
             return key


    #Assigns a name or ID for My Esri
    def myEsriAssign(self, myEsriInput):
        myEsriVal={'my esri': 'both', 'arcgis online':'arcgisonly'}
        for key,val in myEsriVal.iteritems():
         if key.lower() == myEsriInput.lower():
             return val
         if val.lower() == myEsriInput.lower():
            return key

    #Assigns a Name or ID for Pro Entitlement
    def proEntitleAssign(self,proInput):
        proVal={'advanced':'desktopAdvN', 'basic':'desktopBasicN', 'standard':'desktopStdN', "3d analyst":"3DAnalystN", "data reviewer":"dataReviewerN", 'geostatistical analyst':"geostatAnalystN", "network analyst":"networkAnalystN","spatial analyst":"spatialAnalystN","workflow manager": "workflowMgrN" }
        for key,val in proVal.iteritems():
             if key.lower() == proInput.lower():
                return val
             if val.lower() == proInput.lower():
                return key

#-----------------------------Update User Information---------------------------------------------------------------------------------------------------------------------------------
    #provisions Pro Entitlements based on user list and list of entitlements
    def provisionEntitlement(self, userLst, entitLst):
         #Provisions new users Pro Entitlements
           proUrl= '{}.maps.arcgis.com/sharing/rest/content/listings/2d2a9c99bb2a43548c31cd8e32217af6/provisionUserEntitlements'.format(self.urlKey)
           data = {'f':'json', 'token':self.token ,'userEntitlements':'{"users":["'+userLst+'"],"entitlements":'+entitLst+'}'}
           response = requests.post(proUrl, data=data, verify=False).json()

    #updates username properties depending on the input

    def updateUser(self,userName,myEsri=None,fullName = None,description=None, access=None,tags=None,email=None, password=None):
        userURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(self.__urlKey, userName)
        data = {'f':'json','token':self.token}
        if access:
            data['access'] = access
        if fullName :
            data['fullName']= fullName
        if description:
            data['description'] = description
        if myEsri:
            data['usertype'] = myEsri
        if tags:
            data['tags']= tags
        if email:
            data['email'] = email
        if password:
            data['password'] = password
        print data
        response = requests.post(userURL, data=data, verify=False).json()


    #updates UserRole to specified RolID
    def updateUserRole(self, userName, roleID):
       #updates user role to Administrator
       updateURL = '{}.maps.arcgis.com/sharing/rest/portals/self/updateUserRole'.format(self.portalUrl)
       data ={'f':'json', 'token':self.token ,'user':user,'role':roleID}
       response = requests.post(updateURL, data=data, verify=False).json()

    def delUserContent(self, userName, protected=True):
        '''Deletes all of a user's content including protected content and content
        stored in additional folders.'''

        itemURL ='{}.maps.arcgis.com/sharing/rest/content/users/{}'.format(self.portalUrl, userName)
        request = itemURL +"?f=json&token="+self.token
        response = requests.get(request, verify = False)
        jres = json.loads(response.text)
        if protected:
            print "protected items will be deleted"
        else:
            print "Protected items will not be deleted"

        if jres['items']:
            for item in jres['items']:
                itemID= item['id']
                print "Attempting to delete item ID:{}".format(itemID)
                if item['protected']:
                    if protected:
                        '''delete protected data'''
                        unprotectURL = '{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/unprotect'.format(self.portalUrl,userName,itemID)
                        data = {'f':'json', 'token':self.token}
                        resp = requests.post(unprotectURL, data=data, verify=false)

                        delURL = '{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/delete'.format(self.portalUrl,userName,itemID)
                        try:
                          response = requests.post(delURL,data=data, verify = False)
                        except Exception as e:
                          print("Exception {0}. Item may already be deleted...\n".format(e))

                    else:
                        print "Cannot delete item id {} because it is protected; the user will not be deleted.".format(item['id'])

                else:
                    '''delete unprotected data'''
                    delURL = '{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/delete'.format(self.portalUrl,userName,itemID)
                    data = {'f':'json', 'token':self.token}
                    try:
                        response = requests.post(delURL,data=data, verify = False)
                    except Exception as e:
                        print("Exception {0}. Item may already be deleted...\n".format(e))

        else:
            print 'No items to delete in the default folder.'


        if jres['folders']:
            '''Delete content stored in folders'''
            for folder in jres['folders']:
                folderID = folder['id']
                foldercontentURL ='{}.maps.arcgis.com/sharing/rest/content/users/{}/{}?f=json&token={}'.format(self.portalUrl,userName, folderID, self.token)
                response = requests.get(foldercontentURL, verify = False)
                jres = json.loads(response.text)

                if jres['items']:
                    for item in jres['items']:
                        itemID= item['id']
                        print "Attempting to delete item ID:{}".format(itemID)

                        if item['protected']:
                            if protected:
                                '''delete protected data'''
                                unprotectURL = '{}.maps.arcgis.com/sharing/rest/content/users/{}/{}/items/{}/unprotect'.format(self.portalUrl,userName,folderID,itemID)
                                data = {'f':'json', 'token':self.token}
                                response = requests.post(unprotectURL,data=data, verify = False).json()
                                delURL = '{}.maps.arcgis.com/sharing/rest/content/users/{}/{}/items/{}/delete'.format(self.portalUrl,userName,folderID, itemID)
                                try:
                                    response = requests.post(delURL,data=data, verify = False)
                                except Exception as e:
                                    print("Exception {0}. Item may already be deleted...\n".format(e))


                            else:
                                print "Cannot delete item id {} located in folder {} because it is protected; the user will not be deleted.".format(item['id'], folderID)
                        else:
                            '''delete unprotected data'''
                            if item['ownerFolder']:
                                delURL = '{}.maps.arcgis.com/sharing/rest/content/users/{}/{}/items/{}/delete'.format(self.portalUrl,userName,folderID,itemID)
                                data = {'f':'json', 'token':self.token}
                                response = requests.post(delURL,data=data, verify = False).json()

                #delete the folder
                try:
                    folderURL = '{}.maps.arcgis.com/sharing/rest/content/users/{}/{}/delete'.format(self.portalUrl,userName,folderID)
                    data = {'f':'json','token':self.token}
                    response = requests.post(folderURL,data=data, verify = False).json()
                    print "Folder {} has been deleted.".format(folderID)

                except KeyError:
                    print "Unable to delete folder {}, please check that all of the items were deleted from it first.".format(folderID)
    def delUserGroups(self, userName):

        groupURL ='{}.maps.arcgis.com/sharing/rest/community/users/{}'.format(self.portalUrl, userName)
        request = groupURL +"?f=json&token="+self.token
        response = requests.get(request, verify = False)
        jres = json.loads(response.text)
        for row in jres['groups']:
            if row['id'] != "" and row['owner'] == userName:
                delURL ='{}.maps.arcgis.com/sharing/rest/community/groups/{}/delete'.format(self.portalUrl,row['id'])
                data = {'f':'json','token':self.token}
                response = requests.post(delURL,data=data, verify = False).json()
                try:
                    if response['success']:
                         print "deleting is a group" + row['id']
                except:
                    print 'there is an application in this group that must be manually removed'
                    quit()

    def delUser(self, userName):
      #  Revoke Pro Entitlements
        proUrl= '{}.maps.arcgis.com/sharing/rest/content/listings/2d2a9c99bb2a43548c31cd8e32217af6/provisionUserEntitlements'.format(self.portalUrl)
        data = {'f':'json', 'token':self.token ,'userEntitlements':'{"users":["'+userName+'"],"entitlements":[]}'}
        response = requests.post(proUrl, data=data, verify=False).json()

        #disable my ESri Access

        userURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(self.__urlKey, userName)
        data = {'f':'json','usertype':'arcgisonly','token':self.token}
        response = requests.post(userURL, data=data, verify=False).json()

        delURL ='{}.maps.arcgis.com/sharing/rest/community/users/{}/delete'.format(self.portalUrl,userName)
        data = {'f':'json','token':self.token}
        response = requests.post(delURL,data=data, verify = False).json()
        if response['success'] is True:
            print 'Deleted the following user: ' +userName
        else:
            print 'user was not deleted'

#---------------------------Administrative Organization tasks------------------------------------------------------------------------
    #creates a role and assigns privleges
    def createRole(self,roleName,description,privs):
       roleURL = '{}.maps.arcgis.com/sharing/rest/portals/self/createRole'.format(self.portalUrl)
       roleData= {'name':roleName, 'description':description, 'f':'json', 'token':self.token}
       jres = requests.post(roleURL, data = roleData, verify = False).json()
       privileges = '{"privileges":'+str(privs) + "}"

       #Assign Privleges to roles
       privURL = '{}.maps.arcgis.com/sharing/rest/portals/self/roles/{}/setPrivileges'.format(self.portalUrl, jres['id'])
       privData = {'id':jres['id'], 'privileges':privileges, 'f':'json', 'token':self.token}
       pres =requests.post(privURL, data = privData, verify=False).json()

    #define how many users can be
    def __availableInvites(self):
        URL ='{}.maps.arcgis.com/sharing/rest/portals/self/users?start=1&num=1&f=json&token='.format(self.portalUrl)+self.token
        response = requests.get(URL)
        jres = json.loads(response.text)
        actUser=jres['total']
        if actUser<self.maxUser:
            invite = True
        else:
            invite=False
        return invite

    def inviteUsers(self, userName,roleID, userFullName):
        invite=self.__availableInvites()
        if invite ==True:
            #invite users from spreadsheet
            url = '{}.maps.arcgis.com/sharing/rest/portals/self/invite'.format(self.portalUrl)
            #subject and text for email
            subject = 'An invitation to join an ArcGIS Online Organization, ' + self.orgName + '. DO NOT REPLY'
            text = '<html><body><p>' + self.fullName+ ' has invited you to join an ArcGIS Online Organization, ' +self.orgName + '. Please click this link to join:<br><a href="https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@">https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@</a></p><p>If you have difficulty signing in, please email your administrator at '+ self.adminEmail+ '. Be sure to include a description of the problem, your username, the error message, and a screenshot.</p><p>For your reference, you can access the home page of the organization here: <br>http://'+self.urlKey +'.maps.arcgis.com/home/</p><p>This link will expire in two weeks.</p><p style="color:gray;">This is an automated email, please do not reply.</p></body></html>'

            #send invitation without sending an email notification to user
            invitationlist = '{"invitations":[{"username":"'+userName+'", "password":"Password123", "fullname":'+userFullName+',"email":"'+self.adminEmail+'","role":"' +roleID +'"}]}'
            data={'subject':subject, 'html':text, 'invitationlist':invitationlist,'f':'json', 'token':self.token}
            jres = requests.post(url, data=data, verify=False).json()
            return 'success'
        else:
            return 'error: All invitations have been used'

    #creates a Group
    def createGroup(self, title, tags, description, access, viewOnly):
        url = self.portalUrl+'.maps.arcgis.com/sharing/rest/community/createGroup'
        data = {'title': title, 'tags':tags, 'description': description,'access': access, 'isViewOnly':viewOnly, 'f':'json', 'token':self.token}
        jres = requests.post(url, data=data, verify = False).json()
        return jres
    #shares item with Group
    def shareGroup(self, itemId, groupId):
        url = self.portalUrl+'.maps.arcgis.com/sharing/rest/content/items/{}/share'.format(itemId)
        data = {'groups':groupId, 'f':'json', 'token':self.token}
        jres = requests.post(url, data=data, verify = False)
    #add User to Group
    def addUserToGroup(self, userlist, groupId):
        url = self.portalUrl+'.maps.arcgis.com/sharing/rest/community/groups/{}/addUsers'.format(groupId)
        data ={'users':userlist, 'f':'json','token':self.token}
        jres = requests.post(url, data=data, verify = False)
    #list users in a group
    def listGroupUsers(self, groupId):
        url = self.portalUrl+'.maps.arcgis.com/sharing/rest/community/groups/{}/users'.format(groupId)
        data ={'f':'json','token':self.token}
        response = requests.post(url, data=data, verify = False)
        jres = json.loads(response.text)

        return jres['admins'], jres['owner'],jres['users']

    #sets feature group, but more parameters can be added
    def updateOrgAdmin(self, groupId):
        url = self.portalUrl+'.maps.arcgis.com/sharing/rest/portals/self/update'
        data= {'homePageFeaturedContent':groupId,'f':'json', 'token':self.token}
        jres = requests.post(url, data=data, verify = False)

#-----------------------------------------------User analysis-----------------------------------------
    def countFeatures(self, userName):
       itemURL ='{}.maps.arcgis.com/sharing/rest/content/users/{}'.format(self.portalUrl, userName)
       request = itemURL +"?f=json&token="+self.token
       response = requests.get(request, verify = False )
       jres = json.loads(response.text)
       num = 0
       for item in jres['items']:
             if item['type'] == 'Feature Service':
               for x in item['typeKeywords']:
                  if x=='Hosted Service':
                       num +=1
       return num

    def userCredit(self,userName):
        creds = 0
        for item in self.creditDict['data']:
            try:
                if userName == item['username']:
                    for x in item['credits']:
                        creds += float(x[1])
            except KeyError:
                pass
        return creds

    def creditService(self):
    #queries feature service and tiled generation based credits for the past day
        startTime =int(time.time()) -86400
        EndTime = int(time.time())
        str_ST = str(startTime) + '000'
        str_ET =str(EndTime) + '000'
        creditURL =self.__pref+'www.arcgis.com/sharing/rest/portals/{}/usage?'.format(self.orgID)
        request ="f=json&startTime="+str_ST+"&endTime="+str_ET+"&period=1d&vars=credits&groupby=stype,etype&token=" +self.token
        req = creditURL+request
        response = requests.get(req, verify = False)
        jres = json.loads(response.text)

        HFScreds = 0
        tileGencreds = 0
        for item in jres['data']:
            try:
                if item['etype'] =='svcusg' and item['stype']=='features':
                    for x in item['credits']:
                        HFScreds += float(x[1])
                if item['etype'] =='tilegencnt' and item['stype']=='tiles':
                    for x in item['credits']:
                        tileGencreds += float(x[1])
            except KeyError:
                pass
        hfscredRNd = round(HFScreds,2)
        tilernd = round(tileGencreds,2)

        return hfscredRNd, tilernd



