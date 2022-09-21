from connect.board import Board, Result
import unittest

class TestBoard(unittest.TestCase):

    def test_isover_empty(self):
        board = Board(7, 6, 4)
        self.assertEqual(board.isover(), None)


    def test_isover_horizontal(self):
        board0 = Board.from_codex(7, 6, 4, "001122")
        board1 = Board.from_codex(7, 6, 4, "0011223")
        self.assertEqual(board0.isover(), None)
        self.assertEqual(board1.isover(), Result.WIN)

        board2 = Board.from_codex(7, 6, 4, "665544")
        board3 = Board.from_codex(7, 6, 4, "6655443")
        self.assertEqual(board2.isover(), None)
        self.assertEqual(board3.isover(), Result.WIN)

        board4 = Board.from_codex(7, 6, 4, "010101232323103201230616263")
        self.assertEqual(board4.isover(), Result.WIN)

        board5 = Board.from_codex(7, 6, 4, "656565434343563465436050403")
        self.assertEqual(board5.isover(), Result.WIN)


    def test_isover_vertical(self):
        board0 = Board.from_codex(7, 6, 4, "010101")
        board1 = Board.from_codex(7, 6, 4, "0101010")
        self.assertEqual(board0.isover(), None)
        self.assertEqual(board1.isover(), Result.WIN)

        board2 = Board.from_codex(7, 6, 4, "656565")
        board3 = Board.from_codex(7, 6, 4, "6565656")
        self.assertEqual(board2.isover(), None)
        self.assertEqual(board3.isover(), Result.WIN)

        board4 = Board.from_codex(7, 6, 4, "1010010101")
        board5 = Board.from_codex(7, 6, 4, "10100101010")
        self.assertEqual(board4.isover(), None)
        self.assertEqual(board5.isover(), Result.WIN)

        board6 = Board.from_codex(7, 6, 4, "5656656565")
        board7 = Board.from_codex(7, 6, 4, "56566565656")
        self.assertEqual(board6.isover(), None)
        self.assertEqual(board7.isover(), Result.WIN)


    def test_isover_diagonal1(self):
        board0 = Board.from_codex(7, 6, 4, "32211010060")
        self.assertEqual(board0.isover(), Result.WIN)

        board1 = Board.from_codex(7, 6, 4, "65544343303")
        self.assertEqual(board1.isover(), Result.WIN)

        board2 = Board.from_codex(7, 6, 4, "333222221111100030030")
        self.assertEqual(board2.isover(), Result.WIN)

        board3 = Board.from_codex(7, 6, 4, "666555554444433363363")
        self.assertEqual(board3.isover(), Result.WIN)


    def test_isover_diagonal2(self):
        board0 = Board.from_codex(7, 6, 4, "34455656606")
        self.assertEqual(board0.isover(), Result.WIN)

        board1 = Board.from_codex(7, 6, 4, "01122323363")
        self.assertEqual(board1.isover(), Result.WIN)

        board2 = Board.from_codex(7, 6, 4, "333444445555566636636")
        self.assertEqual(board2.isover(), Result.WIN)

        board3 = Board.from_codex(7, 6, 4, "000111112222233303303")
        self.assertEqual(board3.isover(), Result.WIN)


if __name__ == '__main__':
    unittest.main()
