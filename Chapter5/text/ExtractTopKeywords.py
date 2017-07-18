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


class ExtractTopKeywords(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.DEF_K = 60

    @staticmethod
    def get_top_keywords(in_filename, K, ignore_hashtags, ignore_usernames, tu):
        words = {}
        with open(in_filename) as fp:
            for temp in fp:
                tweetobj = json.loads(temp)
                if "text" in tweetobj:
                    text = tweetobj["text"]
                    text = re.sub("\\s+", " ", text.lower())
                    tokens = tu.tokenize_text(text, ignore_hashtags, ignore_usernames)
                    keys = tokens.keys()
                    for key in keys:
                        if key in words:
                            words[key] = words[key] + tokens[key]
                        else:
                            words[key] = tokens[key]

        keys = set(words.keys())
        tags = []
        for key in keys:
            tag = Tags()
            tag.key = key
            tag.value = words[key]
            tags.append(tag)
        tags.sort(reverse=True)
        cloudwords = []
        numwords = K
        if len(tags) < numwords:
            numwords = len(tags)
        for i in range(numwords):
            wordfreq = {}
            tag = tags[i]
            wordfreq["text"] = tag.key
            wordfreq["size"] = tag.value
            cloudwords.append(wordfreq)
        return cloudwords


def main(args):
    etk = ExtractTopKeywords()
    tu = TextUtils()

    parser = argparse.ArgumentParser(
        description='''Creates word cloud data for visualization from the tweet file provided.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=etk.DEF_INFILENAME,
                        help='Name of the input file containing tweets')
    parser.add_argument('-s', nargs="?", default="../stopwords.txt",
                        help='Name of file containing stop words')
    parser.add_argument('-k', nargs="?", default=etk.DEF_K,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    infile_name = argsi.i
    stopwords_file = argsi.s

    tu.load_stop_words(stopwords_file)

    K = argsi.k

    print etk.get_top_keywords(infile_name, K, False, True, tu)


if __name__ == "__main__":
    main(sys.argv[1:])
