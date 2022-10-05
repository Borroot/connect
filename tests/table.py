import sys, os
sys.path.insert(0, os.getcwd() + "/connect")

from evaluation import Eval
from table import Table, Flag
import unittest


class TestTable(unittest.TestCase):

    def test_size(self):
        table = Table(14)
        self.assertEqual(len(table.table), 17)


    def test_entry(self):
        size = 5
        table = Table(size)

        self.assertEqual(len(table.table), size)
        for i in range(size):
            self.assertEqual(table.get(i), None)

        table.put(1, Eval(0, 0, const = Eval.MIN), Flag.UPPERBOUND)
        self.assertEqual(table.get(1), (Eval(0, 0, const = Eval.MIN), Flag.UPPERBOUND))

        table.put(6, Eval(0, 0, const = Eval.MAX), Flag.LOWERBOUND)
        self.assertEqual(table.get(6), (Eval(0, 0, const = Eval.MAX), Flag.LOWERBOUND))
        self.assertEqual(table.get(1), None)


    def test_count(self):
        table = Table(5)

        self.assertEqual(table.count(), 0)

        table.put(0, Eval(0, 0, const = Eval.MIN), Flag.UPPERBOUND)
        table.put(1, Eval(0, 0, const = Eval.MIN), Flag.UPPERBOUND)

        self.assertEqual(table.count(), 2)

        table.put(4, Eval(0, 0, const = Eval.MIN), Flag.UPPERBOUND)

        self.assertEqual(table.count(), 3)

        table.put(5, Eval(0, 0, const = Eval.MIN), Flag.UPPERBOUND)

        self.assertEqual(table.count(), 3)
