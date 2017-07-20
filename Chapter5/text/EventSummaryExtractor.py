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
    """
    Returns the  TopicChartExample HTML file as First page.
    The JS file being used for this page is: topicChart.js
    The CSS file being used for this page is: topicChart.css
    :return: The page to be rendered
    """
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

        # Open file and get time stamps from the tweets
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

                # Convert date to the format needed by D3js
                datestr = d.strftime(self.dayhoursdm)
                text = jobj["text"].lower()

                # Assign it to the category the tweets belong to
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

        # For each datekeys generate a DateInfo class object and append
        for date in datekeys:
            d = datetime.strptime(date, self.dayhoursdm)
            if d:
                info = DateInfo()
                info.d = d
                info.catcounts = datecount[date]
                dinfos.append(info)

        # Sort in descending order of the dates
        dinfos.sort(reverse=True)

        # Assign asixsteps according to number of categories and dates
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
def get_data():
    """
    Function to generate Event summary from the Categories given
    :return: 
    """
    global infile_name
    ese = EventSummaryExtractor()

    ese.initialize_categories()

    return jsonify(ese.extract_category_trends(infile_name))


if __name__ == '__main__':
    global infile_name
    ese = EventSummaryExtractor()
    parser = argparse.ArgumentParser(
        description='''Adds context to word cloud. Creates a Temporal Heatmap data for visualization according to the categories mentioned.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=ese.DEF_INFILENAME,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    # Get the file name containing the tweets from the command line argument
    infile_name = argsi.i

    # Start the flask app on port 5001
    app.run(port=5003)



