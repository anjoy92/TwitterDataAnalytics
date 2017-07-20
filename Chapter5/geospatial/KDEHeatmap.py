#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Creates Heat Map Flask/Web application for visualization from the locations file provided. A control chart is a statistical tool used to detect abnormal variations in a process. This task is performed by measuring the stability of the process through the use of control limits
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path

import math

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
from flask import json, send_from_directory, jsonify
from flask import Flask
app = Flask(__name__ ,static_folder='../static')

@app.route('/')
def hello_world():
    """
    Returns the  KDEExample HTML file as First page.
    The JS file being used for this page is: kernelDE.js and mapWidget.js
    The CSS file being used for this page is: mapstyle.css
    :return: The page to be rendered
    """
    return send_from_directory('../templates/','KDEExample.html')


@app.route('/getData', methods=['GET', 'POST'])
def get_data():
    """
    Api Call to return the D3js object needed for visualization
    :return: 
    """
    parser = argparse.ArgumentParser(
        description='''Creates Control Chart Trend data for visualization from the locations file provided. A control chart is a statistical tool used to detect abnormal variations in a process. This task is performed by measuring the stability of the process through the use of control limits''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default='../locs.json',
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    # Get the file name containing the locations from the command line argument
    in_filename = argsi.i

    # Load the file as json object
    with open(in_filename) as data_file:
        data = json.load(data_file)

    # Return the data
    return jsonify(data)


if __name__ == '__main__':
    # Start the flask app on port 5001
    app.run(port=5001)