import oauth2 as oauth
import json

CONSUMER_KEY = "your app's consumer key"
CONSUMER_SECRET = "your app's consumer secret"
ACCESS_KEY = "your access token"
ACCESS_SECRET = "your access token secret"

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

timeline_endpoint = "https://api.twitter.com/1.1/statuses/home_timeline.json"
response, data = client.request(timeline_endpoint)

tweets = json.loads(data)
for tweet in tweets:
    print tweet['text']