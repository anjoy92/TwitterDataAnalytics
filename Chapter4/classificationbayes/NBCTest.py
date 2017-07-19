#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Train a Naive Bayes Sentiment Classifier from the text of tweets file mentioned. 
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter4.classificationbayes.NaiveBayesSentimentClassifier import NaiveBayesSentimentClassifier

def main(args):
    nbc = NaiveBayesSentimentClassifier()

    parser = argparse.ArgumentParser(
        description='''Train a Naive Bayes Sentiment Classifier from the text of tweets file mentioned. ''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default=nbc.DEFAULT_FILE_NAME,
                        help='Name of the input file containing tweets')

    argsi = parser.parse_args()

    # Get the input file name from the command line argument
    infile_name = argsi.i

    # Train the model
    nbc.train_from_file(infile_name)

    # Test the classification model
    print "Classify: I love new york"
    print str(nbc.classify("I love new york"))
    print "Classify: I like violence"
    print str(nbc.classify("I like violence"))

    print "*******************************************\n"
    # Print top words in Sad Sentiment
    print nbc.print_word_occurs(0, 50)

    print "*******************************************\n"
    # Print top words in Happy Sentiment
    print nbc.print_word_occurs(1, 50)

if __name__ == "__main__":
    main(sys.argv[1:])