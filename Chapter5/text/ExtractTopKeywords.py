#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Creates word cloud data for visualization from the tweet file provided.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import re
from utils.TextUtils import TextUtils
from utils.Tags import Tags
from flask import json, render_template, send_from_directory, jsonify, request
from flask import Flask
app = Flask(__name__ ,static_folder='../static')
@app.route('/')
def hello_world():
    """
    Returns the  WordCloudExample HTML file as First page.
    The JS file being used for this page is: wordCloud.js
    The CSS file being used for this page is: wordCloud.css
    :return: The page to be rendered
    """
    return send_from_directory('../templates/','WordCloudExample.html')


class ExtractTopKeywords(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.DEF_K = 40

    def get_top_keywords(self,in_filename, K, ignore_hashtags, ignore_usernames, tu):
        """
        Gets top keywords from the tweet file.
        :param in_filename: name of the input tweet file.
        :param K: number of words
        :param ignore_hashtags: True to ignore hastags
        :param ignore_usernames: True to ignore usernames
        :param tu: TupleUtil class object
        :return: list of dictionary with keys text and size
        """
        words = {}
        # Traverse the tweet file and count the words.
        with open(in_filename) as fp:
            for temp in fp:
                tweetobj = json.loads(temp)
                if "text" in tweetobj:
                    text = tweetobj["text"]
                    text = re.sub("\\s+", " ", text.lower())

                    # Get the token by using TupleUtil class object tu
                    tokens = tu.tokenize_text(text, ignore_hashtags, ignore_usernames)
                    keys = tokens.keys()

                    # Increment the count if the word already exists
                    for key in keys:
                        if key in words:
                            words[key] = words[key] + tokens[key]
                        else:
                            words[key] = tokens[key]

        # Get all words and create tag class object from it.
        keys = set(words.keys())
        tags = []
        for key in keys:
            tag = Tags()
            tag.key = key
            tag.value = words[key]
            tags.append(tag)

        # Sort the tags
        tags.sort(reverse=True)
        cloudwords = []
        numwords = K

        # Reduce K if the number of words are less than K
        if len(tags) < numwords:
            numwords = len(tags)

        # Take K words and create the list of dictionary object for D3js Library
        for i in range(numwords):
            wordfreq = {}
            tag = tags[i]
            wordfreq["text"] = tag.key
            wordfreq["size"] = tag.value/80
            cloudwords.append(wordfreq)

        return cloudwords


@app.route('/getData', methods=['GET', 'POST'])
def get_data():
    global infile_name
    global stopwords_file
    global K

    etk = ExtractTopKeywords()
    tu = TextUtils()

    # Load the stop words
    tu.load_stop_words(stopwords_file)

    return jsonify(etk.get_top_keywords(infile_name, K, False, True, tu))

if __name__ == "__main__":
    global infile_name
    global stopwords_file
    global K

    parser = argparse.ArgumentParser(
        description='''Creates word cloud data for visualization from the tweet file provided.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=ExtractTopKeywords().DEF_INFILENAME,
                        help='Name of the input file containing tweets')
    parser.add_argument('-s', nargs="?", default="../stopwords.txt",
                        help='Name of file containing stop words')
    parser.add_argument('-k', nargs="?", default=ExtractTopKeywords().DEF_K,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    # Get the file name containing the tweets from the command line argument
    infile_name = argsi.i

    # Get the file name containing the stop words from the command line argument
    stopwords_file = argsi.s

    # Get the number of words from the command line argument
    K = argsi.k

    # Start the flask app on port 5004
    app.run(port=5004)
