from enum import Enum


class Result(Enum):

    LOSS = -1
    DRAW =  0
    WIN  =  1


class HResult(Enum):
    """Heuristic Result"""

    LOSS = -1
    DRAW =  0  # neutral
    WIN  =  1
