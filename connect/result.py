from enum import Enum


class Result(Enum):

    LOSS = -1
    DRAW =  0
    WIN  =  1


    def __neg__(self):
        return Result(-self.value)


class HResult(Enum):
    """Heuristic Result"""

    LOSS = -1
    DRAW =  0  # neutral
    WIN  =  1
