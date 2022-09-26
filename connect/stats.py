class Stats:

    def __init__(self, board, depth=None):
        """An object to keep statistics of a search."""
        self.board = board
        self.nodecount = 0
        self.depth = depth


    def __str__(self):
        builder = (
            "nodecount: {}\n".format(self.nodecount)
        )

        if self.depth is not None:
            builder += "depth: {}".format(self.depth)

        return builder


    def __repl__(self):
        return self.__str__()
