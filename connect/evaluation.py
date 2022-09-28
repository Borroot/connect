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

    def __init__(self, ML, HL, result=None, distance=None, rootplayer=True, heuristic=None, n=None, const=None):
        """Create an evaluation from the given result.

        :param ML: Movecount Limit which depends on the board used
        :param HL: Heuristic Limit which depends on the heurstic used
        :returns: evaluation of the board
        """
        self._ML = ML
        self._HL = HL

        if result is not None:
            if   result == Result.WIN:
                self._n =  2 * ML + HL + 2 - distance
            elif result == Result.LOSS:
                self._n = -2 * ML - HL - 2 + distance
            else:
                if rootplayer: self._n =  distance
                else:          self._n = -distance
            return

        if heuristic is not None:
            if   heuristic > 0:
                self._n =  ML + 1 + heuristic
            elif heuristic < 0:
                self._n = -ML - 1 - heuristic
            else:
                self._n = 0
            return

        if const is not None:
            if const is Eval.UNDEFINED:
                self._n = 0
            elif const is Eval.MAX:
                self._n = math.inf
            elif const is Eval.MIN:
                self._n = -math.inf
            return

        if n is not None:
            self._n = n
            return


    def __str__(self):
        ML = self._ML
        HL = self._HL
        if   self._n >=  ML + HL + 2:
            return "win in {}".format((2 * ML + HL + 2) - self._n)
        elif self._n >=  ML + 1:
            return "heuristic value of {}".format(self._n - ( ML + 1))
        elif self._n <= -ML - HL - 2:
            return "loss in {}".format(-((-2 * ML - HL - 2) - self._n))
        elif self._n <= -ML - 1:
            return "heuristic value of {}".format(self._n - (-ML - 1))
        elif self._n == 0:
            return "undefined".format(self._n)
        else:
            return "draw in {}".format(self._n)


    def __neg__(self):
        return Eval(self._ML, self._HL, n = -self._n)


    def __lt__(self, other):
        return self._n < other._n


    def __le__(self, other):
        return self._n <= other._n


    def __eq__(self, other):
        return self._n == other._n


    def __ne__(self, other):
        return self._n != other._n


    def __gt__(self, other):
        return self._n > other._n


    def __ge__(self, other):
        return self._n >= other._n
