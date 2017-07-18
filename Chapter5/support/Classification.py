#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""


class Classification(object):
    def __init__(self):
        self.label=""
        self.confidence=""

    def classification(self, label, confidence):
        self.label = label
        self.confidence = confidence
        return self

    def __str__(self):
        return "(" +str(self.label) + ", " + str(self.confidence ) +")\n"