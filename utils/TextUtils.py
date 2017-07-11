import re

class TextUtils(object):
    def __init__(self):
        self.STOPWORDS=set()
        self.SEPARATOR = " "

    def LoadStopWords(self,filename):
        if not filename:
            return
        with open(filename) as fp:
            for line in fp:
                map(lambda x: self.STOPWORDS.add(x), line.split(','))

    def TokenizeText(self,text, ignoreHashtags, ignoreUsernames):
        tokens=text.split(self.SEPARATOR)
        words={}
        for token in tokens:
            token=re.sub("\"|'|\\.||;|,", "",token)
            if not token or len(token) <= 2 or token in self.STOPWORDS or token.startswith("&") or token.endswith("http"):
                continue
            else:
                if ignoreHashtags:
                    if token.startswith("#"):
                        continue
                if ignoreUsernames:
                    if token.startswith("@"):
                        continue
                if token in words:
                    words[token] = words[token] + 1
                else:
                    words[token] = 1
        return words

    def IsTweetRT(self,text):
        if re.search("^rt @[a-z_0-9]+",text):
            return True
        else:
            return False


    def ContainsURL(self,text):
        if re.search("https?://[a-zA-Z0-9\\./]+",text):
            return True
        else:
            return False

    def GetHashTags(self,text):
        return re.findall("#[a-zA-Z0-9]+", text)

    def GetCleanText(self,text):
        text=re.sub("'|\"|&quot;", "",text)
        text=re.sub("\\\\", "",text)
        text=re.sub("\r\n|\n|\r", "",text)
        return text.strip()

    def RemoveRTElements(self,tweet):
        text = re.sub("rt @[a-z_A-Z0-9]+", " ",tweet)
        text = re.sub("RT @[a-z_A-Z0-9]+", " ",text)
        text = re.sub(":", "",text)
        return text.strip()

    def RemoveTwitterElements(self,tweet):

        temptweet = re.sub("#[a-zA-Z_0-9]+", "",tweet)
        temptweet = re.sub("https?://[a-zA-Z0-9\\./]+", "",temptweet)
        temptweet = re.sub("@[a-zA-Z_0-9]+", "",temptweet)
        temptweet = re.sub("[:?\\.;<>()]", "",temptweet)
        return temptweet