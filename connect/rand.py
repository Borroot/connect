from player import Player
import random


class Random(Player):

    def move(self, board):
        return random.choice(board.moves())


    def __str__(self):
        return "random"
