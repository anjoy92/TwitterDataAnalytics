#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Calculate InDegree Centrality from the file given
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter4.centrality.TweetToGraph import TweetToGraph
import networkx as nx
import matplotlib.pyplot as plt

def main(args):
    ttg = TweetToGraph()

    parser = argparse.ArgumentParser(
        description='''Calculate InDegree Centrality from the file given.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=ttg.DEF_INFILENAME,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    # Get the input file name containing tweets from the command line argument
    infile_name = argsi.i

    # Create the tweet network using Networkx library from the tweet file mentioned
    ttg.create_retweet_network(infile_name)

    # Calculate the indegree centrality from the tweet network
    in_degree_centrality=ttg.in_degree_centrality()

    print in_degree_centrality
    print "User\t\tCentrality"
    for obj in in_degree_centrality:
        print obj[0],"\t\t",obj[1]


if __name__ == "__main__":
    main(sys.argv[1:])