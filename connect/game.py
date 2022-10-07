from rand import Random
from human import Human
from board import Board
import board
from enum import Enum


class Result(Enum):

    PLAYER1 = 0
    PLAYER2 = 1
    DRAW = 2


    def __str__(self):
        if self == Result.DRAW:
            return "draw"
        else:
            return "player{}".format(self.value + 1)


class Game:

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.onturn = 0
        self.board = Board(7, 6, 4)


    def run(self, verbose):
        while True:
            if verbose: print(self.board)

            player = self.players[self.onturn]
            move = player.move(self.board)
            self.board.play(move)

            if (result := self.board.isover()) is not None:
                if verbose: print(self.board)
                if result == board.Result.DRAW:
                    return Result.DRAW
                else:
                    return Result(self.onturn)

            self.onturn ^= 1


if __name__ == "__main__":
    """Simulate one or multiple games."""
    players = [Random(), Random()]
    game = Game(*players)
    result = game.run(True)

    if result == Result.DRAW:
        print("It's a draw!")
    else:
        print("{} ({}) won!".format(players[result.value], result))
