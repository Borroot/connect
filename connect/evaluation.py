from result import Result
import math


class Eval:

    MIN = 0
    MAX = 1
    UNDEFINED = 2

    # The internal representation of the evaluation is as shown in the diagram below.
    # L = Loss, D = Draw, W = Win, HL = Heuristic Loss, HW = Heuristic Win
    # ML = Movecount Limit = board width * board height, HL = Heuristic Limit

    #  <- MIN                                           0                                             MAX ->
    #  <--------------------------------------------------------------------------------------------------->
    #     |   LOSS     | |                | |         DRAW           | |                 | |     WIN    |
    #     |            / \                / \           |            / \                 / \            |
    #   L in 0   L in ML HL at HL   HL at 0 D in ML   D in 0   D in ML  HW at 0   HW at HL W in ML   W in 0
    #     |        |         |          |      |        |        |         |         |        |         |
    # -2ML-HL-2 -ML-HL-2 -ML-HL-1     -ML-1   -ML       0        ML      ML+1     ML+HL+1  ML+HL+2   2ML+HL+2

    def __init__(self, ML=None, HL=None, result=None, distance=None, rootplayer=True, heuristic=None, n=None, const=None):
        """Create an evaluation from the given result.

        :param ML: Movecount Limit which depends on the board used
        :param HL: Heuristic Limit which depends on the heurstic used
        :returns: evaluation of the board
        """
        self._ML = ML
        self._HL = HL

        if const is not None:
            if const is Eval.UNDEFINED:
                self.n = 0
            elif const is Eval.MAX:
                self.n = math.inf
            elif const is Eval.MIN:
                self.n = -math.inf
            return

        if result is not None:
            if   result == Result.WIN:
                self.n =  2 * ML + HL + 2 - distance
            elif result == Result.LOSS:
                self.n = -2 * ML - HL - 2 + distance
            else:
                if rootplayer: self.n =  distance
                else:          self.n = -distance
            return

        if heuristic is not None:
            if   heuristic > 0:
                self.n =  ML + 1 + heuristic
            elif heuristic < 0:
                self.n = -ML - 1 - heuristic
            else:
                self.n = 0
            return

        if n is not None:
            self.n = n
            return

        raise Exception


    def distance(self):
        """Give the distance to the solution, note that this is not meant for heuristic values."""
        ML = self._ML
        HL = self._HL

        if ML is None or HL is None:
            return self.n

        if   self.n >=  ML + HL + 2:
            return (2 * ML + HL + 2) - self.n
        elif self.n >=  ML + 1:
            return self.n - ( ML + 1)
        elif self.n <= -ML - HL - 2:
            return -((-2 * ML - HL - 2) - self.n)
        elif self.n <= -ML - 1:
            return self.n - (-ML - 1)
        elif self.n < 0:
            return -self.n
        else:
            return self.n


    def __str__(self):
        ML = self._ML
        HL = self._HL

        if ML is None or HL is None:
            if self.n == 0:
                return "undefined"
            elif math.isinf(self.n) and self.n > 0:
                return "+inf"
            elif math.isinf(self.n) and self.n < 0:
                return "-inf"
            raise Exception

        if   self.n >=  ML + HL + 2:
            return "win in {}".format((2 * ML + HL + 2) - self.n)
        elif self.n >=  ML + 1:
            return "heuristic value of {}".format(self.n - ( ML + 1))
        elif self.n <= -ML - HL - 2:
            return "loss in {}".format(-((-2 * ML - HL - 2) - self.n))
        elif self.n <= -ML - 1:
            return "heuristic value of {}".format(self.n - (-ML - 1))
        elif self.n == 0:
            return "undefined"
        else:
            return "draw in {}".format(self.n)

        raise Exception


    def __neg__(self):
        return Eval(self._ML, self._HL, n = -self.n)


    def __lt__(self, other):
        return self.n < other.n


    def __le__(self, other):
        return self.n <= other.n


    def __eq__(self, other):
        return self.n == other.n


    def __ne__(self, other):
        return self.n != other.n


    def __gt__(self, other):
        return self.n > other.n


    def __ge__(self, other):
        return self.n >= other.n
