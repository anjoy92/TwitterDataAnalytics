import urllib
from os import sys, path
import json

import time

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter2.openauthentication.OAuthExample import OAuthExample
from Chapter2.support.InfoType import InfoType
from Chapter2.support.APIType import APIType
import requests


class RESTSearchExample(object):
    def __init__(self):
        self.OutFileWriter=""
        self.query = "#protest"
        self.DEF_FILENAME = "searchresults.json"

    def LoadTwitterToken(self):
        self.OAuthTokens = OAuthExample()

    def InitializeWriters(self,filename):
        self.OutFileWriter = open(filename,"w+")

    def GetRateLimitStatus(self):
        r = requests.get(url="https://api.twitter.com/1.1/application/rate_limit_status.json", auth=self.OAuthTokens.authObj.auth)
        return r.json()

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

    def GetSearchResults(self, query):
        r = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q="+urllib.quote(query.encode('utf8'))+"&count=100",
                         auth=self.OAuthTokens.authObj.auth)
        if r.status_code == 400 or r.status_code == 404 or r.status_code == 429:
            time.sleep(self.GetWaitTime("/friends/list"))
        elif r.status_code == 500 or r.status_code == 502 or r.status_code == 503:
            print r.content
            time.sleep(2)

        return r.json()

    def CreateORQuery(self,queryTerms):
        querystr = " OR ".join(queryTerms)
        return querystr

    def WriteToFile(self,data):
        self.OutFileWriter.write(json.dumps(data, indent=4, sort_keys=True))
        self.OutFileWriter.write("\n\n")

def main(args):
    rse = RESTSearchExample()
    queryterms = []
    outfilename = rse.DEF_FILENAME
    if len(args) != 0:
        for i in range(len(args)):
            queryterms.append(args[i])
    else:
        queryterms.append(rse.query)
    rse.LoadTwitterToken()
    print rse.GetRateLimitStatus()

    rse.InitializeWriters(outfilename)

    results = rse.GetSearchResults(rse.CreateORQuery(queryterms))

    rse.WriteToFile(results)




if __name__ == "__main__":
    main(sys.argv[1:])


