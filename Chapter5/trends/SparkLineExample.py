#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Creates Spark Line data for visualization from the tweet file provided.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path

from Chapter5.trends.TCDateInfo import TCDateInfo

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import datetime
from Chapter5.support.DateInfo import DateInfo
from flask import json, render_template, send_from_directory, jsonify, request
from flask import Flask
app = Flask(__name__ ,static_folder='../static')

@app.route('/')
def hello_world():
   return send_from_directory('../templates/','SparkLineExample.html')

class SparkLineExample(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.SDM = "%d %b %Y %H"

    def generate_data_trend(self, in_filename, keywords):
        result = {}
        datecount = {}
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
                            wordcount[word] += 1
                        else:
                            wordcount[word] = 1
                        datecount[strdate] = wordcount
        dinfos = []
        keys = set(datecount.keys())
        print len(keys)
        for key in keys:
            dinfo = TCDateInfo()
            dinfo.d = datetime.datetime.strptime(key, self.SDM)
            dinfo.wordcount = datecount[key]
            dinfos.append(dinfo)
        dinfos.sort()
        tseriesvals = []
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
                counter += 1
        counter = 0

        for word in keywords:
            result[word] = tseriesvals[counter]
            counter += 1

        return result

@app.route('/getData', methods=['GET', 'POST'])
def getData():
    global in_filename
    sle = SparkLineExample()

    words = argsi.w

    return jsonify(sle.generate_data_trend(in_filename, words))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Creates Spark Line data for visualization from the tweet file provided.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=SparkLineExample().DEF_INFILENAME,
                        help='Name of the input file containing tweets')
    parser.add_argument('-w', nargs="*", default=["#nypd", "#ows", "zuccotti", "protest"],
                        help='Words for spark line chart')

    argsi = parser.parse_args()

    in_filename = argsi.i
    app.run(port=5007)
