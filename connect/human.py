from player import Player


class Human(Player):

    def _move(self, board, depth=None, heuristic=None, timeout=None):
        symbol = "X" if board.onturn == 0 else "O"
        line = input("{} > ".format(symbol))

        while not line.isdigit() or int(line) < 0 or int(line) >= board.w \
              or not board.canplay(int(line)):
            print("please provide a valid move in [0,{})".format(board.w))
            line = input("{} > ".format(symbol))

        return int(line)


    def __str__(self):
        return "human"
