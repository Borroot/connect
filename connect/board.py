from result import Result


class Board:

    X = 0  # player X
    O = 1  # player O
    E = 2  # empty


    def __init__(self, width, height, N):
        """ Initialize a board with the given width and height. The game is won
        if one of the players has N consecutive stones. """
        self.w = width
        self.h = height
        self.N = N
        self.prev = None  # previous move column
        self.onturn = 0  # 0 represents player 1 and 1 represents player 2
        self.movecount = 0
        self.ML = width * height  # movecount limit
        self.grid = [[Board.E] * width for _ in range(height)]
        self.key = 0


    def __str__(self):
        builder = ""

        for y in range(self.h):
            for x in range(self.w):
                if   self.grid[y][x] == Board.X:
                    builder += "X"
                elif self.grid[y][x] == Board.O:
                    builder += "O"
                else:
                    builder += "."
                if x < self.w - 1: builder += " "
            builder += "\n"

        for x in range(self.w):
            builder += str(x % 10)
            if x < self.w - 1: builder += " "
        builder += "\n"

        return builder


    def __repl__(self):
        return self.__str__()


    def clone(self):
        """ Clone the board into a new object. """
        copy = Board(self.w, self.h, self.N)
        copy.prev = self.prev
        copy.onturn = self.onturn
        copy.movecount = self.movecount
        copy.ML = self.ML
        copy.grid = [row[:] for row in self.grid]
        copy.key = self.key
        return copy


    def from_seq(width, height, n, seq):
        """ Create a board from a sequence of moves. """
        board = Board(width, height, n)
        for m in seq:
            board.play(m)
        return board


    def canplay(self, x):
        """ Return whether you can play in the given column. """
        assert 0 <= x < self.w, "column {} is out of range".format(x)
        return self.grid[0][x] == Board.E


    def play(self, x):
        """ Play a stone in the given column, ranging from [0, n) (so excl n). """
        assert 0 <= x < self.w, "column {} is out of range".format(x)
        assert self.canplay(x), "cannot play in column {}".format(x)

        for y in reversed(range(self.h)):
            if self.grid[y][x] == Board.E:
                self.grid[y][x] = self.onturn
                self.prev = x
                self.key += pow(3, x + self.w * y) * (self.onturn + 1)
                break

        self.movecount += 1
        self.onturn ^= 1  # swap onturn


    def moves(self):
        """ The moves that can be made from the current position. """
        return [x for x in range(self.w) if self.canplay(x)]


    def isover(self):
        """ Give the result of the game is it is over due to the last move! """
        if self.prev is None:
            return None

        onturn = self.onturn ^ 1

        px = self.prev
        py = None
        for y in range(self.h):
            if self.grid[y][px] != Board.E:
                py = y
                break

        # check horizontal
        minx = max(0,          px - self.N + 1)
        maxx = min(self.w - 1, px + self.N - 1)

        count = 0
        for x in range(minx, maxx + 1):
            if self.grid[py][x] == onturn:
                count += 1
                if count == self.N:
                    return Result.WIN
            else:
                count = 0

        # check vertical
        miny = max(0,          py - self.N + 1)
        maxy = min(self.h - 1, py + self.N - 1)

        count = 0
        for y in range(miny, maxy + 1):
            if self.grid[y][px] == onturn:
                count += 1
                if count == self.N:
                    return Result.WIN
            else:
                count = 0

        # check top left to bottom right
        dist_top = min(px - minx, py - miny)
        top = (px - dist_top, py - dist_top) # (x, y)
        dist_bot = min(maxx - px, maxy - py)

        count = 0
        for i in range(dist_top + 1 + dist_bot):
            if self.grid[top[1] + i][top[0] + i] == onturn:
                count += 1
                if count == self.N:
                    return Result.WIN
            else:
                count = 0

        # check top right to bottom left
        dist_top = min(maxx - px, py - miny)
        top = (px + dist_top, py - dist_top) # (x, y)
        dist_bot = min(px - minx, maxy - py)

        count = 0
        for i in range(dist_top + 1 + dist_bot):
            if self.grid[top[1] + i][top[0] - i] == onturn:
                count += 1
                if count == self.N:
                    return Result.WIN
            else:
                count = 0

        # check draw
        if not any(self.canplay(x) for x in range(self.w)):
            return Result.DRAW

        # the game is not over yet
        return None
