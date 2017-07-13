import os
import urllib
from os import sys, path
import time

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter2.openauthentication.OAuthExample import OAuthExample
import requests


class StreamingApiExample(object):
    def __init__(self):
        self.RECORDS_TO_PROCESS = 30
        self.MAX_KEYWORDS = 400
        self.MAX_USERS = 5000
        self.MAX_GEOBOXES = 25
        self.Keywords = []
        self.Geoboxes = []
        self.Userids = []
        self.CONFIG_FILE_PATH = "streaming/streaming.config"
        self.DEF_OUTPATH = "streaming/"

    def LoadTwitterToken(self):
        self.OAuthTokens = OAuthExample()

    def ReadParameters(self,filename):
        count = 1
        with open(filename) as fp:
            for line in fp:
                if count == 1:
                    temp = line.split("\t")
                    self.Keywords = list(set(temp[:self.MAX_KEYWORDS]))
                if count == 2:
                    temp = line.split("\t")
                    self.Geoboxes = list(set(temp[:self.MAX_GEOBOXES]))
                if count == 3:
                    temp = line.split("\t")
                    self.Userids = list(set(temp[:self.MAX_USERS]))
                count = count + 1

    def CreateStreamingConnection(self,url,filename):
        print self.Keywords
        print urllib.urlencode({'track': self.Keywords,'locations':self.Geoboxes,'follow':self.Userids}, doseq=True)
        r = requests.post(url=url,
                         auth=self.OAuthTokens.authObj.auth, data=urllib.urlencode({'track': self.Keywords,'locations':self.Geoboxes,'follow':self.Userids}, doseq=True),stream=True)
        rawtweets = []
        nooftweetsuploaded = 0
        print "Streaming..."
        for con in r.iter_lines():
            rawtweets.append(con)
            if len(rawtweets)>=self.RECORDS_TO_PROCESS:
                nooftweetsuploaded = nooftweetsuploaded + self.RECORDS_TO_PROCESS
                outFl = filename + "tweets_" + str(time.time()) + ".json"
                print "Writing "+ str(self.RECORDS_TO_PROCESS) + " number of tweets to "+outFl
                with open(outFl, 'w') as outfile:
                    outfile.write("\n".join(rawtweets))
                print "Written "+ str(nooftweetsuploaded) + " records so far"
                rawtweets = []

def main(args):
    sae = StreamingApiExample()
    filename = sae.CONFIG_FILE_PATH
    outfilepath = sae.DEF_OUTPATH
    sae.LoadTwitterToken()
    if len(args)>0:
        filename = args[0]
    if len(args)>1:
        if os.path.isdir(args[1]) and os.path.exists(args[1]):
            outfilepath = args[1]
    sae.ReadParameters(filename)
    sae.CreateStreamingConnection("https://stream.twitter.com/1.1/statuses/filter.json", outfilepath)


if __name__ == "__main__":
    main(sys.argv[1:])