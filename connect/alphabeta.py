from player import Player
from solver import Solver


class Alphabeta(Player, Solver):

    def eval(self, board):
        pass


    def _move(self, board, depth=None, heuristic=None, timeout=None):
        pass


    def __str__(self):
        return "alphabeta"
