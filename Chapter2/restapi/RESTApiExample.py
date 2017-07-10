from os import sys, path
import json

import time

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter2.openauthentication.OAuthExample import OAuthExample
from Chapter2.support.InfoType import InfoType
from Chapter2.support.APIType import APIType
import requests

class RESTApiExample(object):

    def __init__(self):
        self.DEF_FILENAME = "users.txt"
        self.DEF_OUTFILENAME = "restapiresults.json"
        self.Usernames = []

    def LoadTwitterToken(self):
        self.OAuthTokens = OAuthExample()

    def GetRateLimitStatus(self):
        r = requests.get(url="https://api.twitter.com/1.1/application/rate_limit_status.json", auth=self.OAuthTokens.authObj.auth)
        return r.json()

    def InitializeWriters(self,filename):
        self.OutFileWriter = open(filename,"w+")

    def ReadUsers(self,filename):
        with open(filename) as fp:
            for line in fp:
                self.Usernames.append(line)

    def WriteToFile(self,data):
        self.OutFileWriter.write(json.dumps(data, indent=4, sort_keys=True))
        self.OutFileWriter.write("\n\n")

    def GetWaitTime(self,api):
        jobj = self.GetRateLimitStatus()
        if jobj != None:
            if jobj.has_key('resources'):
                resourcesobj = jobj["resources"]
                apilimit = None
                if api == APIType().USER_TIMELINE:
                    statusobj = resourcesobj["statuses"]
                    apilimit = statusobj[api]
                elif api == APIType().FOLLOWERS:
                    followersobj = resourcesobj["followers"]
                    apilimit = followersobj[api]
                elif api == APIType().FRIENDS:
                    friendsobj = resourcesobj["friends"]
                    apilimit = friendsobj[api]
                elif api == APIType().USER_PROFILE:
                    userobj = resourcesobj["users"]
                    apilimit = userobj[api]

                numremhits = apilimit["remaining"]
                if numremhits <= 1:
                    resettime = apilimit["reset"]
                    print "Going to sleep for "+ str(resettime-int(time.time()))+" seconds "
                    return resettime-int(time.time())
        return 0

    def GetProfile(self,username):
        profile = None
        print "Processing profile of "+username
        flag = True
        r = requests.get(url="https://api.twitter.com/1.1/users/show.json?screen_name="+username,
                         auth=self.OAuthTokens.authObj.auth)
        if r.status_code==404 or r.status_code==401:
            print r.content
        elif r.status_code==500 or r.status_code==502 or r.status_code==503:
            print r.content
            time.sleep(3)
        elif r.status_code==429:
            time.sleep(self.GetWaitTime("/users/show/:id"))
            flag = False
        if not flag:
            #recreate the connection because something went wrong the first time.
            r = requests.get(url="https://api.twitter.com/1.1/application/rate_limit_status.json",
                             auth=self.OAuthTokens.authObj.auth)
        if flag:
            profile = r.json()

        return profile

    def GetFriends(self,username):
        friends=[]
        print "Processing friends of "+username
        cursor = -1
        while True:
            if cursor == 0:
                break
            r = requests.get(
                url="https://api.twitter.com/1.1/friends/list.json?screen_name=" + username + "&cursor=" + str(cursor),
                auth=self.OAuthTokens.authObj.auth)
            if r.status_code == 400 or r.status_code == 401:
                print r.content
            elif r.status_code == 500 or r.status_code == 502 or r.status_code == 503:
                print r.content
                time.sleep(3)
                continue
            elif r.status_code == 429:
                time.sleep(self.GetWaitTime("/friends/list"))
            jobj = r.json()
            cursor = jobj["next_cursor"]
            userlist = jobj["users"]
            if len(userlist) == 0:
                break
            for i in range(len(userlist)):
                friends.append(userlist[i])

        return friends

    def GetFollowers(self,username):
        followers = []
        print "Processing followers of " + username
        cursor = -1
        while True:
            if cursor == 0:
                break
            r = requests.get(
                url="https://api.twitter.com/1.1/followers/list.json?screen_name=" + username + "&cursor=" + str(cursor),
                auth=self.OAuthTokens.authObj.auth)
            if r.status_code == 400 or r.status_code == 401:
                print r.content
            elif r.status_code == 500 or r.status_code == 502 or r.status_code == 503:
                print r.content
                time.sleep(3)
                continue
            elif r.status_code == 429:
                print "shobhit"
                time.sleep(self.GetWaitTime("/followers/list"))
                continue
            jobj = r.json()
            cursor = jobj["next_cursor"]
            userlist = jobj["users"]
            if len(userlist) == 0:
                break
            for i in range(len(userlist)):
                followers.append(userlist[i])

        return followers

    def GetStatuses(self,username):
        tweetcount = 200
        include_rts = True
        statuses = []
        print "Processing status messages of "+username
        maxid = 0
        while True:
            url = ""
            if maxid == 0:
                url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&include_rts=" + str(include_rts) + "&count=" + str(tweetcount)
            else:
                url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&include_rts=" + str(include_rts) + "&count=" + str(tweetcount) + "&max_id=" + str(maxid - 1)
            r = requests.get(url=url,auth=self.OAuthTokens.authObj.auth)
            if r.status_code == 400 or r.status_code == 404:
                print r.content
            elif r.status_code == 500 or r.status_code == 502 or r.status_code == 503:
                print r.content
                time.sleep(3)
                continue
            elif r.status_code == 429:
                print "shobhit"
                time.sleep(self.GetWaitTime("/statuses/user_timeline"))
                continue
            statusarr = r.json()
            if len(statusarr) == 0:
                break
            for i in range(len(statusarr)):
                jobj = statusarr[i]
                statuses.append(jobj)
                if jobj.has_key("id"):
                    maxid = jobj["id"]
        return statuses

    def CleanupAfterFinish(self):
        self.OutFileWriter.close()

