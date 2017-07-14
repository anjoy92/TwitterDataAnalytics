from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(""))))
from Chapter4.classificationbayes.NaiveBayesSentimentClassifier import NaiveBayesSentimentClassifier

def main(args):
    nbc = NaiveBayesSentimentClassifier()
    infilename = nbc.DEFAULT_FILE_NAME

    if len(args)>0:
        infilename = args[0]

    nbc.trainFromFile(infilename)

    print "Classify: I love new york"
    print str(nbc.classify("I love new york"))
    print "Classify: I like violence"
    print str(nbc.classify("I like violence"))

    print nbc.printWordOccurs(0, 50)
    print "**********************"
    print nbc.printWordOccurs(1, 50)

if __name__ == "__main__":
    main(sys.argv[1:])