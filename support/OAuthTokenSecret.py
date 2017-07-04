from requests_oauthlib import OAuth1


class OAuthTokenSecret(object):

    def __init__(self,token,secret):
        self.consumer_key = 'L8CRRCUoRl3xcZ9bdrfUw'
        self.consumer_secret = 'PPCTObQGbGm1gkNvdJiTPKhoTksG787RTBwardkbM'

        self = OAuth1(self.consumer_key,
                       client_secret=self.consumer_secret,
                       resource_owner_key=token,
                       resource_owner_secret=secret)

