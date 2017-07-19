#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Reads and Writes config file json object.
__author__ =  "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""

import json


class Config(object):
    def __init__(self,root):
        self.root=root

        # Opens the config file for reading the authentication keys.
        with open(self.root+'config.json') as json_data_file:
            self.data = json.load(json_data_file)

    def Write(self):
        """
        Write the config file with changed authentication keys.
        """
        with open(self.root+'config.json', 'w') as outfile:

            # Json Format the output
            outfile.write(json.dumps(self.data, indent=4, sort_keys=True))