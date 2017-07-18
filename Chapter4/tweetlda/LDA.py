#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Performs LDA - Latent Dirichlet allocation ( Topic Modeling) on the text of the tweets given in the tweet file.
__author__ = "Shobhit Sharma"
__copyright__ = "TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University"
"""
import argparse
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import sys
import json


def main(args):
    parser = argparse.ArgumentParser(
        description='''Creates a simple retweeted graph network from the json file provided. ''',
        epilog="""TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University\n@author Shobhit Sharma""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', nargs="?", default="../lda.json",
                        help='Name of the input file containing tweets')
    parser.add_argument('-c', nargs="?", default=10,
                        help='Number of Iterations on LDA')
    parser.add_argument('-n', nargs="?", default=25,
                        help='Number of Topics')
    parser.add_argument('-w', nargs="?", default=25,
                        help='Number of Words to analyze')
    parser.add_argument('-t', nargs="?", default=10,
                        help='Number of Worker Threads')
    argsi = parser.parse_args()

    iterations = argsi.c
    num_topics = argsi.n
    num_words_to_analyze = argsi.w
    num_workers = argsi.t
    infile_name = argsi.i

    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # compile sample documents into a list
    doc_set = []

    with open(infile_name) as fp:
        for temp in fp:
            jobj = json.loads(temp)
            doc_set.append(jobj["text"])

    print len(doc_set)

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]

        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        # add tokens to list
        texts.append(stemmed_tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]
    print "started"
    # generate LDA model
    # ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=ITERATIONS)

    ldamodel = models.LdaMulticore(corpus, id2word=dictionary, num_topics=num_topics, workers=num_workers,
                                   passes=iterations)
    for terms in ldamodel.print_topics(num_topics=num_topics, num_words=num_words_to_analyze):
        print terms[0], "-", ", ".join(terms[1].split('+'))


if __name__ == "__main__":
    main(sys.argv[1:])
