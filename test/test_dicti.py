import unittest
from test.test_compat import TestCase
from copy import copy, deepcopy
from json import loads, dumps

from pydicti import dicti

class Test_pydicti(TestCase):
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

    def test_setitem(self):
        i = dicti(a=0)
        i['a'] = 1
        self.assertEqual(i['a'], 1)
        i['a'] = 2
        self.assertEqual(i['a'], 2)

    def test_deepcopy(self):
        c = deepcopy(self.i)
        self.assertIsNot(c['h'], self.i['h'])
        self.assertEqual(c['h'], self.i['h'])

    def test_pop(self):
        self.assertEqual(self.i.pop('A'), 0)
        self.assertRaises(KeyError, self.i.pop, 'A')
        self.assertEqual(self.i.pop('A', 5), 5)

    def test_json(self):
        self.assertEqual(self.i,
                         loads(dumps(self.i), object_hook=dicti))

if __name__ == '__main__':
    unittest.main()
