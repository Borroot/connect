from player import Player
import random


class Random(Player):

    def _move(self, board, depth=None, heuristic=None, timeout=None):
        return random.choice(board.moves())


    def __str__(self):
        return "random"
