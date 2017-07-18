#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Calculate Eigenvector Centrality from the file given
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter4.centrality.TweetToGraph import TweetToGraph


def main(args):
    ttg = TweetToGraph()

    parser = argparse.ArgumentParser(
        description='''Calculate Eigenvector Centrality from the file given. ''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=ttg.DEF_INFILENAME,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    infile_name = argsi.i

    ttg.create_retweet_network(infile_name)
    eigenvector_centrality = ttg.eigen_vector_centrality()

    print eigenvector_centrality
    print "User\t\tCentrality"
    for obj in eigenvector_centrality:
        print obj[0],"\t\t",obj[1]


if __name__ == "__main__":
    main(sys.argv[1:])