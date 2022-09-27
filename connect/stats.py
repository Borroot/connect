class Stats:

    def __init__(self, board, maxdepth=None, heuristic=None):
        """An object to keep statistics of a search."""
        self.board = board
        self.nodecount = 0
        self.maxdepth = maxdepth
        self.heuristic = heuristic
        self.heuristic_used = False
        self.timeout = False


    def __str__(self):
        builder = "\n".join([
            "timeout: {}".format(self.timeout),
            "nodecount: {}".format(self.nodecount),
            "maximum depth: {}".format(self.maxdepth),
            "heuristic: {}".format(self.heuristic),
            "heuristic used: {}".format(self.heuristic_used),
            "",
        ])
        return builder


    def __repl__(self):
        return self.__str__()
