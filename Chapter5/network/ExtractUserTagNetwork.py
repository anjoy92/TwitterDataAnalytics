from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import re
from collections import Counter

class ExtractUserTagNetwork(object):
    """
    
    """
    def __init__(self):
        self.DEF_INFILENAME= "../ows.json"

    def ExtractHashTags(self,text):
        return dict(Counter(map(lambda x:x.lower(),re.findall("#[a-zA-Z0-9]+",text))))

    def ExtractUserHashtagNetwork(self,inFilename):
        usertagmap={}
        with open(inFilename) as fp:
            for line in fp:
                tweetobj = json.loads(line)
                text=""
                username=""
                tags={}
                if "entities" in tweetobj:
                    entities = tweetobj["tweetobj"]
                    hashtags = entities["hashtags"]
                    for i in range(len(hashtags)):
                        tag=hashtags[i]
                        tg = tag["text"].lower()
                        if tg not in tags:
                            tags[tg]=1
                        else:
                            tag[tg]=tag[tg]+1
                else:
                    if "text" in tweetobj:
                        text = tweetobj["text"]
                        tags = self.ExtractHashTags(text)
                if "user" in tweetobj:
                    userobj = tweetobj["user"]
                    username = "@" + str(userobj["screen_name"]).lower()
                    if username in usertagmap:
                        usertags = usertagmap[username]
                        keys = set(tags.keys())
                        for k in keys:
                            if k in usertags:
                                usertags[k]= usertags[k] + tags[k]
                            else:
                                usertags[k]= tags[k]
                        usertagmap[username]=usertags
                    else:
                        usertagmap[username] = tags
        return usertagmap

def main(args):
    eutn = ExtractUserTagNetwork()
    infilename = eutn.DEF_INFILENAME
    if args:
        infilename=args[0]
    usertagmap = eutn.ExtractUserHashtagNetwork(infilename)
    keys = set(usertagmap.keys())
    print len(keys)
    for key in keys:
        print key
        tags = usertagmap[key]
        tagkeys = set(tags.keys())
        for tag in tagkeys:
            print str(tag)+","+str(tags[tag])


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])