from os import sys, path

import math

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import datetime
from Chapter5.support.DateInfo import DateInfo

class ControlChartExample(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.SDM = "%d %b %Y %H:%M"

    def GenerateDataTrend(self,inFilename):
        datecount = {}
        result = []
        with open(inFilename) as fp:
            for temp in fp:
                jobj= json.loads(temp)
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
            dinfo.d = datetime.datetime.strptime(key,self.SDM)
            dinfo.count = datecount[key]
            dinfos.append(dinfo)
        mean = self.GetMean(dinfos)
        stddev = self.GetStandardDev(dinfos, mean)
        dinfos.sort(reverse=True)
        for dinfo in dinfos:
            jobj = {}
            jobj["date"]= dinfo.d.strftime(self.SDM)
            jobj["count"]= ((dinfo.count - mean) / stddev)
            jobj["mean"]= 0
            jobj["stdev+3"]= 3
            jobj["stdev-3"]= -3
            result.append(jobj)
        return result

    def GetStandardDev(self,dateinfos,mean):
        intsum= 0
        numperiods = len(dateinfos)
        for dinfo in dateinfos:
            intsum += math.pow((dinfo.count - mean), 2)
        return math.sqrt(float(intsum) / numperiods)

    def GetMean(self ,dateinfos):
        numperiods = len(dateinfos)
        sum = 0
        for dinfo in dateinfos:
            sum += dinfo.count
        return (float(sum) / numperiods)

def main(args):
    cce = ControlChartExample()
    infilename = cce.DEF_INFILENAME

    if len(args)>0:
        infilename = args[0]

    print cce.GenerateDataTrend(infilename)

if __name__ == "__main__":
    main(sys.argv[1:])
