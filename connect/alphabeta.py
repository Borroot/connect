from player import Player
from solver import Solver
from evaluation import Eval
from stats import Stats
from collections import namedtuple
from result import HResult, Result


class Alphabeta(Player, Solver):

    def search(self, node, depth, rootplayer, alpha, beta, info, stats):
        stats.nodecount += 1

        if info.timeout is not None and info.timeout.is_set():
            return Eval(node.ML, info.heuristic.HL, n = 0)

        if (result := node.isover()) != None:
            return Eval(node.ML, info.heuristic.HL, -result, node.movecount - info.rootcount, rootplayer)

        if depth == 0:
            stats.heuristic_used = True
            return Eval(node.ML, info.heuristic.HL, *info.heuristic.eval(node))

        value = Eval.min()

        for move in node.moves():
            child = node.clone()
            child.play(move)

            value = max(value, -self.search(child, depth - 1, not rootplayer, -beta, -alpha, info, stats))
            alpha = max(alpha, value)

            if alpha >= beta: break

        return value


    def eval(self, board):
        pass


    def _move(self, board, depth=None, heuristic=None, timeout=None):
        Info = namedtuple("Info", ["rootcount", "heuristic", "timeout"])
        info = Info(board.movecount, heuristic, timeout)

        stats = Stats(board.clone(), str(self), depth, heuristic)
        if depth is None: depth = board.ML - board.movecount

        # if we might use the heuristic it should available
        assert depth >= board.ML - board.movecount or heuristic is not None

        alpha = Eval.min()
        beta = Eval.max()

        bestmoves = []
        bestvalue = Eval.min()

        for move in board.moves():
            child = board.clone()
            child.play(move)

            value = -self.search(child, depth - 1, False, alpha, beta, info, stats)
            alpha = max(alpha, value)

            if info.timeout is not None and info.timeout.is_set():
                stats.timeout = True
                return stats

            if value > bestvalue:
                bestvalue = value
                bestmoves.clear()
                bestmoves.append(move)
            elif value == bestvalue:
                bestmoves.append(move)

        return bestmoves, bestvalue, stats


    def __str__(self):
        return "alphabeta"
