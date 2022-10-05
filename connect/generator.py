from board import Board
from insane import Insane
from alphabeta import Alphabeta
from rand import Random
from stats import Stats
from heuristic import NopHeuristic
from evaluation import Eval
import random


def generate_board(movecount, width=7, height=6, N=4):
    complete = False
    while not complete:
        board = Board(width, height, N)
        moves = []

        for i in range(movecount):
            move = Random().move(board)
            # bestmoves, _, _ = Insane().move(board, 3, NopHeuristic(width * height, N))
            # move = random.choice(bestmoves)

            board.play(move)
            moves.append(move)

            if i == movecount - 1:
                complete = True

            if (result := board.isover()) is not None:
                break

        if complete:
            return board, moves


if __name__ == "__main__":
    width = 7
    height = 6
    N = 4

    movecount = 10
    amount = 30

    solver = Insane()
    maxdepth = 7
    mindepth = 3
    heuristic = NopHeuristic(width * height, N)
    timeout = 10

    folder = "tests/sets/"

    for mindepth, maxdepth in [(3, 7), (7, 14)]:
        for movecount in [30, 20, 10]:
            print("min {}, max {}, movecount {}".format(mindepth, maxdepth, movecount))

            filename = "{:02d}_{:02d}.txt".format(movecount, maxdepth)
            builder = ""

            for i in range(amount):
                board, moves = generate_board(movecount, width, height, N)
                result = solver.move(board, maxdepth, heuristic, timeout)

                while isinstance(result, Stats) or result[1] == Eval(const = Eval.UNDEFINED) \
                    or result[1].distance() < mindepth:
                    board, moves = generate_board(movecount, width, height, N)
                    result = solver.move(board, maxdepth, heuristic, timeout)

                print("{:02d}".format(i))

                value = result[1]
                builder += "{} {} {} {} {}\n".format(
                    width, height, N, value.n, " ".join(map(str, moves)))

            with open(folder + filename, "w") as f:
                f.write(builder)
