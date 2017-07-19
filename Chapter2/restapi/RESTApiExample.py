#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
File to use Twitter REST API and get User Profile Info or Friend Info or Follower Info or Statuses Info.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path
import json
import time

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter2.openauthentication.OAuthExample import OAuthExample
from Chapter2.support.InfoType import InfoType
from Chapter2.support.APIType import APIType
import requests


class RESTApiExample(object):
    def __init__(self):
        self.DEF_FILENAME = "users.txt"
        self.DEF_OUTFILENAME = "restapiresults.json"
        self.usernames = []

    def load_twitter_token(self):
        """
        Load the User Access Token, and the User Access Secret
        """
        self.o_auth_tokens = OAuthExample()

    def get_rate_limit_status(self):
        """ 
        Retrieves the rate limit status of the application
        :return: Rate Limit json object
        :rtype: JSON
        """
        r = requests.get(url="https://api.twitter.com/1.1/application/rate_limit_status.json",
                         auth=self.o_auth_tokens.authObj.auth)
        return r.json()

    def initialize_writers(self, filename):
        """
        Initialize the file writeInitiar
        :param filename name of the file
        """
        self.out_file_writer = open(filename, "w+")

    def read_users(self, filename):
        """
        Reads the file and loads the users in the file to be crawled
        :param filename: 
        """
        with open(filename) as fp:
            for line in fp:
                self.usernames.append(line)

    def write_to_file(self, data):
        """
        Writes the retrieved data to the output file
        :param data:  containing the retrived information in JSON
        """
        self.out_file_writer.write(json.dumps(data, indent=4, sort_keys=True))
        self.out_file_writer.write("\n\n")

    def get_wait_time(self, api):
        """
        Retrieves the wait time if the API Rate Limit has been hit
        :param api the name of the API currently being used
        :return the number of milliseconds to wait before initiating a new request
        :rtype: int
        """
        # Make the Get call to get the rate limit json object.
        jobj = self.get_rate_limit_status()
        if jobj is not None:
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

    def get_profile(self, username):
        """
        Retrives the profile information of the user
        :param username the name of the user whose friends need to be fetched
        :return the profile information as a JSONObject
        :rtype: json
        """
        profile = None
        print "*******************************************************\n\n"
        print "Processing profile of " + username, "\n\n"
        flag = True

        # Make the Get request with parameter screen_name and oauth token.
        r = requests.get(url="https://api.twitter.com/1.1/users/show.json?screen_name=" + username,
                         auth=self.o_auth_tokens.authObj.auth)

        # Check if the request was successful or not.
        if r.status_code == 404 or r.status_code == 401:
            print r.content
        elif r.status_code == 500 or r.status_code == 502 or r.status_code == 503:
            print r.content
            time.sleep(3)
        elif r.status_code == 429:
            # Code 429 corresponds to failure due to rate limit. So wait for the reset time.
            time.sleep(self.get_wait_time("/users/show/:id"))
            flag = False
        if not flag:
            # recreate the connection because something went wrong the first time.
            r = requests.get(url="https://api.twitter.com/1.1/application/rate_limit_status.json",
                             auth=self.o_auth_tokens.authObj.auth)
        if flag:
            # get profile object as everything went ok.
            profile = r.json()

        return profile

    def get_friends(self, username):
        """
        Retrieves the friends of a user
        :param username the name of the user whose friends need to be fetched
        :return a list of user objects who are friends of the user
        :rtype: json
        """
        friends = []
        print "*******************************************************\n\n"
        print "Processing friends of " + username, "\n\n"
        cursor = -1
        while True:
            if cursor == 0:
                break

            # Make the Get request with parameter screen_name, cursor ( each cursor have few set of results) and oauth token.
            r = requests.get(
                url="https://api.twitter.com/1.1/friends/list.json?screen_name=" + username + "&cursor=" + str(cursor),
                auth=self.o_auth_tokens.authObj.auth)

            # Check if the request was successful or not.
            if r.status_code == 400 or r.status_code == 401:
                print r.content
            elif r.status_code == 500 or r.status_code == 502 or r.status_code == 503:
                print r.content
                time.sleep(3)
                continue
            elif r.status_code == 429:
                # Code 429 corresponds to failure due to rate limit. So wait for the reset time.
                time.sleep(self.get_wait_time("/friends/list"))
            jobj = r.json()

            # Move to the next cursor to the info of next set of Friends
            cursor = jobj["next_cursor"]
            userlist = jobj["users"]
            if len(userlist) == 0:
                break

            # Get all the friends present in this reply.
            for i in range(len(userlist)):
                friends.append(userlist[i])

        return friends

    def get_followers(self, username):
        """
        Retrieves the followers of a user
        :param username the name of the user whose followers need to be fetched
        :return a list of user objects who are followers of the user
        :rtype: json
        """
        followers = []
        print "*******************************************************\n\n"
        print "Processing followers of " + username, "\n\n"
        cursor = -1
        while True:
            if cursor == 0:
                break

            # Make the Get request with parameter screen_name, cursor ( each cursor have few set of results) and oauth token.
            r = requests.get(
                url="https://api.twitter.com/1.1/followers/list.json?screen_name=" + username + "&cursor=" + str(
                    cursor),
                auth=self.o_auth_tokens.authObj.auth)

            # Check if the request was successful or not.
            if r.status_code == 400 or r.status_code == 401:
                print r.content
            elif r.status_code == 500 or r.status_code == 502 or r.status_code == 503:
                print r.content
                time.sleep(3)
                continue
            elif r.status_code == 429:
                # Code 429 corresponds to failure due to rate limit. So wait for the reset time.
                time.sleep(self.get_wait_time("/followers/list"))
                continue
            jobj = r.json()

            # Move to the next cursor to the info of next set of Followers
            cursor = jobj["next_cursor"]
            userlist = jobj["users"]
            if len(userlist) == 0:
                break

            # Get all the followers present in this reply.
            for i in range(len(userlist)):
                followers.append(userlist[i])

        return followers

    def get_statuses(self, username):
        """
        Retrieves the statuses of a user
        :param username the name of the user whose statuses need to be fetched
        :return a list of statuses of the user
        :rtype: json
        """
        tweetcount = 200
        include_rts = True
        statuses = []
        print "*******************************************************\n\n"
        print "Processing status messages of " + username, "\n\n"
        maxid = 0
        while True:
            url = ""

            # maxid acts as cursor. It returns a set of statuses which are present after the status with maxid.
            if maxid == 0:
                # Make the url with parameter screen_name, count (number of statuses in each reply),
                # include_rts (bool to get retweets) and oauth token.
                url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&include_rts=" + str(
                    include_rts) + "&count=" + str(tweetcount)
            else:
                # Make the url with parameter screen_name, count (number of statuses in each reply),
                # include_rts (bool to get retweets), max_id (statuses after this id) and oauth token.
                url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&include_rts=" + str(
                    include_rts) + "&count=" + str(tweetcount) + "&max_id=" + str(maxid - 1)

            # Make the Get request
            r = requests.get(url=url, auth=self.o_auth_tokens.authObj.auth)

            # Check if the request was successful or not.
            if r.status_code == 400 or r.status_code == 404:
                print r.content
            elif r.status_code == 500 or r.status_code == 502 or r.status_code == 503:
                print r.content
                time.sleep(3)
                continue
            elif r.status_code == 429:
                # Code 429 corresponds to failure due to rate limit. So wait for the reset time.
                time.sleep(self.get_wait_time("/statuses/user_timeline"))
                continue
            statusarr = r.json()
            if len(statusarr) == 0:
                break

            # Get all the statuses present in this reply.
            for i in range(len(statusarr)):
                jobj = statusarr[i]
                statuses.append(jobj)
                if jobj.has_key("id"):
                    maxid = jobj["id"]

        return statuses

    def cleanup_after_finish(self):
        """
        Close the Writer
        :return: 
        """
        self.out_file_writer.close()


