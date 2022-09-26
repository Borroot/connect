from result import Result, HResult


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

    MIN = float("-inf")
    MAX = float("+inf")

    def __init__(self, ML, HL, result, distance_or_heuristic):
        """Create an evaluation from the given result.

        :param ML: Movecount Limit which depends on the board used
        :param HL: Heuristic Limit which depends on the heurstic used
        :param result: either an HResult or a normal Result
        :param distance_or_heurstic: either the distance to the normal Result
        or a heuristic value between 0 and HL
        :returns: evaluation of the board
        """
        assert distance_or_heuristic >= 0
        assert (isinstance(result,  Result) and distance_or_heuristic <= ML) or \
               (isinstance(result, HResult) and distance_or_heuristic <= HL)

        self._ML = ML
        self._HL = HL

        if isinstance(result, Result):
            # normal result
            d = distance_or_heuristic
            if   result == Result.Win:
                self._n =  2 * ML + HL + 2 - d
            elif result == Result.Loss:
                self._n = -2 * ML - HL - 2 + d
            else:
                self._n = d
        else:
            # heuristic result
            h = distance_or_heuristic
            if   result == HResult.Win:
                self._n =  ML + 1 + h
            elif result == HResult.Loss:
                self._n = -ML - 1 - h
            else:
                self._n = 0


    def __str__(self):
        # TODO add pretty evaluation printing
        return str(self._n)


    def raw(self):
        self._n


    def __neg__(self):
        self._n = -self._n


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
