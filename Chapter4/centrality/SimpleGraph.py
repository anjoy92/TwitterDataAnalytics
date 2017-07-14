from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter4.centrality.TweetToGraph import TweetToGraph
import networkx as nx
import matplotlib.pyplot as plt

def main(args):
    ttg = TweetToGraph()
    infilename = "../simplegraph.json"

    if len(args)>0:
        infilename = args[0]

    ttg.createRetweetNetwork(infilename)

    G = ttg.graph
    weights = [ ttg.graph.get_edge_data(u,v, {"weight": 0}).get("weight", 1) for (u, v, d) in G.edges(data=True)]
    d = nx.degree(G)
    pos = nx.spring_layout(G)
    print G.edges(data=True)
    normalized = [float(i) *200/ sum(weights) for i in weights]
    nx.draw_networkx(G,pos, nodelist=d.keys(), node_size=normalized)
    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])