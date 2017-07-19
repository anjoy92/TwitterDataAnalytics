#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Fetches tweets matching a query and writes to file.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
import urllib
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import time
from Chapter2.openauthentication.OAuthExample import OAuthExample
from Chapter2.support.APIType import APIType
import requests


class RESTSearchExample(object):
    def __init__(self):
        """
        Initialize variables
        """
        self.out_file_writer = ""
        self.query = "#protest"
        self.DEF_FILENAME = "searchresults.json"

    def load_twitter_token(self):
        """
        Initialize the oauth token using the OAuthExample class
        """
        self.o_auth_tokens = OAuthExample()

    def initialize_writers(self, filename):
        """
        Initialize Writer
        :param filename: the output file name
        """
        self.out_file_writer = open(filename, "w+")

    def get_rate_limit_status(self):
        """
        Retrieves the rate limit status of the application
        :return: rate limit object
        :rtype: json
        """
        r = requests.get(url="https://api.twitter.com/1.1/application/rate_limit_status.json",
                         auth=self.o_auth_tokens.authObj.auth)
        return r.json()

    def get_wait_time(self, api):
        """
        Retrieves the wait time if the API Rate Limit has been hit
        :param api the name of the API currently being used
        :return the number of milliseconds to wait before initiating a new request
        :rtype: int
        """
        # Make the Get call to get the rate limit json object.
        jobj = self.get_rate_limit_status()
        if jobj != None:
            # The rate limits are under resources key.
            if 'resources' in jobj:
                resources_obj = jobj["resources"]
                api_limit = None
                # Find the rate limit according to the
                # type of call we need to make.
                if api == APIType().USER_TIMELINE:
                    status_obj = resources_obj["statuses"]
                    api_limit = status_obj[api]
                elif api == APIType().FOLLOWERS:
                    followers_obj = resources_obj["followers"]
                    api_limit = followers_obj[api]
                elif api == APIType().FRIENDS:
                    friends_obj = resources_obj["friends"]
                    api_limit = friends_obj[api]
                elif api == APIType().USER_PROFILE:
                    user_obj = resources_obj["users"]
                    api_limit = user_obj[api]

                # Get the number of call left and if less than 1 get the reset time.
                num_rem_hits = api_limit["remaining"]
                if num_rem_hits <= 1:
                    reset_time = api_limit["reset"]
                    # Get the reset time from the reply object and
                    # make the program go to sleep for that amount of time.
                    # The time is in format of unix time stamp so we are subracting
                    # from the current unix time to get the wait time.
                    print "Going to sleep for " + str(reset_time - int(time.time())) + " seconds "
                    return reset_time - int(time.time())
        return 0

    def get_search_results(self, query):
        """
        Fetches tweets matching a query
        :param query for which tweets need to be fetched
        :return an array of status objects
        :rtype: json
        """
        # Make the Get request with q parameter to put the search query and count (number of results)
        r = requests.get(
            url="https://api.twitter.com/1.1/search/tweets.json?q=" + urllib.quote(query.encode('utf8')) + "&count=100",
            auth=self.o_auth_tokens.authObj.auth)

        # Check for any error
        if r.status_code == 400 or r.status_code == 404 or r.status_code == 429:
            time.sleep(self.get_wait_time("/friends/list"))
        elif r.status_code == 500 or r.status_code == 502 or r.status_code == 503:
            print r.content
            # Sleep for sime time for these status codes and try again
            time.sleep(2)

        # Return the result
        return r.json()

    def create_or_query(self,query_terms):
        """
        Create the query string by concatenating all the terms given with or clause.
        :param query_terms: list containing query terms
        :return: query string
        """
        query_string = " OR ".join(query_terms)
        return query_string

    def write_to_file(self, data):
        """
        Writes the data given to the output file defined
        :param data: 
        """
        self.out_file_writer.write(json.dumps(data, indent=4, sort_keys=True))
        self.out_file_writer.write("\n\n")


def main(args):
    rse = RESTSearchExample()

    parser = argparse.ArgumentParser(
        description='''Fetches tweets matching a query and writes to file.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-o', nargs="?", default=rse.DEF_FILENAME,
                        help='Name of the output file for saving result')
    parser.add_argument('-q', nargs="*", default=[rse.query],
                        help="Query terms for searching, example: python RESTSearchExample.py -q '#president' '#usa' 'uk'")
    argsi = parser.parse_args()

    # Get the query terms from the command line argument
    query_terms = argsi.q

    # Get the output file name from the command line argument
    outfile_name = argsi.o

    print "Query Terms: ",query_terms

    # Load the oauth object
    rse.load_twitter_token()

    # Print the rate limit status
    print json.dumps(rse.get_rate_limit_status(), indent=4, sort_keys=True)

    # Initialize the Writer
    rse.initialize_writers(outfile_name)

    # Get the search result
    results = rse.get_search_results(rse.create_or_query(query_terms))
    print json.dumps(results, indent=4, sort_keys=True)

    # Write the result to the output file
    rse.write_to_file(results)

    print "\nResult Written to ", outfile_name


if __name__ == "__main__":
    main(sys.argv[1:])
