from result import Result, HResult
import math


class Eval:

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

    def __init__(self, ML, HL, result=None, distance_or_heuristic=None, rootplayer=True, n=None):
        """Create an evaluation from the given result.

        :param ML: Movecount Limit which depends on the board used
        :param HL: Heuristic Limit which depends on the heurstic used
        :param result: either an HResult or a normal Result
        :param distance_or_heurstic: either the distance to the normal Result
        or a heuristic value between 0 and HL
        :returns: evaluation of the board
        """
        self._ML = ML
        self._HL = HL

        if n is not None:
            self._n = n
        else:
            # Notice that we assume if n is None then result and
            # distance_or_heuristic are not None, the coder has to ensure this.
            assert (isinstance(result,  Result) and -ML <= distance_or_heuristic <= ML) or \
                   (isinstance(result, HResult) and   0 <= distance_or_heuristic <= HL)

            if isinstance(result, Result):
                # normal result with distance
                if   result == Result.WIN:
                    self._n =  2 * ML + HL + 2 - distance_or_heuristic
                elif result == Result.LOSS:
                    self._n = -2 * ML - HL - 2 + distance_or_heuristic
                else:
                    if rootplayer: self._n =  distance_or_heuristic
                    else:          self._n = -distance_or_heuristic
            else:
                # heuristic result
                if   result == HResult.WIN:
                    self._n =  ML + 1 + distance_or_heuristic
                elif result == HResult.LOSS:
                    self._n = -ML - 1 - distance_or_heuristic
                else:
                    self._n = 0


    @classmethod
    def min(cls):
        return cls(0, 0, n=-math.inf)


    @classmethod
    def max(cls):
        return cls(0, 0, n=math.inf)


    def __str__(self):
        ML = self._ML
        HL = self._HL
        if   self._n >=  ML + HL + 2:
            return "win in {}".format((2 * ML + HL + 2) - self._n)
        elif self._n >=  ML + 1:
            return "hvalue of {}".format(self._n - ( ML + 1))
        elif self._n <= -ML - HL - 2:
            return "loss in {}".format(-((-2 * ML - HL - 2) - self._n))
        elif self._n <= -ML - 1:
            return "hvalue of {}".format(self._n - (-ML - 1))
        elif self._n == 0:
            return "hvalue neutral".format(self._n)
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
        return self._n == other._n


    def __gt__(self, other):
        return self._n > other._n


    def __ge__(self, other):
        return self._n >= other._n
