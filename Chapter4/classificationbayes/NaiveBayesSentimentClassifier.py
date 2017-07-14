from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from Chapter5.support.Classification import Classification
from Chapter5.support.WordCountPair import WordCountPair
import math
from gensim import corpora, models

class NaiveBayesSentimentClassifier(object):
    def __init__(self):
        self.SENTIMENT_LABELS = ["happy", "sad"]
        self.HAPPY_SMILEYS = [":)", ";)", ":D", ":-)", ":o)", ":-D"]
        self.SAD_SMILEYS = [":(", ":-(", ":'(", ":'-(", "D:"]
        self.HAPPY_SMILEY_SET = set (self.HAPPY_SMILEYS)
        self.SAD_SMILEY_SET = set(self.SAD_SMILEYS)
        self.sentOccurs = {}
        self.sentCount = [0]*len(self.SENTIMENT_LABELS)
        self.DEFAULT_FILE_NAME = "../sentiment.json"

    def getTokens(self,text):
        raw = text.lower()

        # remove stop words from tokens
        tokenizer = RegexpTokenizer(r'\w+')

        tokens = tokenizer.tokenize(raw)


        tokens = [unicode(i, errors='ignore').decode('utf-8') for i in tokens]

        tokens = [i for i in tokens if not i.isdigit()]

        # create English stop words list
        en_stop = get_stop_words('en')

        tokens = [i for i in tokens if not i in en_stop]

        #Create p_stemmer of class PorterStemmer
        p_stemmer = PorterStemmer()

        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in tokens]

        return stemmed_tokens

    def trainInstance(self,tweetText):
        tweetLabel = self.extractLabel(tweetText)
        tokens = self.getTokens(tweetText)
        if tweetLabel != -1:
            self.updateClassifier(tokens, tweetLabel)

    def extractLabel(self,tweetText):
        for word in self.HAPPY_SMILEY_SET:
            if word in tweetText:
                return 0

        for word in self.SAD_SMILEY_SET:
            if word in tweetText:
                return 1

        return -1

    def updateClassifier(self,tokens, sentIndex):
        for token in tokens:
            if token in self.sentOccurs:
                self.sentOccurs[token][sentIndex] += 1
            else:
                newArray = [0, 0]
                newArray[sentIndex] += 1
                self.sentOccurs[token] = newArray
        self.sentCount[sentIndex] += 1

    def calcLabelProb(self,tokens, sentIndex):
        pClass = [0]*len(self.SENTIMENT_LABELS)
        cSum = self.sumVector(self.sentCount)
        totalWordCount = 0
        for i in range(len(self.sentCount)):
            pClass[i] = self.sentCount[i] * 1.0 / cSum
        for word in set(self.sentOccurs.keys()):
            wordCt = self.sentOccurs[word]
            totalWordCount = self.sumVector(wordCt)
            p = 1.0
            foundOne = False
            for token in tokens:
                if ( token in self.sentOccurs):
                    foundOne = True
                    probs = self.sentOccurs[token]
                    pWordGivenClass = probs[sentIndex] / (self.sumVector(probs))
                    pWord = self.sumVector(probs) / totalWordCount
                    p *= pWordGivenClass * pClass[sentIndex] / pWord
            if foundOne:
                return p
            else:
                return 0.0

    def sumVector(self,vector):
        sum = 0.0
        for d in vector:
            sum = sum + d
        return sum

    def classify(self,tweetText):
        labelProbs = [0]*len(self.SENTIMENT_LABELS)
        tokens = self.getTokens(tweetText)
        maxLabelIdx = 0
        for i in range(len(labelProbs)):
            labelProbs[i] = self.calcLabelProb(tokens, i)
            print i," -> ",labelProbs[i]
            if labelProbs[i] > labelProbs[maxLabelIdx]:
                maxLabelIdx = i
            else:
                maxLabelIdx = maxLabelIdx

        conf = labelProbs[maxLabelIdx]
        labelProbs[maxLabelIdx] = 0

        conf -= self.sumVector(labelProbs)

        return Classification().Classification(self.SENTIMENT_LABELS[maxLabelIdx], conf)

    def printWordOccurs(self,sentIndex,topN):
        sb = ""
        wpcset = []
        s = ""
        t = 0
        print "Top ",topN," from ",self.SENTIMENT_LABELS[sentIndex]
        sIter = set(self.sentOccurs.keys())
        for s in sIter:
            wpcset.append(WordCountPair().WordCountPair(s, math.sqrt(self.sentOccurs[s][sentIndex] * 1.0)))
        wpcset.sort()
        frac= 0.0
        i = 0

        while (i < topN or topN <= 0) and i < len(wpcset):
            if wpcset:
                s = wpcset[i].word
                frac = wpcset[i].count
                sb+=s
                sb+=":"
                sb+=str(frac)
                sb+="\n"
                i+=1

        return sb

    def trainInstances(self,tweetTexts):
        for text in tweetTexts:
            self.trainInstance(text)

    def trainFromFile(self,infilename):
        with open(infilename) as fp:
            for temp in fp:
                self.trainInstance(temp)

