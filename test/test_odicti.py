# test utilities:
import unittest
import test.test_common

# tested module
import pydicti

# interoperability tests:
from json import loads, dumps

# setup logging
import logging
if __name__ == '__main__':
    logging.basicConfig()
logger = logging.getLogger(__name__)

try:
    loads('{}', object_pairs_hook=dict)
except TypeError:
    logger.warn('Not testing object_pairs_hook!')
    _test_json = test.test_common.TestBase.test_json
else:
    def _test_json(self):
        d = self.cls(self.simple)
        l = loads(dumps(d), object_pairs_hook=self.cls)
        self.checkItems(d.items(), l.items())

def _checkItems(self, a, b):
    unittest.TestCase.assertEqual(self, list(a), list(b))

try:
    from collections import OrderedDict
except ImportError:
    logger.warn('Not testing collections.OrderedDict!')
else:
    collections_OrderedDicti = pydicti.build_dicti(
        OrderedDict, 'collections_OrderedDicti')
    class Test_collections_OrderedDict(test.test_common.TestBase):
        base = OrderedDict
        cls = collections_OrderedDicti
        checkItems = _checkItems
        test_json = _test_json

try:
    from ordereddict import OrderedDict
except ImportError:
    logger.warn('Not testing ordereddict.OrderedDict!')
else:
    ordereddict_OrderedDicti = pydicti.build_dicti(
        OrderedDict, 'ordereddict_OrderedDicti')
    class Test_ordereddict_OrderedDict(test.test_common.TestBase):
        base = OrderedDict
        cls = ordereddict_OrderedDicti
        checkItems = _checkItems
        test_json = _test_json


if __name__ == '__main__':
    unittest.main()
