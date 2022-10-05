from enum import Enum


class Flag(Enum):

    LOWERBOUND = 0
    UPPERBOUND = 1
    EXACT = 2


class Table:

    def __init__(self, size):
        # make sure the size is a prime
        while not all(size % i for i in range(2, size)): size += 1
        self.size = size
        self.table = [None] * size


    def put(self, key, value, flag):
        self.table[key % self.size] = (key, value, flag)


    def get(self, key):
        if (entry := self.table[key % self.size]) is not None:
            if key == entry[0]:
                return entry[1], entry[2]  # value, flag
        return None


    def count(self):
        return sum(1 for entry in self.table if entry is not None)
