from abc import ABC, abstractmethod


class Heuristic(ABC):

    def __init__(self, ML, N, HL):
        self._ML = ML  # Movecount Limit
        self._N = N    # N in a row in order to win
        self.HL = HL


    @abstractmethod
    def eval(self, board):
        pass


    def __str__(self):
        return self.__class__.__name__


class NopHeuristic(Heuristic):

    def __init__(self, ML, N):
        super().__init__(ML, N, 0)


    def eval(self, board):
        return 0


class BadHeuristic(Heuristic):
    """This is the heuristic given in the assignment.

    DO NOT USE THIS HEURISTIC. As this heuristic violates the symmetry
    requirement of evaluation values in zero-sum games such as connect N.
    Because of this the search will give an incorrect answer.
    """

    def __init__(self, ML, N):
        super().__init__(ML, N, N - 1)


    def eval(self, board):
        maxrow = 0
        for x in range(board.w):
            for y in range(board.h):
                if board.grid[y][x] == board.onturn:
                    maxrow = max(maxrow, 1)

                    for xx in range(1, board.w - x):
                        if board.grid[y][x + xx] == board.onturn:
                            maxrow = max(maxrow, xx + 1)
                        else:
                            break

                    for yy in range(1, board.h - y):
                        if board.grid[y + yy][x] == board.onturn:
                            maxrow = max(maxrow, yy + 1)
                        else:
                            break

                    for d in range(1, min(board.w - x, board.h - y)):
                        if board.grid[y + d][x + d] == board.onturn:
                            maxrow = max(maxrow, d + 1)
                        else:
                            break

                    for a in range(1, min(board.w - x, y)):
                        if board.grid[y - a][x + a] == board.onturn:
                            maxrow = max(maxrow, a + 1)
                        else:
                            break

        return maxrow
