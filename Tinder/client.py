import time
import requests
import urllib3 as url
from objects import person
from token import *
import json
import datetime
last_activity_date = '2014-04-09T04:41:38.276Z'

URL = 'https://api.gotinder.com'
matches = []

TOKYO =  {u'lat': 35.678403, u'lon': 139.670506}
SIGNGAPORE = {u'lat': 1.290301, u'lon': 103.844555}
PARIS =  {u'lat': 48.856614, u'lon': 2.352222}
NYC =  {u'lat': 40.738187, u'lon': -74.005204}
location = NYC

def datetimeToTimestamp(datetime):
    split = str(datetime).split(' ')
    return split[0]+'T'+split[1]+'Z'

class BaseClient():

    def __init__(self,token):
        self.req = url.HTTPSConnectionPool(URL)
        self.HEADERS = HEADERS
        self.HEADERS['X-Auth-Token'] = requests.post(URL+'/auth', data= {"facebook_token":token}).json()['token']

    def updateLocation(self,location):
        return requests.post(URL+'/user/ping', headers=self.HEADERS, data=location).json()

    def likeUser(self, id):
        return requests.get(URL+'/like/' + id, headers=self.HEADERS).json()

    def getRecs(self):
        return requests.post(URL+'/user/recs', headers=self.HEADERS, data={"limit": 40}).json()

    def getUpdate(self, date='2014-04-07T06:36:49.027Z'):
        return requests.post(URL+'/updates', headers=self.HEADERS, data={'last_activity_date': date}).json()

    def sendMessage(self, message, matchid):
        return requests.post(URL+'/user/matches/' + matchid, headers=self.HEADERS, data={"message": message}).json()

class ExampleClient(BaseClient):

    def getUsers(self, numusers):
        users = []
        while(len(users) < numusers):
            users += self.getRecs()['results']
        return users
    def likeUsers(self, users):
        for i in users:
            print self.likeUser(i['_id'])





HEADERS = {'Accept-Language': 'en-GB;q=1, en;q=0.9, fr;q=0.8, de;q=0.7, ja;q=0.6, nl;q=0.5',
           'User-Agent': 'Tinder/3.0.3 (iPhone; iOS 7.0.6; Scale/2.00)',
           'os_version': '70000000006',
           'Accept': '*/*',
           'platform': 'ios',
           'Connection': 'keep-alive',
           'Proxy-Connection': 'keep-alive',
           'app_version': '1',
           'Accept-Encoding': 'gzip, deflate',}

ec = ExampleClient(facebook_token)
date = datetimeToTimestamp(datetime.datetime.today() - datetime.timedelta(minutes=20))
print ec.getUpdate(date)
