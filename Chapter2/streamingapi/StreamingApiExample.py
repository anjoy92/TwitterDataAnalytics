#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Fetches tweets matching query mentioned in the file and writes to output directory where each file contains -n numbers of tweets
__author__ =  "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
import os
import urllib
from os import sys, path
import time

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter2.openauthentication.OAuthExample import OAuthExample
import requests


class StreamingApiExample(object):
    def __init__(self):
        # Initialize the variables

        # Number of tweets to write to each output file.
        self.RECORDS_TO_PROCESS = 1000

        # Number of keywords allowed by the twitter API
        self.MAX_KEYWORDS = 400

        # Number of users allowed by the twitter API
        self.MAX_USERS = 5000

        # Number of geoboxes allowed by the twitter API
        self.MAX_GEOBOXES = 25

        # List of Keywords
        self.keywords = []

        # List of geoboxes
        self.geo_boxes = []

        # List of users
        self.user_ids = []

        # Location of the config file
        self.CONFIG_FILE_PATH = "streaming/streaming.config"

        # Location of the directory where the tweets file will be saved
        self.DEF_OUTPATH = "streaming/"
        self.print_number = False

    def load_twitter_token(self):
        """
        Loads the Twitter access token and secret for a user
        """
        self.o_auth_tokens = OAuthExample()

    def read_parameters(self, filename):
        """
        Reads the file and loads the parameters to be crawled. Expects that the parameters are tab separated values and the
        :param filename
        """
        count = 1
        with open(filename) as fp:
            for line in fp:
                # Read the Parameters on each line and restrict the input the twitter api restriction values
                if count == 1:
                    temp = [word.strip() for word in line.split("\t")]
                    self.keywords = list(set(temp[:self.MAX_KEYWORDS]))
                if count == 2:
                    temp = [word.strip() for word in line.split("\t")]
                    self.geo_boxes = list(set(temp[:self.MAX_GEOBOXES]))
                if count == 3:
                    temp = [word.strip() for word in line.split("\t")]
                    self.user_ids = list(set(temp[:self.MAX_USERS]))
                count = count + 1

    def create_streaming_connection(self, url, filename):
        """
        Creates a connection to the Streaming Filter API
        :param url the URL for Twitter Filter API
        :param filename Location to place the exported file
        """
        print 'Keywords:',self.keywords
        print 'GeoBoxes:',self.geo_boxes
        print 'User Ids:',self.user_ids

        # Make the post Streaming request with the parameters track for keywords,
        # locations for geoboxes and follow for user ids to track
        r = requests.post(url=url,
                          auth=self.o_auth_tokens.authObj.auth, data=urllib.urlencode(
                {'track': self.keywords, 'locations': self.geo_boxes, 'follow': self.user_ids}, doseq=True),
                          stream=True)

        raw_tweets = []
        no_of_tweets_uploaded = 0
        print "Streaming..."

        # This loops runs Infinitely till the connection is active the streaming api.
        # This connection is continuously listening/waiting for tweets and
        # whenever twitter pushes tweets this loop iterates.
        for con in r.iter_lines():

            # Append the result to the list of tweets
            raw_tweets.append(con)

            if self.print_number:
                print len(raw_tweets)

            # If the number of tweets crosses the RECORDS_TO_PROCESS value,
            # all the tweets are written to a file with name: tweets_timestamp.json
            # and the raw_tweet object is cleared for the next iteration
            if len(raw_tweets) >= self.RECORDS_TO_PROCESS:
                no_of_tweets_uploaded = no_of_tweets_uploaded + self.RECORDS_TO_PROCESS
                outFl = filename + "tweets_" + str(time.time()) + ".json"
                print "Writing " + str(self.RECORDS_TO_PROCESS) + " number of tweets to " + outFl
                with open(outFl, 'w') as outfile:
                    outfile.write("\n".join(raw_tweets))
                print "Written " + str(no_of_tweets_uploaded) + " records so far"
                raw_tweets = []


def main(args):

    # Create the class object
    sae = StreamingApiExample()

    parser = argparse.ArgumentParser(
        description='''Fetches tweets matching query mentioned in the file and writes to output directory where each file contains -n numbers of tweets''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=sae.CONFIG_FILE_PATH,
                        help="Name of the input file having the filter queries. The file should be of format:\nKeywords sepreated by tab\nGeoboxes seperated by tab and coordinates seperated by ','\nFollow userid's seperated by tab\nExample:\n#morsi	#egypt	#tahrir	#june30	#scaf\n-118.79,32.49,15.23,34.67\n15127356	20627637")
    parser.add_argument('-o', nargs="?", default=sae.DEF_OUTPATH,
                        help='Output directory for saving results')
    parser.add_argument('-n', nargs="?", default=sae.RECORDS_TO_PROCESS,
                        help='Number of Tweets to process and write to each file')
    parser.add_argument('-d', action='store_true',
                        help='Use to see the counter of the tweet being received from the twitter streaming api')

    argsi = parser.parse_args()

    # Get the name of the input file from the command line argument
    file_name = argsi.i

    # Get the name of the output directory from the command line argument
    outfile_path = argsi.o

    # Get the name of the RECORDS_TO_PROCESS value from the command line argument
    sae.RECORDS_TO_PROCESS = int(argsi.n)
    if argsi.d:
        sae.print_number = True

    # Load the oauth object
    sae.load_twitter_token()

    # Read the query parameters for the filter api from the input file mentioned
    sae.read_parameters(file_name)

    # Create the connection, start streaming and writing these tweet files to the directory mentioned
    sae.create_streaming_connection("https://stream.twitter.com/1.1/statuses/filter.json", outfile_path)


if __name__ == "__main__":
    main(sys.argv)
