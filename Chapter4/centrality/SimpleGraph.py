#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Creates a simple retweeted graph network from the json file provided. 
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
        description='''Creates a simple retweeted graph network from the json file provided. ''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default="../simplegraph.json",
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    # Get the input file name containing tweets from the command line argument
    infile_name = argsi.i

    # Create the tweet network using Networkx library from the tweet file mentioned
    ttg.create_retweet_network(infile_name)

    # Print the Network generated.
    print ttg.graph
    G = ttg.graph

    nodes = {}

    # Traverse the full network and create a nodes dictionary having key as the node name
    # and value as the number of times it has occurred in the network.
    # We are doing this to assign the size of the node according to its weight/occurrence
    for (u, v, d) in G.edges(data=True):
        print u, v, d
        if u in nodes.keys():
            if 'weight' in d.keys():
                nodes[u] += d['weight']
            else:
                nodes[u] += 1
        else:
            if 'weight' in d.keys():
                nodes[u] = d['weight']
            else:
                nodes[u] = 1
        if v in nodes.keys():
            if 'weight' in d.keys():
                nodes[v] += d['weight']
            else:
                nodes[v] += 1
        else:
            if 'weight' in d.keys():
                nodes[v] = d['weight']
            else:
                nodes[v] = 1

    # Copy the nodes values/weights to the weights list
    weights = [int(nodes[i]) for i in nodes]

    # This creates the visualization network using spring layout and returns the position(x,y) of each node
    pos = nx.spring_layout(G)

    # Normalize the weights to create a good visualization. Also increase the value of 1000 to get bigger sized nodes.
    normalized = [float(i) * 1000 / sum(weights) for i in weights]

    # Draw the network using the matplotlib library. Networkx uses it internally.
    nx.draw_networkx(G, pos, nodelist=nodes.keys(), node_size=normalized)

    # Show the plotted network graph
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
