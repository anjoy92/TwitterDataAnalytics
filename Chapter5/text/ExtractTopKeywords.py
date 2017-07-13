from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
import json
import re
from utils.TextUtils import TextUtils
from utils.Tags import Tags

class ExtractTopKeywords(object):
    def __init__(self):
        self.DEF_INFILENAME = "../ows.json"
        self.DEF_K = 60

    def GetTopKeywords(self,inFilename,  K,  ignoreHashtags,  ignoreUsernames,  tu):
        words = {}
        with open(inFilename) as fp:
            for temp in fp:
                tweetobj = json.loads(temp)
                if "text" in tweetobj:
                    text = tweetobj["text"]
                    text=re.sub("\\s+"," ",text.lower())
                    tokens = tu.TokenizeText(text, ignoreHashtags, ignoreUsernames)
                    keys =tokens.keys()
                    for key in keys:
                        if key in words:
                            words[key] = words[key] + tokens[key]
                        else:
                            words[key]= tokens[key]

        keys = set(words.keys())
        tags = []
        for key in keys:
            tag = Tags()
            tag.key = key
            tag.value = words[key]
            tags.append(tag)
        tags.sort(reverse=True)
        cloudwords = []
        numwords = K
        if len(tags) < numwords:
            numwords = len(tags)
        for i in range(numwords):
            wordfreq = {}
            tag = tags[i]
            wordfreq["text"] = tag.key
            wordfreq["size"] = tag.value
            cloudwords.append(wordfreq)
        return cloudwords



def main(args):
    etk = ExtractTopKeywords()
    tu = TextUtils()
    tu.LoadStopWords("../stopwords.txt")
    infilename = etk.DEF_INFILENAME
    K = etk.DEF_K

    if len(args)>0:
        infilename = args[0]
    if len(args)>1:
        K = int(args[1])

    print etk.GetTopKeywords(infilename, K, False,True,tu)


if __name__ == "__main__":
    main(sys.argv[1:])



