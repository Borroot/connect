from board import Board
from rand import Random
import random as rand


board = Board(7, 6, 4)
history = []


def move(play):
    global board, history

    if play < 0 or play >= board.w:
        print("not in range of [0,{})".format(board.n))
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
    board = Board.from_codex(board.w, board.h, board.n, "".join(map(str, history)))

    show()


def random():
    if board.isover() is not None:
        print("game is already over")
        return

    move(Random().move(board))


def new(args):
    global board

    if len(args) == 0:
        board = Board(board.w, board.h, board.n)
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
    n = board.n

    if len(args) == 4:
        w = int(args[0])
        h = int(args[1])
        n = int(args[2])
        codex = args[3]

    history.clear()
    board = Board(w, h, n)

    for c in codex:
        board.play(int(c))
        history.append(int(c))

    show()


def mirror():
    global board, history

    history = list(map(lambda x: board.w - 1 - x, history))
    board = Board.from_codex(board.w, board.h, board.n, "".join(map(str, history)))

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
    board = Board.from_codex(board.w, board.h, board.n, "".join(map(str, history)))

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
        # "e eval [timeout]: evaluate state",
        # "b best [timeout]: make best move",
        "r random: make random move",
        "n new [w h n]: new game",
        "l load [w h n] codex: load game",
        "m mirror: mirror the board",
        "s shift r|l: shift the board",
        "c count: print movecount",
        "p print: print board",
        "q quit: quit the maker",
        "h help: show this help",
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
        elif cmd == "r" or cmd == "random":
            random()
        elif cmd == "n" or cmd == "new":
            new(args)
        elif cmd == "l" or cmd == "load":
            load(args)
        elif cmd == "m" or cmd == "mirror":
            mirror()
        elif cmd == "s" or cmd == "shift":
            shift(args)
        elif cmd == "c" or cmd == "count":
            count()
        elif cmd == "p" or cmd == "print":
            show()
        elif cmd == "h" or cmd == "help":
            help_msg()
        elif cmd == "q" or cmd == "quit":
            exit()


if __name__ == "__main__":
    maker()
