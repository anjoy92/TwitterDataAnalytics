#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Adds context to word cloud. Creates a Temporal Heatmap data for visualization according to the categories mentioned.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from datetime import datetime
import json
from Chapter5.support.DateInfo import DateInfo
from flask import json, render_template, send_from_directory, jsonify, request
from flask import Flask
app = Flask(__name__ ,static_folder='../static')

@app.route('/')
def hello_world():
   return send_from_directory('../templates/','TopicChartExample.html')



class EventSummaryExtractor(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.CATEGORIES = {}
        self.twittersdm = "%a %b %d %H:%M:%S Z %Y"
        self.dayhoursdm = "%Y-%b-%d:%H"
        self.daysdm = "%b/%d/%Y"
        self.hoursdm = "%H"

    def initialize_categories(self):
        self.CATEGORIES["People"]= ["protesters", "people"]
        self.CATEGORIES["Police"]= ["police", "cops", "nypd", "raid"]
        self.CATEGORIES["Media"] = ["press", "news", "media"]
        self.CATEGORIES["Location"]= ["nyc", "zucotti", "park"]
        self.CATEGORIES["Judiciary"] = ["judge", "eviction", "order", "court"]

    def extract_category_trends(self, filename):
        """
        :param filename: 
        :return: 
        """
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


@app.route('/getData', methods=['GET', 'POST'])
def getData():
    ese = EventSummaryExtractor()
    parser = argparse.ArgumentParser(
        description='''Adds context to word cloud. Creates a Temporal Heatmap data for visualization according to the categories mentioned.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=ese.DEF_INFILENAME,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    infile_name = argsi.i
    ese.initialize_categories()

    return jsonify(ese.extract_category_trends(infile_name))


if __name__ == '__main__':
   app.run()