def main(args):

    rae = RESTApiExample()
    rae.load_twitter_token()

    parser = argparse.ArgumentParser(
        description='''File to use Twitter REST API and get User Profile Info or Friend Info or Follower Info or Statuses Info.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=rae.DEF_FILENAME,
                        help='Name of the input file, which has user names separated by new line.')
    parser.add_argument('-o', nargs="?", default=rae.DEF_OUTFILENAME,
                        help='Name of the output file for saving result')
    parser.add_argument('-a', nargs="?", default=InfoType().PROFILE_INFO,
                        help='API Code. 0 for PROFILE_INFO , 1 for FOLLOWER_INFO , 2 for FRIEND_INFO , 3 for STATUSES_INFO')
    argsi = parser.parse_args()

    rate_limit = rae.get_rate_limit_status()
    print json.dumps(rate_limit, indent=4, sort_keys=True)

    # Get the type of call to be made from command line argument.
    # API Code. 0 for PROFILE_INFO , 1 for FOLLOWER_INFO , 2 for FRIEND_INFO , 3 for STATUSES_INFO
    api_code = argsi.a

    # Get the input file name from the command line argument
    infile_name = argsi.i

    # Get the output file name from the command line argument
    outfile_name = argsi.o

    # Initialize Writer with the output file name provided.
    rae.initialize_writers(outfile_name)

    # Read the users names or twitter handle present in the file provided.
    rae.read_users(infile_name)

    # Check if the api code is valid
    if api_code != InfoType().PROFILE_INFO and api_code != InfoType().FOLLOWER_INFO and api_code != InfoType().FRIEND_INFO and api_code != InfoType().STATUSES_INFO:
        print "Invalid API type: Use 0 for Profile, 1 for Followers, 2 for Friends, and 3 for Statuses"
        return

    # If input file has users.
    if len(rae.usernames) > 0:
        # Load the oauth variable
        rae.load_twitter_token()

        # Call the particular API function as requested by the command line argument.
        for user in rae.usernames:
            if api_code == InfoType().PROFILE_INFO:
                jobj = rae.get_profile(user)
                if jobj != None and len(jobj) != 0:
                    # Print the result and write to the output file
                    print json.dumps(jobj, indent=4, sort_keys=True)
                    rae.write_to_file(jobj)
            elif api_code == InfoType().FRIEND_INFO:
                statusarr = rae.get_friends(user)
                if len(statusarr) > 0:
                    # Print the result and write to the output file
                    print json.dumps(jobj, indent=4, sort_keys=True)
                    rae.write_to_file(statusarr)
            elif api_code == InfoType().FOLLOWER_INFO:
                statusarr = rae.get_followers(user)
                if len(statusarr) > 0:
                    # Print the result and write to the output file
                    print json.dumps(statusarr, indent=4, sort_keys=True)
                    rae.write_to_file(statusarr)
            elif api_code == InfoType().STATUSES_INFO:
                statusarr = rae.get_statuses(user)
                if len(statusarr) > 0:
                    # Print the result and write to the output file
                    print json.dumps(statusarr, indent=4, sort_keys=True)
                    rae.write_to_file(statusarr)

    print "\nResult Written to ", outfile_name

    # Close the writer
    rae.cleanup_after_finish()


if __name__ == "__main__":
    main(sys.argv)
