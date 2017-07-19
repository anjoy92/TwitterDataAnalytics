#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Create D3 network data from the file give.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
import math
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter5.support.HashTagDS import HashTagDS
from Chapter5.support.NetworkNode import NetworkNode
from Chapter5.support.ToNodeInfo import ToNodeInfo
from Chapter5.support.Tweet import Tweet
from utils.TextUtils import TextUtils
import re
from flask import json, render_template, send_from_directory, jsonify, request
from flask import Flask
app = Flask(__name__ ,static_folder='../static')

@app.route('/')
def hello_world():
   return send_from_directory('../templates/','RetweetNetworkExample.html')


class CreateD3Network(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.RTPATTERN = "rt @[_a-zA-Z0-9]+"
        self.DEFAULT_NODE_SIZE = 0

        self.NODE_COUNT_LIMIT = 1
        self.node_color_scheme = ["#FFFFD9", "#EDF8B1", "#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8",
                                  "#253494", "#081D58"]
        self.node_color_scheme = ["#A6BDDB", "#74A9CF", "#3690C0", "#0570B0", "#045A8D", "#023858"]

    def get_rt_users(self, text):

        rt_users = []
        for nuser in re.findall(self.RTPATTERN, text, flags=re.IGNORECASE):
            nuser = re.sub("rt @|RT @", "", nuser)
            rt_users.append(nuser.lower())
        return rt_users

    def get_category(self, tweet, usercategories):
        """
        Identifies the category to which the tweet belongs. Each category is defined by a group of words/hashtags
        :param tweet: 
        :param usercategories: 
        :return: 
        """
        category_votes = {}
        tweet = tweet.lower()
        i = 0
        for cat in usercategories:
            for s in cat.tags:
                if s in tweet:
                    if i in category_votes:
                        category_votes[i] = category_votes[i] + 1
                    else:
                        category_votes[i] = 1
            i += 1
        keyset = set(category_votes.keys())
        maxvote = 0
        # by default the tweet will be in the first category
        maxcategoryindex = 0
        for key in keyset:
            if category_votes[key] > maxvote:
                maxvote = category_votes[key]
                maxcategoryindex = key
        return maxcategoryindex

    def convert_json_array_to_array(self, hashtagcoll):
        """
        Converts the input jsonobject containing category descriptions to an array for processing.
        :param hashtagcoll: hashtagcoll JSONObject containing the list of hashtags, color, and the topic information
        :return: An array of hashtags
        """
        hashtags = []
        if hashtagcoll != None:
            for key in hashtagcoll.keys():
                ht = HashTagDS()
                ht.groupname = key
                ht.color = hashtagcoll[key]["color"]
                ht.tags = hashtagcoll[key]["hts"]
                hashtags.append(ht)
        return hashtags

    def get_majority_topic_color(self, tnfs, hashtagarray):
        """
        Identifies the category of a node based on the content of his tweets(each tweet can be assigned a category based on it's text). A simple majority is sufficient to make this decision.
        :param tnfs: 
        :param hashtagarray: 
        :return: 
        """
        catcount = {}
        # if the node has no tolinks then look at the node that it retweeted to decide the color of the node
        for tweet in tnfs.data:
            id = self.get_category(tweet, hashtagarray)
            if id in catcount:
                catcount[id] = catcount[id] + 1
            else:
                catcount[id] = 1
        keys = set(catcount.keys())
        maxcatID = -1
        maxcount = 0
        for k in keys:
            if maxcatID == -1:
                maxcatID = k
                maxcount = catcount[k]
            else:
                if maxcount < catcount[k]:
                    maxcount = catcount[k]
                    maxcatID = k
        return maxcatID

    def node_size_comparator(self, o1, o2):
        size1 = o1.size
        size2 = o2.size
        if size1 > size2:
            return 1
        if size1 < size2:
            return -1
        else:
            return 0

    def node_id_comparator(self, o1, o2):
        id1 = o1.id
        id2 = o2.id
        if id1 > id2:
            return 1
        elif id1 < id2:
            return -1
        else:
            return 0

    def convert_tweets_to_diffusion_path(self, inFilename, numNodeClasses, hashtags, num_nodes):
        """
        Takes as input a JSON file and reads through the file sequentially to process and create a retweet network from the tweets.
        :param inFilename
        :param numNodeClasses
        :param hashtags  category info containing hashtags
        :param num_nodes number of seed nodes to be included in the network
        :return a JSONObject consisting of nodes and links of the network
        """
        userconnections = {}
        hashtagarray = self.convert_json_array_to_array(hashtags)
        br = None
        with open(inFilename) as fp:
            for line in fp:
                tweetobj = json.loads(line)
                t = Tweet()
                text = TextUtils().get_clean_text(tweetobj["text"]).lower()
                groupmatch = False
                for ht in hashtagarray:
                    tags = ht.tags
                    for tg in tags:
                        if tg in text:
                            groupmatch = True
                            break
                    if groupmatch:
                        break
                if not groupmatch:
                    continue
                fromusers = []
                if "retweeted_status" in tweetobj:
                    rtstatus = tweetobj["retweeted_status"]
                    if "user" in rtstatus:
                        rtuserobj = rtstatus["user"]
                        fromusers.append(rtuserobj["screen_name"])
                else:
                    # use the tweet text to retrieve the pattern "RT @username:"
                    fromusers = self.get_rt_users(text)
                if not fromusers:
                    continue
                t.text = TextUtils().remove_rt_elements(text)
                if "user" in tweetobj:
                    userobj = tweetobj["user"]
                    t.user = str(userobj["screen_name"]).lower()
                t.catColor = hashtagarray[t.catID].color
                cur_level = 0
                for i in range(len(fromusers) - 1, -1, -1):
                    touser = ""
                    if i == 0:
                        touser = t.user
                    else:
                        touser = fromusers[i - 1]
                    if fromusers[i] == touser:
                        continue
                    fromuser = NetworkNode()
                    if fromusers[i] in userconnections:
                        fromuser = userconnections[fromusers[i]]
                    else:
                        fromuser = NetworkNode()
                        fromuser.username = fromusers[i]
                        fromuser.tonodes = []
                        fromuser.class_codes = []
                        fromuser.size = self.DEFAULT_NODE_SIZE
                        fromuser.level = cur_level
                        fromuser.data = []
                        fromuser.data.append(t.text)
                    tonode = NetworkNode()
                    if touser not in userconnections:
                        tonode = NetworkNode()
                        tonode.username = touser
                        tonode.tonodes = []
                        tonode.class_codes = []
                        tonode.catID = t.catID
                        tonode.catColor = t.catColor
                        tonode.size = self.DEFAULT_NODE_SIZE
                        tonode.data = []
                        tonode.data.append(t.text)
                        tonode.level = cur_level + 1
                        userconnections[touser] = tonode
                    else:
                        tonode = userconnections[touser]
                        tonode.data.append(t.text)
                        if tonode.level < (cur_level + 1):
                            tonode.level = cur_level
                    inf = ToNodeInfo()
                    inf.tonodeid = tonode.id
                    inf.text = t.text
                    inf.tousername = touser
                    inf.catID = t.catID
                    inf.catColor = t.catColor
                    fromuser.tonodes.append(inf)
                    fromuser.size = fromuser.size + 1
                    userconnections[fromusers[i]] = fromuser
                    cur_level = cur_level + 1
        keys = set(userconnections.keys())
        returnnodes = []
        min = self.DEFAULT_NODE_SIZE + 1
        max = self.DEFAULT_NODE_SIZE + 1
        for k in keys:
            n = userconnections[k]
            maxcat = self.get_majority_topic_color(n, hashtagarray)
            n.catID = maxcat
            n.catColor = hashtagarray[maxcat].color
            userconnections[k] = n
            if n.size > max:
                max = n.size
            if n.size < min:
                min = n.size
            returnnodes.append(n)
        nodes = self.compute_groups_sqrt(returnnodes, max, min, numNodeClasses)
        nodes.sort(self.node_size_comparator, reverse=True)
        nodes_to_visit = 0
        if len(nodes) >= num_nodes:
            nodes_to_visit = num_nodes
        else:
            nodes_to_visit = nodes.size()
        prunednodes = {}
        nodeidlist = {}
        nodeid = 0
        for k in range(nodes_to_visit):
            nd = nodes[k]
            nd.level = 0
            rtnodes = get_next_hop_connections(userconnections, nd, {})
            names = set(rtnodes.keys())
            for n in names:
                if n not in prunednodes:
                    newnode = rtnodes[n]
                    if newnode.size > 0:
                        prunednodes[n] = newnode
                        nodeidlist[n] = nodeid
                        nodeid = nodeid + 1

        allnodes = set(prunednodes.keys())
        finalnodes = []
        for n in allnodes:
            nd = prunednodes[n]
            nd.id = nodeidlist[nd.username]
            connids = []
            counter = 0
            for tnf in nd.tonodes:
                if tnf.tousername in nodeidlist:
                    tnf.tonodeid = nodeidlist[tnf.tousername]
                    connids.append(tnf.tonodeid)
                    nd.tonodes[counter] = tnf
                    counter = counter + 1
            finalnodes.append(nd)
        # generate the clusterids
        # skipped

        finalnodes.sort(self.node_id_comparator)
        #print len(finalnodes)
        # for node in finalnodes:
        #     print str(node.id) + " " + node.username + " " + str(node.level) + " " + str(
        #         node.size) + " " + node.catColor + node.data[0]

        return self.get_d3_structure(finalnodes)

    def get_d3_structure(self, finalnodes):
        alltweets = {}
        nodes = []
        links = []
        for node in finalnodes:
            nodedata = []
            for tnf in node.tonodes:
                jsadj = {}
                jsadj["source"] = node.id
                jsadj["target"] = tnf.tonodeid
                jsadj["value"] = 1
                jsadj["data"] = tnf.class_code
                links.append(jsadj)
                jsdata = {}
                jsdata["tonodeid"] = tnf.tonodeid
                jsdata["nodefrom"] = node.username
                jsdata["nodeto"] = tnf.tousername
                jsdata["tweet"] = tnf.text
                nodedata.append(jsdata)
            nd = {}
            nd["name"] = node.username
            nd["group"] = node.group
            nd["id"] = node.id
            nd["size"] = node.size
            nd["catColor"] = node.catColor
            nd["catID"] = node.catID
            nd["data"] = nodedata
            nd["level"] = node.level
            nodes.append(nd)
        alltweets["nodes"] = nodes
        alltweets["links"] = links
        return alltweets

    def compute_groups_sqrt(self, nodes, max, min, noofclasses):
        finalnodes = []
        for i in range(len(nodes)):
            node = nodes[i]
            color_index = 0
            if node.size > 0:
                color_index = (math.ceil(((math.sqrt(node.size)) / math.sqrt(max)) * noofclasses)) - 1
            node.group = color_index
            finalnodes.append(node)
        return finalnodes


def get_next_hop_connections(userconnections, cur_node, newnodes):
    cur_node.level = cur_node.level + 1
    newnodes[cur_node.username] = cur_node
    i = 0
    while i < len(cur_node.tonodes):
        tnf = cur_node.tonodes[i]
        if tnf.tousername in newnodes:
            i += 1
            continue
        rtnodes = get_next_hop_connections(userconnections, userconnections[tnf.tousername], newnodes)
        newnodes = rtnodes
        i += 1
    return newnodes


@app.route('/getData', methods=['GET', 'POST'])
def getData():
    global groups
    global infile_name
    cdn = CreateD3Network()

    nodes = cdn.convert_tweets_to_diffusion_path(infile_name, 7, groups, 5)
    return jsonify(nodes)


if __name__ == '__main__':
    global jobj
    global infile_name

    parser = argparse.ArgumentParser(
        description='''Adds context to word cloud. Creates a Temporal Heatmap data for visualization according to the categories mentioned.''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=CreateD3Network().DEF_INFILENAME,
                        help='Name of the input file containing tweets')

    parser.add_argument('-g', nargs="?", default='{"Group 1": {"color": "#800000", "hts": ["zuccotti"]}, "Group 2": {"color": "#0FFF00", "hts": ["#nypd"]}}',
                        help="JSON of Groups. Each group has color and hts(keywords array):\nFor Example:\n{'Group 2': {'color': '#0FFF00', 'hts': ['#nypd']}, 'Group 1': {'color': '#800000', 'hts': ['zuccotti']}}")

    argsi = parser.parse_args()

    infile_name = argsi.i

    groups = json.loads(argsi.g)
    app.run(port=5002)
