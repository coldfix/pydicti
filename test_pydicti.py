import unittest
from copy import copy, deepcopy

from pydicti import dicti

class Test_pydicti(unittest.TestCase):

    def setUp(self):
        self.i = dicti(zip("abcde", range(5)))
        self.i['h'] = {'x': 3}

    def test_pop(self):
        self.assertEqual(self.i.pop('A'), 0)
        self.assertRaises(KeyError, self.i.pop, 'A')
        self.assertEqual(self.i.pop('A', 5), 5)
