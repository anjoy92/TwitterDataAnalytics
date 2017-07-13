from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import sys
import json


def main(args):
    ITERATIONS = 10
    NUM_TOPICS = 25
    NOM_WORDS_TO_ANALYZE = 25
    WORKERS = 10
    infilename = "../testows.json"

    if len(args)>0:
        infilename = args[0]

    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # compile sample documents into a list
    doc_set = []

    with open(infilename) as fp:
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
    #ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=ITERATIONS)
    ldamodel = models.LdaMulticore(corpus, id2word=dictionary, num_topics=NUM_TOPICS, workers=WORKERS, passes=ITERATIONS)
    for terms in ldamodel.print_topics(num_topics=NUM_TOPICS, num_words=NOM_WORDS_TO_ANALYZE):
        print terms[0],"-",", ".join(terms[1].split('+'))

if __name__ == "__main__":
    main(sys.argv[1:])
