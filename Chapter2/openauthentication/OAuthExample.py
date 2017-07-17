#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Creates user access token and secret and saves it into config.json. Also verifies the key.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""

import os
import urlparse
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(''))))
import oauth2 as oauth
import requests
from Chapter2.support.Config import Config
from Chapter2.support.OAuthTokenSecret import OAuthTokenSecret
import argparse


class OAuthExample(object):
    def __init__(self):
        self.confObj = Config(os.path.realpath('../../') + '/')
        self.config = self.confObj.data
        self.user_access_token = self.config['user_access_token']
        self.user_access_secret = self.config['user_access_secret']
        self.consumer_key = self.config['consumer_key']
        self.consumer_secret = self.config['consumer_secret']
        self.authObj = ""
        self.worked = False

        while not self.test_o_auth():
            self.get_user_access_key_secret()
        self.worked = True

    def test_o_auth(self):
        """
        If the keys worked or not.
        :rtype: bool
        """
        self.authObj = OAuthTokenSecret(self.consumer_key,
                                        self.consumer_secret, self.user_access_token,
                                        self.user_access_secret)
        r = requests.get(url='https://api.twitter.com/1.1/users/show.json?screen_name=anjoy92'
                         , auth=self.authObj.auth)

        return not r.json().has_key('errors')

    def get_user_access_key_secret(self):
        """
        Method to request for keys.
        :return: None
        """
        consumer_key = self.consumer_key
        consumer_secret = self.consumer_secret

        request_token_url = \
            'https://api.twitter.com/oauth/request_token'
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        authorize_url = 'https://api.twitter.com/oauth/authorize'

        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)

        # Step 1: Get a request token. This is a temporary token that is used for
        # having the user authorize an access token and to sign the request to obtain
        # said access token.

        (resp, content) = client.request(request_token_url, 'GET')
        if resp['status'] != '200':
            raise Exception('Invalid response %s.' % resp['status'])

        request_token = dict(urlparse.parse_qsl(content))

        print 'Request Token:'
        print '    - oauth_token        = %s' \
              % request_token['oauth_token']
        print '    - oauth_token_secret = %s' \
              % request_token['oauth_token_secret']
        print

        # Step 2: Redirect to the provider. Since this is a CLI script we do not
        # redirect. In a web application you would redirect the user to the URL
        # below.

        print 'Go to the following link in your browser:'
        print '%s?oauth_token=%s' % (authorize_url,
                                     request_token['oauth_token'])
        print

        # After the user has granted access to you, the consumer, the provider will
        # redirect you to whatever URL you have told them to redirect to. You can
        # usually define this in the oauth_callback argument as well.

        accepted = 'n'
        while accepted.lower() == 'n':
            accepted = raw_input('Have you authorized me? (y/n) ')
        oauth_verifier = raw_input('What is the PIN? ')

        # Step 3: Once the consumer has redirected the user back to the oauth_callback
        # URL you can request the access token the user has approved. You use the
        # request token to sign this request. After this is done you throw away the
        # request token and use the access token returned. You should store this
        # access token somewhere safe, like a database, for future use.

        token = oauth.Token(request_token['oauth_token'],
                            request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)

        (resp, content) = client.request(access_token_url, 'POST')
        access_token = dict(urlparse.parse_qsl(content))

        print 'Access Token:'
        print '    - oauth_token        = %s' \
              % access_token['oauth_token']
        print '    - oauth_token_secret = %s' \
              % access_token['oauth_token_secret']
        print
        print 'You may now access protected resources using the access tokens above.'
        print

        self.user_access_token = access_token['oauth_token']
        self.user_access_secret = access_token['oauth_token_secret']
        self.config['user_access_token'] = access_token['oauth_token']
        self.config['user_access_secret'] = \
            access_token['oauth_token_secret']
        self.confObj.Write()


def main(args):
    """
    Creates user access token and secret and save into config.json. Also verifies the key.
    """
    parser = argparse.ArgumentParser(
        description='''Creates user access token and secret and saves it into config.json. Also verifies the key.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    argsi = parser.parse_args()
    lte = OAuthExample()
    if lte.worked:
        print "Key is good and saved inside config.json"


if __name__ == "__main__":
    main(sys.argv)
