class Classification(object):
    def __init__(self):
        self.label=""
        self.confidence=""

    def Classification(self,label,confidence):
        self.label = label
        self.confidence = confidence
        return self

    def __str__(self):
        return "(" +str(self.label) + ", " + str(self.confidence ) +")\n"