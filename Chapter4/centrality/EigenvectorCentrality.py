from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter4.centrality.TweetToGraph import TweetToGraph


def main(args):
    ttg = TweetToGraph()
    words = []
    infilename = ttg.DEF_INFILENAME

    if len(args)>0:
        infilename = args[0]

    ttg.createRetweetNetwork(infilename)
    eigenvector_centrality = ttg.eigenvectorCentrality()
    print eigenvector_centrality
    print "User\t\tCentrality"
    for obj in eigenvector_centrality:
        print obj[0],"\t\t",obj[1]


if __name__ == "__main__":
    main(sys.argv[1:])