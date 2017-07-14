from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter4.centrality.TweetToGraph import TweetToGraph
import networkx as nx
import matplotlib.pyplot as plt

def main(args):
    ttg = TweetToGraph()
    infilename = ttg.DEF_INFILENAME

    if len(args)>0:
        infilename = args[0]

    ttg.createRetweetNetwork(infilename)
    in_degree_centrality=ttg.inDegreeCentrality()
    print in_degree_centrality
    print "User\t\tCentrality"
    for obj in in_degree_centrality:
        print obj[0],"\t\t",obj[1]


if __name__ == "__main__":
    main(sys.argv[1:])