from board import Board
from rand import Random
from negamax import Negamax
from alphabeta import Alphabeta
from insane import Insane
from random import choice
from heuristic import NopHeuristic, BadHeuristic
from stats import Stats


board = Board(7, 6, 4)
history = []
heuristic = NopHeuristic
automove = False


def move(play):
    global board, history

    if play < 0 or play >= board.w:
        print("not in range of [0,{})".format(board.N))
        return

    if board.isover() is not None:
        print("game is already over")
        return

    if not board.canplay(play):
        print("illegal move")
        return

    board.play(play)
    history.append(play)

    show()

    if (result := board.isover()) is not None:
        if result == result.DRAW:
            print("It's a draw!")
        else:
            player = "X" if board.onturn == 1 else "O"
            print("Player {} won!".format(player))


def undo():
    global board, history

    if not history:
        return

    history.pop()
    board = Board.from_seq(board.w, board.h, board.N, history)

    show()


def solver(ai, args):
    if board.isover() is not None:
        print("game is already over")
        return

    timeout = float(5)
    depth = None

    if len(args) > 0:
        if args[0].isdigit():
            if int(args[0]) > 0: depth = int(args[0])
        else:
            print("please provide a valid depth")
            return

    if len(args) > 1:
        if args[1].isdigit() and int(args[1]) > 0:
            timeout = float(args[1])
        else:
            print("please provide a valid timeout")
            return

    result = ai.move(board, depth, heuristic(board.ML, board.N), timeout)

    if isinstance(result, Stats):
        print("\ntimeout reached at {}s".format(timeout))
        print(result)
    else:
        bestmoves, bestvalue, stats = result
        chosen = choice(bestmoves)

        print(
            "\n{} -> {}".format(bestmoves, chosen),
            "eval: {} ({})\n".format(bestvalue, bestvalue.n),
            stats,
            sep="\n"
        )

        if automove:
            move(chosen)


def random(args):
    global board, history

    if board.isover() is not None:
        print("game is already over")
        return

    number = 1

    if len(args) > 0:
        if not args[0].isdigit() or int(args[0]) < 1 or int(args[0]) > board.ML - board.movecount:
            print("please provide a valid number")
            return
        number = int(args[0])

    complete = False
    while not complete:
        board_clone = board.clone()
        history_clone = history[:]

        for i in range(number):
            move = Random().move(board_clone)

            board_clone.play(move)
            history_clone.append(move)

            if i == number - 1:
                complete = True

            if (result := board_clone.isover()) is not None:
                break

        if complete:
            board = board_clone
            history = history_clone
            show()

    if (result := board_clone.isover()) is not None:
        if result == result.DRAW:
            print("It's a draw!")
        else:
            player = "X" if board_clone.onturn == 1 else "O"
            print("Player {} won!".format(player))


def change_heuristic():
    global heuristic

    print("current:", heuristic.__name__)
    heuristics = [NopHeuristic, BadHeuristic]
    for i, h in enumerate(heuristics):
        print("{}: {}".format(i, h.__name__))

    i = input("H > ")
    while not i.isdigit() or int(i) < 0 or int(i) >= len(heuristics):
        if i == "q": return
        print("please choose a valid heuristic index")
        i = input("H > ")

    heuristic = heuristics[int(i)]
    print("new:", heuristic.__name__)


def new(args):
    global board, history

    if len(args) == 0:
        history.clear()
        board = Board(board.w, board.h, board.N)
        show()
        return

    if len(args) < 3:
        print("not enough arguments")
        return

    if not all(arg.isdigit() for arg in args):
        print("please provide integers")
        return

    history.clear()
    board = Board(int(args[0]), int(args[1]), int(args[2]))
    show()


def load(args):
    global board, history

    if len(args) == 0:
        print("please provide a sequence")
        return

    if not all(arg.isdigit() for arg in args):
        print("please provide only digits")

    history.clear()
    board = Board(board.w, board.h, board.N)

    for move in list(map(int, args)):
        board.play(move)
        history.append(move)

    show()


def toggle_automove():
    global automove

    automove = not automove
    print("automove is now ", end="")
    if automove: print("on")
    else: print("off")


def mirror():
    global board, history

    history = list(map(lambda x: board.w - 1 - x, history))
    board = Board.from_seq(board.w, board.h, board.N, history)

    show()


def shift(args):
    global board, history

    if len(args) == 0:
        print("please provide a direction to shift")
        return

    go = 0

    if   args[0] == "r":
        go = 1
    elif args[0] == "l":
        go = -1
    else:
        print("the arguments must be 'r' or 'l'")
        return

    if not all(0 <= x + go < board.w for x in history):
        print("impossible shift")
        return

    history = list(map(lambda x: x + go, history))
    board = Board.from_seq(board.w, board.h, board.N, history)

    show()



def count():
    print("movecount: {}".format(board.movecount))


def show():
    print("\n", board, sep="", end="")
    if len(history) > 0:
        print()
        print(*history)
    print()


def help_msg():
    print(
        "[0-n): make move",
        "u undo: undo last move",
        # "e eval [t]: evaluate state",
        # "b best [t]: make best move",
        "ab alphabeta [d t]: make alphabeta move",
        "nx negamax [d t]: make negamax move",
        "in insane [d t]: make insane move",
        "r random [n]: make n random moves",
        "h heuristic: choose heuristic",
        "n new [w h n]: new game",
        "l load seq: load game",
        "a automove: toggle automove",
        "m mirror: mirror the board",
        "sl shiftl: shift the board left",
        "sr shiftr: shift the board right",
        "c count: print movecount",
        "p print: print board",
        "q quit: quit the maker",
        "? help: show this help",
        sep="\n"
    )


def maker():
    prev_line = ""
    show()

    while True:
        symbol = "X" if len(history) % 2 == 0 else "O"
        line = input("{} > ".format(symbol)).split()

        if len(line) == 0: line = prev_line
        else: prev_line = line

        cmd = line[0]
        args = line[1:]

        if   cmd.isdigit():
            move(int(cmd))
        elif cmd == "u" or cmd == "undo":
            undo()
        elif cmd == "ab" or cmd == "alphabeta":
            solver(Alphabeta(), args)
        elif cmd == "nx" or cmd == "negamax":
            solver(Negamax(), args)
        elif cmd == "in" or cmd == "insane":
            solver(Insane(), args)
        elif cmd == "r" or cmd == "random":
            random(args)
        elif cmd == "h" or cmd == "heuristic":
            change_heuristic()
        elif cmd == "n" or cmd == "new":
            new(args)
        elif cmd == "l" or cmd == "load":
            load(args)
        elif cmd == "a" or cmd == "automove":
            toggle_automove()
        elif cmd == "m" or cmd == "mirror":
            mirror()
        elif cmd == "sl" or cmd == "shiftl":
            shift("l")
        elif cmd == "sr" or cmd == "shiftr":
            shift("r")
        elif cmd == "c" or cmd == "count":
            count()
        elif cmd == "p" or cmd == "print":
            show()
        elif cmd == "?" or cmd == "help":
            help_msg()
        elif cmd == "q" or cmd == "quit":
            exit()


if __name__ == "__main__":
    maker()
