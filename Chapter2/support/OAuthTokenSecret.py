from requests_oauthlib import OAuth1
from Config import Config
from Chapter2.support import root


class OAuthTokenSecret(object):

    def __init__(self,consumer_key,consumer_secret,UserAccessToken,UserAccessSecret):

        self.auth = OAuth1(consumer_key,
               client_secret=consumer_secret,
               resource_owner_key=UserAccessToken,
               resource_owner_secret=UserAccessSecret)

