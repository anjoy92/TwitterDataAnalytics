#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Class to clean and tokenize tweets
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import re


class TextUtils(object):
    def __init__(self):
        self.STOPWORDS = set()
        self.SEPARATOR = " "

    def load_stop_words(self, filename):
        if not filename:
            return
        with open(filename) as fp:
            for line in fp:
                map(lambda x: self.STOPWORDS.add(x), line.split(','))

    def tokenize_text(self, text, ignore_hashtags, ignore_usernames):
        tokens = text.split(self.SEPARATOR)
        words = {}
        for token in tokens:
            token = re.sub("\"|'|\\.||;|,", "", token)
            if not token or len(token) <= 2 or token in self.STOPWORDS or token.startswith("&") or token.endswith(
                    "http"):
                continue
            else:
                if ignore_hashtags:
                    if token.startswith("#"):
                        continue
                if ignore_usernames:
                    if token.startswith("@"):
                        continue
                if token in words:
                    words[token] = words[token] + 1
                else:
                    words[token] = 1
        return words

    def is_tweet_rt(self, text):
        if re.search("^rt @[a-z_0-9]+", text):
            return True
        else:
            return False

    def contains_url(self, text):
        if re.search("https?://[a-zA-Z0-9\\./]+", text):
            return True
        else:
            return False

    def get_hash_tags(self, text):
        return re.findall("#[a-zA-Z0-9]+", text)

    def get_clean_text(self, text):
        text = re.sub("'|\"|&quot;", "", text)
        text = re.sub("\\\\", "", text)
        text = re.sub("\r\n|\n|\r", "", text)
        return text.strip()

    def remove_rt_elements(self, tweet):
        text = re.sub("rt @[a-z_A-Z0-9]+", " ", tweet)
        text = re.sub("RT @[a-z_A-Z0-9]+", " ", text)
        text = re.sub(":", "", text)
        return text.strip()

    def remove_twitter_elements(tweet):

        temp_tweet = re.sub("#[a-zA-Z_0-9]+", "", tweet)
        temp_tweet = re.sub("https?://[a-zA-Z0-9\\./]+", "", temp_tweet)
        temp_tweet = re.sub("@[a-zA-Z_0-9]+", "", temp_tweet)
        temp_tweet = re.sub("[:?\\.;<>()]", "", temp_tweet)
        return temp_tweet
