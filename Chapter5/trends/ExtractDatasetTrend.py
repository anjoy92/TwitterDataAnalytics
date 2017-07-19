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
   return send_from_directory('../templates/','TrendLineExample.html')


class ExtractDatasetTrend(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.SDM = "%d %b %Y %H:%M"

    def generate_data_trend(self, inFilename):
        result = []
        datecount = {}
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


@app.route('/getData', methods=['GET', 'POST'])
def getData():
    edt = ExtractDatasetTrend()

    parser = argparse.ArgumentParser(
        description='''Creates Simple Trend Line data for visualization from the tweet file provided.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=edt.DEF_INFILENAME,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    in_filename = argsi.i

    return jsonify(edt.generate_data_trend(in_filename))


if __name__ == '__main__':
   app.run()
