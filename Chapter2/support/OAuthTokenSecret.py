#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ =  "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
from requests_oauthlib import OAuth1


class OAuthTokenSecret(object):
    def __init__(self, consumer_key, consumer_secret, user_access_token, user_access_secret):
        self.auth = OAuth1(consumer_key,
                           client_secret=consumer_secret,
                           resource_owner_key=user_access_token,
                           resource_owner_secret=user_access_secret)
