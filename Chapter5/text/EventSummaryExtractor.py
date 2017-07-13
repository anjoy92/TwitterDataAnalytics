from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from datetime import datetime
import json
from Chapter5.support.DateInfo import DateInfo

class EventSummaryExtractor(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.CATEGORIES = {}
        self.twittersdm = "%a %b %d %H:%M:%S Z %Y"
        self.dayhoursdm = "%Y-%b-%d:%H"
        self.daysdm = "%b/%d/%Y"
        self.hoursdm = "%H"

    def InitializeCategories(self):
        people = []
        people.append("protesters")
        people.append("people")
        self.CATEGORIES["People"]= people
        police = []
        police.append("police")
        police.append("cops")
        police.append("nypd")
        police.append("raid")
        self.CATEGORIES["Police"]= police
        media = []
        media.append("press")
        media.append("news")
        media.append("media")
        self.CATEGORIES["Media"] = media
        city = []
        city.append("nyc")
        city.append("zucotti")
        city.append("park")
        self.CATEGORIES["Location"]= city
        judiciary = []
        judiciary.append("judge")
        judiciary.append("eviction")
        judiciary.append("order")
        judiciary.append("court")
        self.CATEGORIES["Judiciary"] = judiciary

    def ExtractCategoryTrends(self,filename):
        result = {}
        temp = ""
        catkeys = self.CATEGORIES.keys()
        datecount = {}
        with open(filename) as fp:
            for temp in fp:
                d = ""
                jobj = json.loads(temp)
                if "created_at" in jobj:
                    time = ""
                    time = jobj["created_at"]
                    if not time:
                        continue
                    else:
                        d = datetime.strptime(time, self.twittersdm)
                elif "timestamp" in jobj:
                    time = jobj["timestamp"]
                    d = datetime.fromtimestamp(time/1000)
                datestr = d.strftime(self.dayhoursdm)
                text = jobj["text"].lower()
                for key in catkeys:
                    words = self.CATEGORIES.keys()
                    for word in words:
                        if word.lower() in text:
                            categorycount={}
                            if datestr in datecount:
                                categorycount = datecount[datestr]
                            if key in categorycount:
                                categorycount[key] +=1
                            else:
                                categorycount[key] =1
                            datecount[datestr] = categorycount
                            break
        datekeys = set(datecount.keys())
        dinfos = []
        for date in datekeys:
            d = datetime.strptime(date, self.dayhoursdm)
            if d:
                info = DateInfo()
                info.d = d
                info.catcounts = datecount[date]
                dinfos.append(info)
        dinfos.sort(reverse=True)
        result["axisxstep"] = len(dinfos) - 1
        result["axisystep"] = len(self.CATEGORIES) - 1
        xcoordinates = []
        ycoordinates = []
        axisxlabels = []
        axisylabels = []
        data = []
        for key in catkeys:
            axisylabels.append(key)
        i=0
        j=0
        for date in dinfos:
            strdate = date.d.strftime(self.hoursdm)
            axisxlabels.append(strdate)
            catcounts = date.catcounts
            for key in catkeys:
                xcoordinates.append(j)
                ycoordinates.append(i)
                i+=1
                if key in catcounts:
                    data.append(catcounts[key])
                else:
                    data.append(0)
            i=0
            j+=1
        result["xcoordinates"]=xcoordinates
        result["ycoordinates"]=ycoordinates
        result["axisxlabels"]=axisxlabels
        result["axisylabels"]=axisylabels
        result["data"]=data
        return result

def main(args):
    ese = EventSummaryExtractor()
    infilename = ese.DEF_INFILENAME

    if len(args)>0:
        infilename = args[0]

    ese.InitializeCategories()
    print ese.ExtractCategoryTrends(infilename)


if __name__ == "__main__":
    main(sys.argv[1:])


