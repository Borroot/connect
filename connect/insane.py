from player import Player
from evaluation import Eval
from stats import Stats
from collections import namedtuple
from result import Result
from table import Table, Flag
import time


class Insane(Player):

    def search(self, node, depth, rootplayer, alpha, beta, info, stats):
        stats.nodecount += 1
        alpha_original = alpha

        if info.timeout is not None and info.timeout.is_set():
            return Eval(const = Eval.UNDEFINED)

        if (entry := info.table.get(node.key)) is not None:
            value, flag = entry
            if   flag == Flag.LOWERBOUND: alpha = max(alpha, value)
            elif flag == Flag.UPPERBOUND: beta  = min(beta,  value)
            else: return value  # flag == Flag.EXACT

            if alpha >= beta and alpha != Eval(const = Eval.UNDEFINED) \
                             and beta  != Eval(const = Eval.UNDEFINED):
                return value

        if (result := node.isover()) != None:
            return Eval(node.ML, info.heuristic.HL, -result, node.movecount - info.rootcount, rootplayer)

        if depth == 0:
            stats.heuristic_used = True
            return Eval(node.ML, info.heuristic.HL, heuristic = info.heuristic.eval(node))

        moves = node.moves()
        moves.sort(key = lambda c: abs(node.w / 2 - c))

        value = Eval(const = Eval.MIN)

        for move in moves:
            child = node.clone()
            child.play(move)

            value = max(value, -self.search(child, depth - 1, not rootplayer, -beta, -alpha, info, stats))
            alpha = max(alpha, value)

            if alpha >= beta and alpha != Eval(const = Eval.UNDEFINED) \
                             and beta  != Eval(const = Eval.UNDEFINED):
                break

        if value != Eval(const = Eval.UNDEFINED):
            def getflag():
                if value <= alpha_original: return Flag.UPPERBOUND
                elif value >= beta: return Flag.LOWERBOUND
                else: return Flag.EXACT
            info.table.put(node.key, value, getflag())

        return value


    def mtdf(self, node, depth, rootplayer, alpha, beta, info, stats):
        min_value = alpha.n
        max_value = beta.n
        guess = 0

        while min_value < max_value:
            beta = max(guess, min_value + 1)

            alpha_eval = Eval(node.ML, info.heuristic.HL, n = beta - 1)
            beta_eval = Eval(node.ML, info.heuristic.HL, n = beta)

            value = self.search(node, depth, rootplayer, alpha_eval, beta_eval, info, stats)
            guess = value.n

            if guess < beta:
                max_value = guess
            else:
                min_value = guess

        return Eval(node.ML, info.heuristic.HL, n = guess)


    def iterdeep(self, node, maxdepth, rootplayer, alpha, beta, info, stats):
        value = Eval(const = Eval.UNDEFINED)
        for depth in range(maxdepth + 1):
            if info.timeout is not None and info.timeout.is_set():
                return value

            value = self.mtdf(node, depth, rootplayer, alpha, beta, info, stats)
            if value != Eval(const = Eval.UNDEFINED): # TODO continue until we got no heuristic value
                return value
        return value


    def _move(self, board, depth=None, heuristic=None, timeout=None):
        Info = namedtuple("Info", ["rootcount", "heuristic", "timeout", "table"])
        info = Info(board.movecount, heuristic, timeout, Table(int(1e7)))

        stats = Stats(board.clone(), str(self), time.time(), depth, heuristic, hastable=True)
        stats.table_size = info.table.size
        if depth is None: depth = board.ML - board.movecount

        # if we might use the heuristic it should available
        assert depth >= board.ML - board.movecount or heuristic is not None

        alpha = Eval(const = Eval.MIN)
        beta = Eval(const = Eval.MAX)

        bestmoves = []
        bestvalue = Eval(const = Eval.MIN)

        moves = board.moves()
        moves.sort(key = lambda c: abs(board.w / 2 - c))

        for move in moves:
            child = board.clone()
            child.play(move)

            value = -self.search(child, depth - 1, False, -beta, -alpha, info, stats)

            if info.timeout is not None and info.timeout.is_set():
                stats.table_count = info.table.count()
                stats.timeout = True
                stats.end_time = time.time()
                return stats

            if value > bestvalue:
                bestvalue = value
                bestmoves.clear()
                bestmoves.append(move)
            elif value == bestvalue:
                bestmoves.append(move)

        bestmoves.sort()

        stats.table_count = info.table.count()
        stats.end_time = time.time()
        return bestmoves, bestvalue, stats


    def __str__(self):
        return "insane"
