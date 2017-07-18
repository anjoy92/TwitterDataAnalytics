#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Class to parse and create Network from tweet file.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import networkx as nx
import operator
import json


class TweetToGraph(object):
    def __init__(self):
        self.DEF_INFILENAME = "../bigtweet.json"
        self.graph=nx.DiGraph()

    def create_retweet_network(self, tweetFile):
        """
        Parsing the tweets in file and creating a Networkx graph object.
        :param tweetFile: Name of the file containing tweets
        """
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
                from_user = retweeted_user
                to_user = user
                if self.graph.has_edge(to_user,from_user):
                    weight = self.graph.get_edge_data(to_user,from_user, {"weight": 0}).get("weight", 1)
                    self.graph.add_edge(to_user,from_user, weight=weight + 1)
                else:
                    self.graph.add_edge(to_user,from_user)

    def in_degree_centrality(self):
        """
        In degree centrality calculation using Networkx function.
        :return: JSON object having in degree centrality
        :rtype: JSON
        """
        return sorted(nx.in_degree_centrality(self.graph).items(), key=operator.itemgetter(1),reverse=True)

    def eigen_vector_centrality(self):
        """
        Eigenvector centrality calculation using Networkx function.
        :return: JSON object having in eigenvector centrality
        :rtype: JSON
        """
        return sorted(nx.eigenvector_centrality(self.graph).items(), key=operator.itemgetter(1),reverse=True)

    def betweenness_centrality(self):
        """
        Betweenness centrality calculation using Networkx function.
        :return: JSON object having betweenness centrality
        :rtype: JSON
        """
        return sorted(nx.betweenness_centrality(self.graph).items(), key=operator.itemgetter(1),reverse=True)

    def pagerank_centrality(self):
        """
        Pagerank degree centrality calculation using Networkx function.
        :return: JSON object having pagerank centrality
        :rtype: JSON
        """
        return sorted(nx.pagerank(self.graph).items(), key=operator.itemgetter(1),reverse=True)


