import sys, os
sys.path.insert(0, os.getcwd() + "/connect")

from result import Result
import unittest


class TestResult(unittest.TestCase):

    def test_result_negation(self):
        self.assertEqual( Result.WIN,  -Result.LOSS)
        self.assertEqual(-Result.WIN,   Result.LOSS)
        self.assertEqual( Result.DRAW, -Result.DRAW)
