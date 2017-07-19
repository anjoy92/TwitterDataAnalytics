#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Class to perform Naive Bayes Sentiment Classification.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from Chapter5.support.Classification import Classification
from Chapter5.support.WordCountPair import WordCountPair
import math


class NaiveBayesSentimentClassifier(object):
    def __init__(self):
        self.SENTIMENT_LABELS = ["happy", "sad"]
        self.HAPPY_SMILEYS = [":)", ";)", ":D", ":-)", ":o)", ":-D"]
        self.SAD_SMILEYS = [":(", ":-(", ":'(", ":'-(", "D:"]
        self.HAPPY_SMILEY_SET = set(self.HAPPY_SMILEYS)
        self.SAD_SMILEY_SET = set(self.SAD_SMILEYS)
        self.sentOccurs = {}
        self.sentCount = [0] * len(self.SENTIMENT_LABELS)
        self.DEFAULT_FILE_NAME = "../sentiment.json"

    def get_tokens(self, text):
        """
        Tokenize a string. Turns string into list of words based on whitespace, then removes stopwords, punctuation, and reduces the word to its stem. 
        :param text: The piece of text
        :return: Each individual word.
        """
        raw = text.lower()

        # remove stop words from tokens
        tokenizer = RegexpTokenizer(r'\w+')

        tokens = tokenizer.tokenize(raw)

        tokens = [unicode(i, errors='ignore').decode('utf-8') for i in tokens]

        tokens = [i for i in tokens if not i.isdigit()]

        # create English stop words list
        en_stop = get_stop_words('en')

        tokens = [i for i in tokens if not i in en_stop]

        # Create p_stemmer of class PorterStemmer
        p_stemmer = PorterStemmer()

        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in tokens]

        return stemmed_tokens

    def train_instance(self, tweetText):
        """
        Checks if tweet has a "label" (emoticon). If so, stores the words in the prior
        :param tweetText: The text of the document to check.
        """
        tweetLabel = self.extract_label(tweetText)
        tokens = self.get_tokens(tweetText)
        if tweetLabel != -1:
            self.update_classifier(tokens, tweetLabel)

    def extract_label(self, tweetText):
        """
        Check for the label
        :param tweetText: The text of the document to check.
        :return: 
        """
        for word in self.HAPPY_SMILEY_SET:
            if word in tweetText:
                return 0

        for word in self.SAD_SMILEY_SET:
            if word in tweetText:
                return 1

        return -1

    def update_classifier(self, tokens, sentIndex):
        """
        This updates the classifier's probabilites for each word with the new piece of text.
        :param tokens: The tokens in the tweet.
        :param sentIndex: The sentiment label.
        """
        for token in tokens:
            if token in self.sentOccurs:
                self.sentOccurs[token][sentIndex] += 1
            else:
                newArray = [0, 0]
                newArray[sentIndex] += 1
                self.sentOccurs[token] = newArray
        self.sentCount[sentIndex] += 1

    def calculate_label_prob(self, tokens, sent_index):
        """
        The probability of the tweet having a given label.
        :param tokens: The tokens in the tweet.
        :param sent_index: The probability we are testing.
        :return: The probability the tweet has the class label indicated by "sentIndex".
        """
        pClass = [0] * len(self.SENTIMENT_LABELS)

        # Get total times the sentiment was observed
        cSum = self.sum_vector(self.sentCount)

        # Number of words in each sentiment and then normalize. So we get P(s)
        for i in range(len(self.sentCount)):
            pClass[i] = self.sentCount[i] * 1.0 / cSum

        p = 1.0
        found_one = False
        for token in tokens:
            if token in self.sentOccurs:
                found_one = True
                probs = self.sentOccurs[token]
                # Calculate P(d/s) where d is word and s is sentiment
                p_word_given_class = probs[sent_index] / (self.sum_vector(probs))
                # Calculate (P(d/s)*P(s))/P(d) for each and keep on multiplying.
                # We are ignoring P(d).
                p = p *(p_word_given_class * pClass[sent_index])
        if found_one:
            return p
        else:
            return 0.0

    def sum_vector(self,vector):
        """
        Sum the elements in the array
        :param vector: 
        :return: sum of the array elements
        """
        sum = 0.0
        for d in vector:
            sum = sum + d
        return sum

    def classify(self, tweetText):
        """
        Classify a tweet as happy or sad. This ignores the emoticon for demonstration purposes.
        :param tweetText: The text of the tweet
        :return: A Classification object that returns the sentiment of the tweet.
        """
        label_probs = [0] * len(self.SENTIMENT_LABELS)
        tokens = self.get_tokens(tweetText)
        max_label_idx = 0
        for i in range(len(label_probs)):
            # Calculate the probability that the tweet has that sentiment
            label_probs[i] = self.calculate_label_prob(tokens, i)
            print i, " -> ", label_probs[i]

            # Keep track of the label probability
            if label_probs[i] > label_probs[max_label_idx]:
                max_label_idx = i
            else:
                max_label_idx = max_label_idx

        # Calculate the confidence
        conf = label_probs[max_label_idx]
        label_probs[max_label_idx] = 0
        conf -= self.sum_vector(label_probs)

        # Create a classification Object and return
        return Classification().classification(self.SENTIMENT_LABELS[max_label_idx], conf)

    def print_word_occurs(self, sentIndex, topN):
        """
        Print the top words in the particular sentiment.
        :param sentIndex: sentiment Index
        :param topN: top n words
        :return: string having the result
        """
        sb = ""
        wpcset = []
        print "Top ", topN, " from ", self.SENTIMENT_LABELS[sentIndex],":\n"

        # Get the sentiment keys
        s_iter = set(self.sentOccurs.keys())

        for s in s_iter:
            # Get the word and create a word count pair and append in wpset object
            wpcset.append(WordCountPair().WordCountPair(s, math.sqrt(self.sentOccurs[s][sentIndex] * 1.0)))

        # Sort by the count value. See the comparator in WordCountPair class for more info
        wpcset.sort()
        i = 0

        # Traverse the top words in the sentIndex sentiment
        while (i < topN or topN <= 0) and i < len(wpcset):
            if wpcset:
                s = wpcset[i].word
                frac = wpcset[i].count
                sb += s
                sb += ":"
                sb += str(frac)
                sb += "\n"
                i += 1

        return sb

    def train_instances(self, tweet_texts):
        """
        Call the train function to train each word in the tweet text
        :param tweet_texts: 
        :return: 
        """
        for text in tweet_texts:
            self.train_instance(text)

    def train_from_file(self, infile_name):
        """
        Train the words in the file.
        :param infile_name: Name of the input file.
        """
        with open(infile_name) as fp:
            for temp in fp:
                self.train_instance(temp)
