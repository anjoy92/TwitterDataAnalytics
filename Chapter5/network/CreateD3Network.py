import math

from Chapter5.support.HashTagDS import HashTagDS
from Chapter5.support.NetworkNode import NetworkNode
from Chapter5.support.ToNodeInfo import ToNodeInfo
from Chapter5.support.Tweet import Tweet
from utils.TextUtils import TextUtils
import re
from flask import json


class CreateD3Network(object):

    def __init__(self):
        self.DEF_INFILENAME = "ows.json"
        self.RTPATTERN = "rt @[_a-zA-Z0-9]+"
        self.DEFAULT_NODE_SIZE = 0

        self.NODE_COUNT_LIMIT = 1
        self.node_color_scheme = ["#FFFFD9","#EDF8B1","#C7E9B4","#7FCDBB","#41B6C4","#1D91C0","#225EA8","#253494","#081D58"]
        self.node_color_scheme = ["#A6BDDB","#74A9CF","#3690C0","#0570B0","#045A8D","#023858"]

    def GetRTUsers(self, text):

        rtusers = []
        for nuser in re.findall(self.RTPATTERN,text,flags=re.IGNORECASE):
            nuser = re.sub("rt @|RT @", "",nuser)
            rtusers.append(nuser.lower())
        return rtusers

    #
    #      * Identifies the category to which the tweet belongs. Each category is defined by a group of words/hashtags
    #      * @param tweet
    #      * @param usercategories
    #      * @return
    #
    def GetCategory(self, tweet, usercategories):
        """ generated source for method GetCategory """
        categoryvotes = {}
        tweet = tweet.lower()
        i = 0
        for cat in usercategories:
            for s in cat.tags:
                if s in tweet:
                    if i in categoryvotes:
                        categoryvotes[i]= categoryvotes[i] + 1
                    else:
                        categoryvotes[i]= 1
            i += 1
        keyset = set(categoryvotes.keys())
        maxvote = 0
        # by default the tweet will be in the first category
        maxcategoryindex = 0
        for key in keyset:
            if categoryvotes[key] > maxvote:
                maxvote = categoryvotes[key]
                maxcategoryindex = key
        return maxcategoryindex

    #
    #      * Converts the input jsonobject containing category descriptions to an array for processing.
    #      * @param hashtagcoll JSONObject containing the list of hashtags, color, and the topic information
    #      * @return An array of hashtags
    #
    def ConvertJSONArrayToArray(self, hashtagcoll):
        hashtags = []
        if hashtagcoll != None:
            for key in hashtagcoll.keys():
                ht=HashTagDS()
                ht.groupname = key
                ht.color = hashtagcoll[key]["color"]
                ht.tags = hashtagcoll[key]["hts"]
                hashtags.append(ht)
        return hashtags

    #
    #      * Identifies the category of a node based on the content of his tweets(each tweet can be assigned a category based on it's text). A simple majority is sufficient to make this decision.
    #      * @param tnfs
    #      * @param hashtagarray
    #      * @return
    #
    def GetMajorityTopicColor(self, tnfs, hashtagarray):
        """ generated source for method GetMajorityTopicColor """
        catcount = {}
        # if the node has no tolinks then look at the node that it retweeted to decide the color of the node
        for tweet in tnfs.data:
            id = self.GetCategory(tweet, hashtagarray)
            if id in catcount:
                catcount[id]=catcount[id] + 1
            else:
                catcount[id]= 1
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



    def NodeSizeComparator(self,o1, o2):
        size1 = o1.size
        size2 = o2.size
        if size1 > size2:
            return 1
        if size1 < size2:
            return -1
        else:
            return 0

    def NodeIDComparator(self,o1,o2):
        id1 = o1.id
        id2 = o2.id
        if id1 > id2:
            return 1
        elif id1 < id2:
            return -1
        else:
            return 0

    #
    #      * Takes as input a JSON file and reads through the file sequentially to process and create a retweet network from the tweets.
    #      * @param inFilename
    #      * @param numNodeClasses
    #      * @param hashtags  category info containing hashtags
    #      * @param num_nodes number of seed nodes to be included in the network
    #      * @return a JSONObject consisting of nodes and links of the network
    #
    def ConvertTweetsToDiffusionPath(self, inFilename, numNodeClasses, hashtags, num_nodes):
        """ generated source for method ConvertTweetsToDiffusionPath """
        userconnections = {}
        hashtagarray = self.ConvertJSONArrayToArray(hashtags)
        br = None
        with open(inFilename) as fp:
            for line in fp:
                tweetobj = json.loads(line)
                t=Tweet()
                text = TextUtils().GetCleanText(tweetobj["text"]).lower()
                groupmatch = False
                for ht in hashtagarray:
                    tags=ht.tags
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
                    fromusers = self.GetRTUsers(text)
                if not fromusers:
                    continue
                t.text = TextUtils().RemoveRTElements(text)
                if "user" in tweetobj:
                    userobj = tweetobj["user"]
                    t.user = str(userobj["screen_name"]).lower()
                t.catColor = hashtagarray[t.catID].color
                cur_level = 0
                for i in range(len(fromusers)-1,-1,-1):
                    touser=""
                    if i==0:
                        touser=t.user
                    else:
                        touser=fromusers[i-1]
                    if fromusers[i] == touser:
                        continue
                    fromuser=NetworkNode()
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
                        userconnections[touser]=tonode
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
                    userconnections[fromusers[i]]= fromuser
                    cur_level =  cur_level + 1
        keys = set(userconnections.keys())
        returnnodes = []
        min = self.DEFAULT_NODE_SIZE + 1
        max = self.DEFAULT_NODE_SIZE + 1
        for k in keys:
            n = userconnections[k]
            maxcat = self.GetMajorityTopicColor(n, hashtagarray)
            n.catID = maxcat
            n.catColor = hashtagarray[maxcat].color
            userconnections[k]= n
            if n.size>max:
                max = n.size
            if n.size<min:
                min = n.size
            returnnodes.append(n)
        nodes = self.ComputeGroupsSqrt(returnnodes, max, min, numNodeClasses)
        nodes.sort(self.NodeSizeComparator, reverse=True)
        nodes_to_visit = 0
        if len(nodes)>=num_nodes:
            nodes_to_visit = num_nodes
        else:
            nodes_to_visit = nodes.size()
        prunednodes = {}
        nodeidlist = {}
        nodeid = 0
        for k in range(nodes_to_visit):
            nd = nodes[k]
            nd.level = 0
            rtnodes = GetNextHopConnections(userconnections,nd,{})
            names = set(rtnodes.keys())
            for n in names:
                if n not in prunednodes:
                    newnode = rtnodes[n]
                    if newnode.size>0:
                        prunednodes[n]=newnode
                        nodeidlist[n]=nodeid
                        nodeid=nodeid+1

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
                    nd.tonodes[counter]=tnf
                    counter = counter + 1
            finalnodes.append(nd)
        # generate the clusterids
        # skipped

        finalnodes.sort(self.NodeIDComparator)
        print len(finalnodes)
        for node in finalnodes:
            print str(node.id)+" "+node.username+" "+str(node.level)+" "+str(node.size)+" "+node.catColor+node.data[0]

        return self.GetD3Structure(finalnodes)

    def GetD3Structure(self, finalnodes):
        """ generated source for method GetD3Structure """
        alltweets = {}
        nodes = []
        links = []
        for node in finalnodes:
            nodedata = []
            for tnf in node.tonodes:
                jsadj = {}
                jsadj["source"] = node.id
                jsadj["target"]= tnf.tonodeid
                jsadj["value"]= 1
                jsadj["data"]= tnf.class_code
                links.append(jsadj)
                jsdata={}
                jsdata["tonodeid"]= tnf.tonodeid
                jsdata["nodefrom"]= node.username
                jsdata["nodeto"]= tnf.tousername
                jsdata["tweet"]=tnf.text
                nodedata.append(jsdata)
            nd = {}
            nd["name"]= node.username
            nd["group"]= node.group
            nd["id"]= node.id
            nd["size"]= node.size
            nd["catColor"]= node.catColor
            nd["catID"]= node.catID
            nd["data"]= nodedata
            nd["level"]=node.level
            nodes.append(nd)
        alltweets["nodes"]= nodes
        alltweets["links"]= links
        return alltweets



    def ComputeGroupsSqrt(self, nodes, max, min, noofclasses):
        """ generated source for method ComputeGroupsSqrt """
        finalnodes = []
        for i in range(len(nodes)):
            node = nodes[i]
            color_index = 0
            if node.size>0:
                color_index = (math.ceil(((math.sqrt(node.size)) / math.sqrt(max)) * noofclasses)) - 1
            node.group = color_index
            finalnodes.append(node)
        return finalnodes
def GetNextHopConnections(userconnections, cur_node, newnodes):
    cur_node.level = cur_node.level + 1
    newnodes[cur_node.username]= cur_node
    i = 0
    while i < len(cur_node.tonodes):
        tnf = cur_node.tonodes[i]
        if tnf.tousername in newnodes:
            i+=1
            continue
        rtnodes = GetNextHopConnections(userconnections, userconnections[tnf.tousername], newnodes)
        newnodes = rtnodes
        i += 1
    return newnodes
def main( args):
    """ generated source for method main """
    cdn = CreateD3Network()
    obj={}
    jobj={}
    obj["color"] = "#800000"
    ja=["zuccotti"]
    obj["hts"] = ja
    jobj["Group 1"]=obj
    obj2={}
    obj2["color"] ="#0FFF00"
    ja2 = ["#nypd"]
    obj2["hts"]= ja2
    jobj["Group 2"]=obj2

    filename = "../ows.json"

    print jobj
    nodes = cdn.ConvertTweetsToDiffusionPath(filename, 7, jobj, 5)


if __name__ == '__main__':
    import sys
    main(sys.argv)
