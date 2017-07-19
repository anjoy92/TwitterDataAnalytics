#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ =  "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""


class InfoType(object):
    def __init__(self):

        # API key values for the twitter Rest API for getting info about profile/follower/friends/statuses
        self.PROFILE_INFO = 0
        self.FOLLOWER_INFO = 1
        self.FRIEND_INFO = 2
        self.STATUSES_INFO = 3
