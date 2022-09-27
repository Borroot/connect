from board import Board
from rand import Random
from negamax import Negamax
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


def undo():
    global board, history

    if not history:
        return

    history.pop()
    board = Board.from_codex(board.w, board.h, board.N, "".join(map(str, history)))

    show()


def negamax(args):
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

    result = Negamax().move(board, depth, heuristic(board.ML, board.N), timeout)

    if isinstance(result, Stats):
        print("timeout reached at {}s".format(timeout))
        print(result)
    else:
        bestmoves, bestvalue, stats = result
        chosen = choice(bestmoves)

        print(
            "{} -> {}".format(bestmoves, chosen),
            "eval: {} ({})".format(bestvalue, bestvalue._n),
            stats,
            sep="\n"
        )

        if automove:
            move(chosen)


def random():
    if board.isover() is not None:
        print("game is already over")
        return

    move(Random().move(board))


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
    global board

    if len(args) == 0:
        board = Board(board.w, board.h, board.N)
        show()
        return

    if len(args) < 3:
        print("not enough arguments")
        return

    if not all(arg.isdigit() for arg in args):
        print("please provide integers")
        return

    board = Board(int(args[0]), int(args[1]), int(args[2]))
    show()


def load(args):
    global board, history

    if len(args) == 0:
        print("please provide a codex")
        return

    if board.w > 10:
        print("codex not supported for width > 10")
        return

    if not all(arg.isdigit() for arg in args):
        print("please provide only digits")

    codex = args[0]
    w = board.w
    h = board.h
    N = board.N

    if len(args) == 4:
        w = int(args[0])
        h = int(args[1])
        N = int(args[2])
        codex = args[3]

    history.clear()
    board = Board(w, h, N)

    for c in codex:
        board.play(int(c))
        history.append(int(c))

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
    board = Board.from_codex(board.w, board.h, board.N, "".join(map(str, history)))

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
        print("sadly this shift is not possible")
        return

    history = list(map(lambda x: x + go, history))
    board = Board.from_codex(board.w, board.h, board.N, "".join(map(str, history)))

    show()



def count():
    print("movecount: {}".format(board.movecount))


def show():
    print("\n", board, sep="", end="")
    if board.w <= 10: print(*history, sep="")
    if len(history) > 0: print()


def help_msg():
    print(
        "[0-n): make move",
        "u undo: undo last move",
        # "e eval [t]: evaluate state",
        # "b best [t]: make best move",
        "n negamax [d t]: make negamax move",
        "r random: make random move",
        "h heuristic: choose heuristic",
        "n new [w h n]: new game",
        "l load [w h n] codex: load game",
        "a automove: toggle automove",
        "m mirror: mirror the board",
        "s shift r|l: shift the board",
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
        elif cmd == "n" or cmd == "negamax":
            negamax(args)
        elif cmd == "r" or cmd == "random":
            random()
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
        elif cmd == "s" or cmd == "shift":
            shift(args)
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