def main(args):

    rae = RESTApiExample()
    rae.LoadTwitterToken()

    print rae.GetRateLimitStatus()
    apicode = InfoType().PROFILE_INFO
    infilename = rae.DEF_FILENAME
    outfilename = rae.DEF_OUTFILENAME
    if args != None:
        if len(args) > 2:
            apicode = int(args[2])
            outfilename = args[1]
            infilename = args[0]
        elif len(args) > 1:
            outfilename = args[1]
            infilename = args[0]
        elif len(args) > 0:
            infilename = args[0]
    rae.InitializeWriters(outfilename)
    rae.ReadUsers(infilename)
    if apicode != InfoType().PROFILE_INFO and apicode != InfoType().FOLLOWER_INFO and apicode != InfoType().FRIEND_INFO and apicode != InfoType().STATUSES_INFO:
        print "Invalid API type: Use 0 for Profile, 1 for Followers, 2 for Friends, and 3 for Statuses"
        return

    if len(rae.Usernames) > 0:
        rae.LoadTwitterToken()
        for user in rae.Usernames:
            if apicode == InfoType().PROFILE_INFO:
                jobj = rae.GetProfile(user)
                if jobj != None and len(jobj) != 0:
                    rae.WriteToFile(jobj)
            elif apicode == InfoType().FRIEND_INFO:
                statusarr = rae.GetFriends(user)
                if len(statusarr) > 0:
                    rae.WriteToFile(statusarr)
            elif apicode == InfoType().FOLLOWER_INFO:
                statusarr = rae.GetFollowers(user)
                if len(statusarr) > 0:
                    rae.WriteToFile(statusarr)
            elif apicode == InfoType().STATUSES_INFO:
                statusarr = rae.GetStatuses(user)
                if len(statusarr) > 0:
                    rae.WriteToFile(statusarr)

    rae.CleanupAfterFinish()


if __name__ == "__main__":
    main(sys.argv[1:])