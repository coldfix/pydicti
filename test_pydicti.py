import unittest
from copy import copy, deepcopy

from pydicti import dicti

class Test_pydicti(unittest.TestCase):

    def setUp(self):
        self.i = dicti(zip("abcde", range(5)))
        self.i['h'] = {'x': 3}

    def test_copy(self):
        c = copy(self.i)

        c['a'] = 5
        self.i['A'] = 6

        self.assertIs(c['H'], self.i['h'])
        self.assertEqual(c['a'], 5)
        self.assertEqual(self.i['a'], 6)

    def test_deepcopy(self):
        c = deepcopy(self.i)
        self.assertIsNot(c['h'], self.i['h'])
        self.assertEqual(c['h'], self.i['h'])

    def test_pop(self):
        self.assertEqual(self.i.pop('A'), 0)
        self.assertRaises(KeyError, self.i.pop, 'A')
        self.assertEqual(self.i.pop('A', 5), 5)
