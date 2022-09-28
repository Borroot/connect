import sys, os
sys.path.insert(0, os.getcwd() + "/connect")

from result import Result
from board import Board
import unittest


class TestIsOver(unittest.TestCase):

    def test_isover_empty(self):
        board = Board(7, 6, 4)
        self.assertEqual(board.isover(), None)


    def test_isover_horizontal(self):
        board0 = Board.from_seq(7, 6, 4, [0,0,1,1,2,2])
        board1 = Board.from_seq(7, 6, 4, [0,0,1,1,2,2,3])
        self.assertEqual(board0.isover(), None)
        self.assertEqual(board1.isover(), Result.WIN)

        board2 = Board.from_seq(7, 6, 4, [6,6,5,5,4,4])
        board3 = Board.from_seq(7, 6, 4, [6,6,5,5,4,4,3])
        self.assertEqual(board2.isover(), None)
        self.assertEqual(board3.isover(), Result.WIN)

        board4 = Board.from_seq(7, 6, 4, [0,1,0,1,0,1,2,3,2,3,2,3,1,0,3,2,0,1,2,3,0,6,1,6,2,6,3])
        self.assertEqual(board4.isover(), Result.WIN)

        board5 = Board.from_seq(7, 6, 4, [6,5,6,5,6,5,4,3,4,3,4,3,5,6,3,4,6,5,4,3,6,0,5,0,4,0,3])
        self.assertEqual(board5.isover(), Result.WIN)


    def test_isover_vertical(self):
        board0 = Board.from_seq(7, 6, 4, [0,1,0,1,0,1])
        board1 = Board.from_seq(7, 6, 4, [0,1,0,1,0,1,0])
        self.assertEqual(board0.isover(), None)
        self.assertEqual(board1.isover(), Result.WIN)

        board2 = Board.from_seq(7, 6, 4, [6,5,6,5,6,5])
        board3 = Board.from_seq(7, 6, 4, [6,5,6,5,6,5,6])
        self.assertEqual(board2.isover(), None)
        self.assertEqual(board3.isover(), Result.WIN)

        board4 = Board.from_seq(7, 6, 4, [1,0,1,0,0,1,0,1,0,1])
        board5 = Board.from_seq(7, 6, 4, [1,0,1,0,0,1,0,1,0,1,0])
        self.assertEqual(board4.isover(), None)
        self.assertEqual(board5.isover(), Result.WIN)

        board6 = Board.from_seq(7, 6, 4, [5,6,5,6,6,5,6,5,6,5])
        board7 = Board.from_seq(7, 6, 4, [5,6,5,6,6,5,6,5,6,5,6])
        self.assertEqual(board6.isover(), None)
        self.assertEqual(board7.isover(), Result.WIN)


    def test_isover_diagonal1(self):
        board0 = Board.from_seq(7, 6, 4, [3,2,2,1,1,0,1,0,0,6,0])
        self.assertEqual(board0.isover(), Result.WIN)

        board1 = Board.from_seq(7, 6, 4, [6,5,5,4,4,3,4,3,3,0,3])
        self.assertEqual(board1.isover(), Result.WIN)

        board2 = Board.from_seq(7, 6, 4, [3,3,3,2,2,2,2,2,1,1,1,1,1,0,0,0,3,0,0,3,0])
        self.assertEqual(board2.isover(), Result.WIN)

        board3 = Board.from_seq(7, 6, 4, [6,6,6,5,5,5,5,5,4,4,4,4,4,3,3,3,6,3,3,6,3])
        self.assertEqual(board3.isover(), Result.WIN)


    def test_isover_diagonal2(self):
        board0 = Board.from_seq(7, 6, 4, [3,4,4,5,5,6,5,6,6,0,6])
        self.assertEqual(board0.isover(), Result.WIN)

        board1 = Board.from_seq(7, 6, 4, [0,1,1,2,2,3,2,3,3,6,3])
        self.assertEqual(board1.isover(), Result.WIN)

        board2 = Board.from_seq(7, 6, 4, [3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,6,3,6,6,3,6])
        self.assertEqual(board2.isover(), Result.WIN)

        board3 = Board.from_seq(7, 6, 4, [0,0,0,1,1,1,1,1,2,2,2,2,2,3,3,3,0,3,3,0,3])
        self.assertEqual(board3.isover(), Result.WIN)


class TestKey(unittest.TestCase):

    def print_key(key, w, h):
        digits = []
        while key:
            digits.append(int(key % 3))
            key //= 3

        while len(digits) != w * h:
            digits.append(0)

        for y in range(h):
            print("".join(map(str, digits[y * w: (y + 1) * w])))


    def test_key(self):
        # TestKey.print_key(board.key, board.w, board.h)

        board = Board(7, 6, 4)
        self.assertEqual(board.key, int(
            "".join([
                "0000000",
                "0000000",
                "0000000",
                "0000000",
                "0000000",
                "0000000",
            ])[::-1], 3
        ))

        board.play(0)
        self.assertEqual(board.key, int(
            "".join([
                "0000000",
                "0000000",
                "0000000",
                "0000000",
                "0000000",
                "1000000",
            ])[::-1], 3
        ))

        board.play(0)
        self.assertEqual(board.key, int(
            "".join([
                "0000000",
                "0000000",
                "0000000",
                "0000000",
                "2000000",
                "1000000",
            ])[::-1], 3
        ))

        board.play(0)
        board.play(0)
        board.play(0)
        board.play(0)

        self.assertEqual(board.key, int(
            "".join([
                "2000000",
                "1000000",
                "2000000",
                "1000000",
                "2000000",
                "1000000",
            ])[::-1], 3
        ))

        board.play(3)
        board.play(6)
        board.play(6)
        board.play(6)
        board.play(6)
        board.play(6)
        board.play(6)

        self.assertEqual(board.key, int(
            "".join([
                "2000001",
                "1000002",
                "2000001",
                "1000002",
                "2000001",
                "1001002",
            ])[::-1], 3
        ))
