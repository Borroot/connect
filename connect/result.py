from enum import Enum


class Result(Enum):

    LOSS = -1
    DRAW =  0
    WIN  =  1


    def __neg__(self):
        return Result(-self.value)
