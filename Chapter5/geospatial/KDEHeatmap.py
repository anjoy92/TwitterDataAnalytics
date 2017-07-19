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
   return send_from_directory('../templates/','KDEExample.html')


@app.route('/getData', methods=['GET', 'POST'])
def getData():

    parser = argparse.ArgumentParser(
        description='''Creates Control Chart Trend data for visualization from the tweet file provided. A control chart is a statistical tool used to detect abnormal variations in a process. This task is performed by measuring the stability of the process through the use of control limits''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default='../locs.json',
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    in_filename = argsi.i

    with open(in_filename) as data_file:
        data = json.load(data_file)

    return jsonify(data)


if __name__ == '__main__':
   app.run(port=5001)