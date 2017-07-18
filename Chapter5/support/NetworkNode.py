#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""


class NetworkNode(object):
    def __init__(self):
        self.id=0
        self.username = ""
        self.size=0
        self.catColor=""
        self.group=""
        self.clusterID=0
        self.catID=0
        self.lat=0
        self.lng=0
        self.data=[]
        self.level=0
        self.class_codes=[]
        self.tonodes=[]
