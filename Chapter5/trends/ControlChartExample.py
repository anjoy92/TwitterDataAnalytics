#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Creates Control Chart Trend data for visualization from the tweet file provided. A control chart is a statistical tool used to detect abnormal variations in a process. This task is performed by measuring the stability of the process through the use of control limits
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path

import math

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import datetime
from Chapter5.support.DateInfo import DateInfo
from flask import json, render_template, send_from_directory, jsonify, request
from flask import Flask
app = Flask(__name__ ,static_folder='../static')

@app.route('/')
def hello_world():
   return send_from_directory('../templates/','ControlChartExample.html')


class ControlChartExample(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.SDM = "%d %b %Y %H:%M"

    def generate_data_trend(self, in_filename):
        datecount = {}
        result = []
        with open(in_filename) as fp:
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
        mean = self.get_mean(dinfos)
        stddev = self.get_standard_dev(dinfos, mean)
        dinfos.sort(reverse=True)
        for dinfo in dinfos:
            jobj = {}
            jobj["date"] = dinfo.d.strftime(self.SDM)
            jobj["count"] = ((dinfo.count - mean) / stddev)
            jobj["mean"] = 0
            jobj["stdev+3"] = 3
            jobj["stdev-3"] = -3
            result.append(jobj)
        return result

    def get_standard_dev(self,dateinfos, mean):
        intsum = 0
        numperiods = len(dateinfos)
        for dinfo in dateinfos:
            intsum += math.pow((dinfo.count - mean), 2)
        return math.sqrt(float(intsum) / numperiods)

    def get_mean(self, date_infos):
        num_periods = len(date_infos)
        sum = 0
        for dinfo in date_infos:
            sum += dinfo.count
        return float(sum) / num_periods

@app.route('/getData', methods=['GET', 'POST'])
def getData():
    global in_filename
    cce = ControlChartExample()

    return jsonify(cce.generate_data_trend(in_filename))


if __name__ == '__main__':
    global in_filename

    parser = argparse.ArgumentParser(
        description='''Creates Control Chart Trend data for visualization from the tweet file provided. A control chart is a statistical tool used to detect abnormal variations in a process. This task is performed by measuring the stability of the process through the use of control limits''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=ControlChartExample().DEF_INFILENAME,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    in_filename = argsi.i
    app.run(port=5005)