from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import datetime
from Chapter5.trends.TCDateInfo import TCDateInfo

class TrendComparisonExample(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.SDM = "%d %b %Y %H:%M"

    def GenerateDataTrend(self,inFilename, keywords):
        result = []
        datecount = {}

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
                            wordcount[word] = wordcount[word] + 1
                        else:
                            wordcount[word] = 1
                        datecount[strdate] = wordcount

        dinfos = []
        keys = set(datecount.keys())
        for key in keys:
            dinfo = TCDateInfo()
            dinfo.d = datetime.datetime.strptime(key,self.SDM)
            dinfo.wordcount = datecount.get(key)
            dinfos.append(dinfo)
        dinfos.sort()

        for date in dinfos:
            item = {}
            strdate = date.d.strftime(self.SDM)
            item["date"] = strdate
            wordcount = date.wordcount
            for word in keywords:
                if word in wordcount:
                    item[word] =  wordcount[word]
                else:
                    item[word] = 0
            result.append(item)
        return result


def main(args):
    tce = TrendComparisonExample()
    words = []
    infilename = tce.DEF_INFILENAME

    if len(args)>0:
        infilename = args[0]

    for i in range(1,len(args)):
        words.append(args[i])

    if not words:
        words.append("#nypd")
        words.append("#ows")

    print tce.GenerateDataTrend(infilename,words)

if __name__ == "__main__":
    main(sys.argv[1:])