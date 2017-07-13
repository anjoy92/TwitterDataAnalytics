from os import sys, path

from Chapter5.trends.TCDateInfo import TCDateInfo

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import datetime
from Chapter5.support.DateInfo import DateInfo

class SparkLineExample(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.SDM = "%d %b %Y %H"

    def GenerateDataTrend(self,inFilename,keywords):
        result={}
        datecount={}
        with open(inFilename) as fp:
            for temp in fp:
                jobj = json.loads(temp)
                text = jobj["text"].lower()
                timestamp = jobj["timestamp"]
                d = datetime.datetime.fromtimestamp(timestamp/1000)
                strdate = d.strftime(self.SDM)
                for word in keywords:
                    if word in text:
                        wordcount = {}
                        if strdate in datecount:
                            wordcount = datecount[strdate]
                        if word in wordcount:
                            wordcount[word]+=1
                        else:
                            wordcount[word] = 1
                        datecount[strdate] =  wordcount
        dinfos = []
        keys = set(datecount.keys())
        print len(keys)
        for key in keys:
            dinfo = TCDateInfo()
            dinfo.d = datetime.datetime.strptime(key,self.SDM)
            dinfo.wordcount = datecount[key]
            dinfos.append(dinfo)
        dinfos.sort()
        tseriesvals=[]
        for i in keywords:
            tseriesvals.append([])
        for date in dinfos:
            wordcount = date.wordcount
            counter = 0
            for word in keywords:
                if word in wordcount:
                    tseriesvals[counter].append(wordcount[word])
                else:
                    tseriesvals[counter].append(0)
                counter +=1
        counter = 0

        for word in keywords:
            result[word]= tseriesvals[counter]
            counter+=1

        return result


def main(args):
    sle = SparkLineExample()
    words = []
    infilename = sle.DEF_INFILENAME

    if len(args)>0:
        infilename = args[0]

    for i in range(1,len(args)):
        words.append(args[i])

    if not words:
        words.append("#nypd")
        words.append("#ows")

    print sle.GenerateDataTrend(infilename,words)

if __name__ == "__main__":
    main(sys.argv[1:])


