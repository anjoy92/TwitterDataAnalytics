from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from collections import OrderedDict
import networkx as nx
import operator
import json
class TweetToGraph(object):
    def __init__(self):
        self.DEF_INFILENAME = "../bigtweet.json"
        self.graph=nx.DiGraph()
    def createRetweetNetwork(self,tweetFile):
        with open(tweetFile) as fp:
            for tweet in fp:
                tweet = json.loads(tweet)

                user = tweet["user"]["screen_name"]
                if not user:
                    continue
                if "retweeted_status" not in tweet:
                    continue
                retweet = tweet["retweeted_status"]
                retweeted_user = retweet["user"]["screen_name"]
                touser = retweeted_user
                fromuser = user
                if self.graph.has_edge(touser,fromuser):
                    weight = self.graph.get_edge_data(touser,fromuser, {"weight": 0}).get("weight", 1)
                    self.graph.add_edge(touser,fromuser, weight=weight + 1)
                else:
                    self.graph.add_edge(touser,fromuser)

    def inDegreeCentrality(self):
        return sorted(nx.in_degree_centrality(self.graph).items(), key=operator.itemgetter(1),reverse=True)

    def eigenvectorCentrality(self):
        return sorted(nx.eigenvector_centrality(self.graph).items(), key=operator.itemgetter(1),reverse=True)

    def betweennessCentrality(self):
        return sorted(nx.betweenness_centrality(self.graph).items(), key=operator.itemgetter(1),reverse=True)

    def pagerankCentrality(self):
        return sorted(nx.pagerank(self.graph).items(), key=operator.itemgetter(1),reverse=True)


