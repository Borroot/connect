from player import Player
from solver import Solver
from evaluation import Eval
from stats import Stats
from collections import namedtuple
from result import HResult


class Negamax(Player, Solver):

    def search(self, node, depth, color, info, stats):
        stats.nodecount += 1

        if (result := node.isover()) != None:
            if color: return  Eval(node.ML, 0,  result, node.movecount - info.rootcount)
            else:     return -Eval(node.ML, 0, -result, node.movecount - info.rootcount)

        if depth == 0: # TODO add HL
            return Eval(node.ML, 0, HResult.DRAW, 0)

        value = Eval.min()

        for move in node.moves():
            child = node.clone()
            child.play(move)
            value = max(value, -self.search(child, depth - 1, not color, info, stats))

        return value


    def eval(self, board):
        pass


    def move(self, board, depth=None, timeout=None):
        Info = namedtuple("Info", ["rootcount", "rootplayer"])
        info = Info(board.movecount, board.onturn)

        stats = Stats(board.clone(), depth)
        if depth is None: depth = board.ML

        bestmoves = []
        bestvalue = Eval.min()

        for move in board.moves():
            child = board.clone()
            child.play(move)

            value = self.search(child, depth, False, info, stats)

            if value > bestvalue:
                bestvalue = value
                bestmoves.clear()
                bestmoves.append(move)
            elif value == bestvalue:
                bestmoves.append(move)

        return bestmoves, bestvalue, stats


    def __str__(self):
        return "negamax"
