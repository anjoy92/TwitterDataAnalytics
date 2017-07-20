#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ =  "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""


class Location(object):

    def __init__(self,lat,lng):
        self.latitude = float(lat)
        self.longitude = float(lng)

    def __str__(self):
        return "Latitude: " + str(self.latitude) + " & Longitude: " + str(self.longitude)+"\n"+\
               "Use this url to look up on Google Maps:\n"+\
               "https://www.google.com/maps/search/?api=1&query="+str(self.latitude)+","+str(self.longitude)