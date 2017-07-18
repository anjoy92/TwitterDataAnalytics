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

    infile_name = argsi.i

    ttg.create_retweet_network(infile_name)
    print ttg.graph
    G = ttg.graph
    nodes = {}
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
    weights = [int(nodes[i]) for i in nodes]
    # d = nx.degree(G)
    pos = nx.spring_layout(G)
    normalized = [float(i) * 1000 / sum(weights) for i in weights]
    nx.draw_networkx(G, pos, nodelist=nodes.keys(), node_size=normalized)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
