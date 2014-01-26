import unittest
from test.test_compat import TestCase

try:
    from pydicti import dicti, odicti, Dicti, build_dicti
    from collections import OrderedDict
except ImportError:
    # Drop this test if OrderedDict can not be imported (py26):
    __test__ = False

class Test_odicti(TestCase):
    def setUp(self):
        self.k = list('abcdefghijklm')
        self.v = list(range(13))
        self.z = list(zip(self.k, self.v))
        self.o = odicti(self.z)
        self.i = dicti(self.z)
        self.r = odicti(reversed(self.z))

    def test_order(self):
        self.assertEqual(self.z, list(self.o.items()))
        self.assertEqual(self.k, list(self.o.keys()))
        self.assertEqual(self.v, list(self.o.values()))

    def test_reflexitivity(self):
        self.assertEqual(self.r, self.i)
        self.assertEqual(self.i, self.r)
        self.assertNotEqual(self.r, self.o)
        self.assertNotEqual(self.o, self.r)
        self.assertEqual(self.i, self.o)
        self.assertEqual(self.o, self.i)

    def test_build_dicti(self):
        Do = Dicti(OrderedDict(self.z))
        self.assertEqual(self.o, Do)
        self.assertIs(odicti, build_dicti(OrderedDict))
        self.assertIs(type(self.o), type(Do))

    def test_json(self):
        from json import loads, dumps
        self.assertEqual(self.o,
                         loads(dumps(self.o), object_pairs_hook=odicti))

if __name__ == '__main__':
    unittest.main()
