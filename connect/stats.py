class Stats:

    def __init__(self, board, algorithm, start_time, maxdepth=None, heuristic=None, hastable=False):
        """An object to keep statistics of a search."""
        self.board = board
        self.algorithm = algorithm
        self.maxdepth = maxdepth
        self.heuristic = heuristic
        self.heuristic_used = False
        self.timeout = False
        self.nodecount = 0
        self.start_time = start_time
        self.end_time = None
        self.hastable = hastable
        self.table_count = 0
        self.table_size = 0


    def __str__(self):
        builder = "\n".join([
            "total time: {}ms".format(round(self.end_time - self.start_time, 3)),
            "timeout: {}".format(self.timeout),
            "nodecount: {}\n".format(self.nodecount),
            "algorithm: {}".format(self.algorithm),
            "max depth: {}".format(self.maxdepth),
            "heuristic: {}".format(self.heuristic),
            "heuristic used: {}".format(self.heuristic_used),
            "",
        ])
        if self.hastable:
            builder += "\n" + "\n".join([
                "table count: {}".format(self.table_count),
                "table size: {}".format(self.table_size),
                "",
            ])
        return builder


    def __repl__(self):
        return self.__str__()
