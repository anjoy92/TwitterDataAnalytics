#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Creates data for user tag Network.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import re
from collections import Counter


class ExtractUserTagNetwork(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"

    @staticmethod
    def extract_hash_tags(text):
        return dict(Counter(map(lambda x: x.lower(), re.findall("#[a-zA-Z0-9]+", text))))

    def extract_user_hashtag_network(self, in_filename):
        user_tag_map = {}
        with open(in_filename) as fp:
            for line in fp:
                tweetobj = json.loads(line)
                text = ""
                username = ""
                tags = {}
                if "entities" in tweetobj:
                    entities = tweetobj["tweetobj"]
                    hashtags = entities["hashtags"]
                    for i in range(len(hashtags)):
                        tag = hashtags[i]
                        tg = tag["text"].lower()
                        if tg not in tags:
                            tags[tg] = 1
                        else:
                            tag[tg] = tag[tg] + 1
                else:
                    if "text" in tweetobj:
                        text = tweetobj["text"]
                        tags = self.extract_hash_tags(text)
                if "user" in tweetobj:
                    userobj = tweetobj["user"]
                    username = "@" + str(userobj["screen_name"]).lower()
                    if username in user_tag_map:
                        usertags = user_tag_map[username]
                        keys = set(tags.keys())
                        for k in keys:
                            if k in usertags:
                                usertags[k] = usertags[k] + tags[k]
                            else:
                                usertags[k] = tags[k]
                        user_tag_map[username] = usertags
                    else:
                        user_tag_map[username] = tags
        return user_tag_map


def main(args):
    eutn = ExtractUserTagNetwork()

    parser = argparse.ArgumentParser(
        description='''Creates Control Chart Trend data for visualization from the tweet file provided. A control chart is a statistical tool used to detect abnormal variations in a process. This task is performed by measuring the stability of the process through the use of control limits''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=eutn.DEF_INFILENAME,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    in_filename = argsi.i

    user_tag_map = eutn.extract_user_hashtag_network(in_filename)

    keys = set(user_tag_map.keys())
    print len(keys)
    for key in keys:
        print key
        tags = user_tag_map[key]
        tagkeys = set(tags.keys())
        for tag in tagkeys:
            print str(tag) + "," + str(tags[tag])


if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
