from abc import ABC, abstractmethod


class Player(ABC):

    @abstractmethod
    def move(self, board, depth=None, timeout=None):
        pass
