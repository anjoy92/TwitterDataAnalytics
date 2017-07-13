import datetime

class DateInfo(object):
    def __init__(self):
        self.d = datetime.time()
        self.catcounts = {}

    def __cmp__(self, other):
        if other.d > self.d:
            return 1
        elif other.d < self.d:
            return -1
        else:
            return 0