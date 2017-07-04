import os

import requests
import oauth2 as oauth
import urlparse

from requests_oauthlib import OAuth1

from support.Config import Config
from support.Constants import consumer_key,consumer_secret
from support.OAuthTokenSecret import OAuthTokenSecret


class OAuthExample(object):

    def __init__(self):
        self.confObj= Config(os.path.abspath("../../")+"/")
        self.config= self.confObj.data
        self.UserAccessToken = self.config['UserAccessToken']
        self.UserAccessSecret = self.config['UserAccessSecret']
        self.consumer_key = self.config['consumer_key']
        self.consumer_secret = self.config['consumer_secret']
        if not self.TestOAuth():
            self.GetUserAccessKeySecret()
            self.TestOAuth()

    def TestOAuth(self):
        au=OAuth1(self.consumer_key,
               client_secret=self.consumer_secret,
               resource_owner_key=self.UserAccessToken,
               resource_owner_secret=self.UserAccessSecret)
        r = requests.get(url="https://api.twitter.com/1.1/users/show.json?screen_name=anjoy92", auth=au)
        print r.json()
        return not r.json().has_key('errors')

    def GetUserAccessKeySecret(self):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        consumer_key = self.consumer_key
        consumer_secret = self.consumer_secret

        request_token_url = 'https://api.twitter.com/oauth/request_token'
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        authorize_url = 'https://api.twitter.com/oauth/authorize'

        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)

        # Step 1: Get a request token. This is a temporary token that is used for
        # having the user authorize an access token and to sign the request to obtain
        # said access token.

        resp, content = client.request(request_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        request_token = dict(urlparse.parse_qsl(content))

        print "Request Token:"
        print "    - oauth_token        = %s" % request_token['oauth_token']
        print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
        print

        # Step 2: Redirect to the provider. Since this is a CLI script we do not
        # redirect. In a web application you would redirect the user to the URL
        # below.

        print "Go to the following link in your browser:"
        print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
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

        resp, content = client.request(access_token_url, "POST")
        access_token = dict(urlparse.parse_qsl(content))

        print "Access Token:"
        print "    - oauth_token        = %s" % access_token['oauth_token']
        print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
        print
        print "You may now access protected resources using the access tokens above."
        print

        self.UserAccessToken = access_token['oauth_token']
        self.UserAccessSecret = access_token['oauth_token_secret']
        self.config['UserAccessToken'] = access_token['oauth_token']
        self.config['UserAccessSecret'] = access_token['oauth_token_secret']
        self.confObj.Write()

obj=OAuthExample()
