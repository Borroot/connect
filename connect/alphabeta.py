from player import Player
from evaluation import Eval
from stats import Stats
from collections import namedtuple
from result import Result
import time


class Alphabeta(Player):

    def search(self, node, depth, rootplayer, alpha, beta, info, stats):
        stats.nodecount += 1

        if info.timeout is not None and info.timeout.is_set():
            return Eval(const = Eval.UNDEFINED)

        if (result := node.isover()) != None:
            return Eval(node.ML, info.heuristic.HL, -result, node.movecount - info.rootcount, rootplayer)

        if depth == 0:
            stats.heuristic_used = True
            return Eval(node.ML, info.heuristic.HL, heuristic = info.heuristic.eval(node))

        value = Eval(const = Eval.MIN)

        for move in node.moves():
            child = node.clone()
            child.play(move)

            value = max(value, -self.search(child, depth - 1, not rootplayer, -beta, -alpha, info, stats))
            alpha = max(alpha, value)

            if alpha >= beta and alpha != Eval(const = Eval.UNDEFINED) \
                             and beta  != Eval(const = Eval.UNDEFINED):
                break

        return value


    def _move(self, board, depth=None, heuristic=None, timeout=None):
        Info = namedtuple("Info", ["rootcount", "heuristic", "timeout"])
        info = Info(board.movecount, heuristic, timeout)

        stats = Stats(board.clone(), str(self), time.time(), depth, heuristic)
        if depth is None: depth = board.ML - board.movecount

        # if we might use the heuristic it should available
        assert depth >= board.ML - board.movecount or heuristic is not None

        alpha = Eval(const = Eval.MIN)
        beta = Eval(const = Eval.MAX)

        bestmoves = []
        bestvalue = Eval(const = Eval.MIN)

        for move in board.moves():
            child = board.clone()
            child.play(move)

            value = -self.search(child, depth - 1, False, -beta, -alpha, info, stats)

            if info.timeout is not None and info.timeout.is_set():
                stats.end_time = time.time()
                stats.timeout = True
                return stats

            if value > bestvalue:
                bestvalue = value
                bestmoves.clear()
                bestmoves.append(move)
            elif value == bestvalue:
                bestmoves.append(move)

        stats.end_time = time.time()
        return bestmoves, bestvalue, stats


    def __str__(self):
        return "alphabeta"
