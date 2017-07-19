#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ =  "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""


class APIType(object):
    def __init__(self):

        # Twitter Rest Api strings for getting the rate limit info
        # from the object returned from rate limit api call
        self.USER_TIMELINE = "/statuses/user_timeline"
        self.FOLLOWERS = "/followers/list"
        self.FRIENDS = "/friends/list"
        self.USER_PROFILE = "/users/show"