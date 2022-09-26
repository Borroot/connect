from abc import ABC, abstractmethod


class Solver(ABC):

    @abstractmethod
    def eval(self, board, depth=None, timeout=None):
        pass
