class Tags(object):
    def __init__(self):
        self.key = 0
        self.value = 0

    def __cmp__(self, other):
        if self.value > other.value:
            return 1
        if self.value < other.value:
            return -1
        else:
            return 0

