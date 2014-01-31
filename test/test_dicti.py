import unittest
import test.test_common

from pydicti import build_dicti

class Test_dicti(test.test_common.TestBase):
    base = dict
    cls = build_dicti(dict)

if __name__ == '__main__':
    unittest.main()
