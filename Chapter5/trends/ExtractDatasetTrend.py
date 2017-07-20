#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Creates Simple Trend Line data for visualization from the tweet file provided.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import datetime
from Chapter5.support.DateInfo import DateInfo
from flask import json, render_template, send_from_directory, jsonify, request
from flask import Flask
app = Flask(__name__ ,static_folder='../static')

@app.route('/')
def hello_world():
    """
    Returns the  TrendLineExample HTML file as First page.
    The JS file being used for this page is: trendLine.js
    The CSS file being used for this page is: trendLine.css
    :return: The page to be rendered
    """
    return send_from_directory('../templates/','TrendLineExample.html')


class ExtractDatasetTrend(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.SDM = "%d %b %Y %H:%M"

    def generate_data_trend(self, inFilename):
        result = []
        datecount = {}

        # Open the tweet file and get the date count on each format
        with open(inFilename) as fp:
            for temp in fp:
                jobj = json.loads(temp)
                timestamp = jobj["timestamp"]
                d = datetime.datetime.fromtimestamp(timestamp / 1000)
                strdate = d.strftime(self.SDM)
                if strdate in datecount:
                    datecount[strdate] += 1
                else:
                    datecount[strdate] = 1
        dinfos = []

        # Iterate on keys and generate a DateInfo class object
        keys = set(datecount.keys())
        for key in keys:
            dinfo = DateInfo()
            dinfo.d = datetime.datetime.strptime(key, self.SDM)
            dinfo.count = datecount[key]
            dinfos.append(dinfo)
        dinfos.sort(reverse=True)

        # Create a json object as required by D3js Library
        for dinfo in dinfos:
            jobj = {}
            jobj["date"] = dinfo.d.strftime(self.SDM)
            jobj["count"] = dinfo.count
            result.append(jobj)
        return result


@app.route('/getData', methods=['GET', 'POST'])
def get_data():
    """
    Function to generate Simple Data Trend from tweet file given
    :return: 
    """
    global in_filename
    edt = ExtractDatasetTrend()

    return jsonify(edt.generate_data_trend(in_filename))


if __name__ == '__main__':
    global in_filename

    parser = argparse.ArgumentParser(
        description='''Creates Simple Trend Line data for visualization from the tweet file provided.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=ExtractDatasetTrend().DEF_INFILENAME,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    # Get the file name containing the tweets from the command line argument
    in_filename = argsi.i

    # Run the flask app on port 5006
    app.run(port=5006)
