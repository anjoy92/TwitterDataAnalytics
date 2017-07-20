#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Creates data for visualizing Trend Comparison.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import datetime
from Chapter5.trends.TCDateInfo import TCDateInfo
from flask import json, render_template, send_from_directory, jsonify, request
from flask import Flask

app = Flask(__name__, static_folder='../static')


@app.route('/')
def hello_world():
    """
    Returns the  TrendComparisonExample HTML file as First page.
    The JS file being used for this page is: trendComparison.js
    The CSS file being used for this page is: trendComparison.css
    :return: The page to be rendered
    """
    return send_from_directory('../templates/', 'TrendComparisonExample.html')


class TrendComparisonExample(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.SDM = "%d %b %Y %H:%M"

    def generate_data_trend(self, in_filename, keywords):
        """
        :param in_filename: File containing tweets
        :param keywords: words for trend comparision.
        """
        result = []
        datecount = {}

        # Open the tweet file and get the date and word count on each date format
        with open(in_filename) as fp:
            for temp in fp:
                jobj = json.loads(temp)
                text = jobj["text"].lower()
                timestamp = jobj["timestamp"]
                d = datetime.datetime.fromtimestamp(timestamp / 1000)
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

        # Iterate on keys and generate DateInfo class object
        for key in keys:
            dinfo = TCDateInfo()
            dinfo.d = datetime.datetime.strptime(key, self.SDM)
            dinfo.wordcount = datecount.get(key)
            dinfos.append(dinfo)
        dinfos.sort()

        # Create a result json object as required by D3js Library
        for date in dinfos:
            item = {}
            strdate = date.d.strftime(self.SDM)
            item["date"] = strdate
            wordcount = date.wordcount
            for word in keywords:
                if word in wordcount:
                    item[word] = wordcount[word]
                else:
                    item[word] = 0
            result.append(item)
        return result


@app.route('/getData', methods=['GET', 'POST'])
def get_data():
    """
    Api Call to return the D3js object needed for visualization
    :return: 
    """
    global words
    global in_filename
    tce = TrendComparisonExample()

    return jsonify(tce.generate_data_trend(in_filename, words))


if __name__ == '__main__':
    global words
    global in_filename
    parser = argparse.ArgumentParser(
        description='''Creates data for visualizing Trend Comparison.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=TrendComparisonExample().DEF_INFILENAME,
                        help='Name of the input file containing tweets')
    parser.add_argument('-w', nargs="*", default=["#nypd", "#ows"],
                        help='Words for spark line chart')

    argsi = parser.parse_args()

    # Get the file name containing the tweets from the command line argument
    in_filename = argsi.i

    # Get the words for trend comparison from the command line argument
    words = argsi.w

    # Run the flask app on port 5008
    app.run(port=5008)
