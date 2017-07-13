from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import datetime
from Chapter5.support.DateInfo import DateInfo

class ExtractDatasetTrend(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.SDM = "%d %b %Y %H:%M"

    def GenerateDataTrend(self,inFilename):
        result = []
        datecount = {}
        with open(inFilename) as fp:
            for temp in fp:
                jobj = json.loads(temp)
                timestamp = jobj["timestamp"]
                d = datetime.datetime.fromtimestamp(timestamp/1000)
                strdate = d.strftime(self.SDM)
                if strdate in datecount:
                    datecount[strdate] += 1
                else:
                    datecount[strdate] = 1
        dinfos = []
        keys = set(datecount.keys())
        for key in keys:
            dinfo = DateInfo()
            dinfo.d = datetime.datetime.strptime(key, self.SDM)
            dinfo.count = datecount[key]
            dinfos.append(dinfo)
        dinfos.sort(reverse=True)
        for dinfo in dinfos:
            jobj = {}
            jobj["date"] = dinfo.d.strftime(self.SDM)
            jobj["count"] = dinfo.count
            result.append(jobj)
        return result


def main(args):
    edt = ExtractDatasetTrend()
    infilename = edt.DEF_INFILENAME

    if len(args)>0:
        infilename = args[0]

    print edt.GenerateDataTrend(infilename)

if __name__ == "__main__":
    main(sys.argv[1:])


