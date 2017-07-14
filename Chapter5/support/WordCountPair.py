class WordCountPair():
    def __init__(self):
        self.word=""
        self.count=0.0

    def __cmp__(self, other):
        if other.count - self.count < 0:
            return -1
        else:
            return 1

    def WordCountPair(self,word,count):
        self.word = word
        self.count = count
        return self
