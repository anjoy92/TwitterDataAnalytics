#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""


class Tweet(object):
    def __init__(self):
        self.text=""
        self.id=0
        self.lat=0.0
        self.lng=0.0
        self.pubdate=""
        self.user=""
        self.catID=0
        self.catColor=0