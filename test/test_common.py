__test__ = False

# test utilities:
import unittest

# interoperability tests:
import copy
import json
import pickle

# tested module:
import pydicti


def c(k):
    """Capitalize or decapitalize one letter depending on its ascii value."""
    if isinstance(k, str):
        return k.lower() if ord(k) % 2 == 0 else k.upper()
    return k

class TestBase(unittest.TestCase):
    base = None
    cls = None

    # utilities:
    @property
    def simple(self):
        return list(zip("ABCDefgh", range(8)))

    @property
    def items(self):
        special = 2, (), None, True
        return self.simple + list(zip(special, range(len(special))))

    @property
    def more_items(self):
        return list(zip("nopqRSTV", range(14, 22)))

    # TODO: check cases

    # test properties of the type:
    def test_subclass(self):
        self.assertTrue(issubclass(self.cls, self.base))

    def test_build_dicti(self):
        self.assertIs(pydicti.build_dicti(self.base), self.cls)

    # test the constructor:
    def test_construction_from_iterable(self):
        d = self.cls((k,v) for k,v in self.items)
        self.checkItems(d.items(), self.items)

    def test_construction_from_base(self):
        b = self.base(self.items)
        d = self.cls(b)
        self.checkItems(d.items(), b.items())

    def test_construction_from_kwargs(self):
        kwargs = dict(self.simple)
        d = self.cls(**kwargs)
        self.assertItemsEqual(d.items(), self.simple)

    # test basic access
    def test_setitem(self):
        d = self.cls((c(k),0) for k,v in self.items)
        for k,v in self.items:
            d[k] = v
        self.checkItems(d.items(), self.items)
        for k,v in self.more_items:
            d[k] = v
        self.checkItems(d.items(), self.items + self.more_items)

    def test_getitem(self):
        d = self.cls(self.items)
        self.checkItems([(k,d[c(k)]) for k,v in self.items], self.items)
        def getitem(d, k):
            return d[c(k)]
        for k,v in self.more_items:
            self.assertRaises(KeyError, getitem, d, k)

    def test_get(self):
        d = self.cls(self.items)
        self.checkItems([(k,d.get(c(k))) for k,v in self.items], self.items)
        for k,v in self.more_items:
            self.assertIs(d.get(k), None)
        for k,v in self.more_items:
            self.assertEqual(d.get(k, v), v)

    def test_delitem(self):
        p = self.items
        d = self.cls(p)
        while p:
            k,v = p.pop()
            del d[c(k)]
            self.checkItems(d.items(), p)
        def delitem(d, k):
            del d[c(k)]
        for k,v in self.items + self.more_items:
            self.assertRaises(KeyError, delitem, d, k)

    def test_contains(self):
        d = self.cls(self.items)
        for k,v in self.items:
            self.assertTrue(c(k) in d)
        for k,v in self.more_items:
            self.assertFalse(k in d)

    def test_clear(self):
        d = self.cls(self.items)
        d.clear()
        self.checkItems(d.items(), ())
        d.clear()
        self.checkItems(d.items(), ())

    def test_pop(self):
        p = self.items
        d = self.cls(p)
        while p:
            k,v = p.pop()
            v2 = d.pop(c(k))
            self.assertEqual(v2, v)
        def popitem(d, k, *a):
            return d.pop(c(k), *a)
        for k,v in self.items:
            self.assertRaises(KeyError, popitem, d, k)
        for k,v in self.items:
            self.assertEqual(d.pop(c(k), v), v)

    def test_update(self):
        d = self.cls((k,v-1) for k,v in self.items)
        d.update(self.base())

    def test_setdefault(self):
        d = self.cls(self.items)
        for k,v in self.items:
            d.setdefault(c(k), v+1)
        for k,v in self.more_items:
            d.setdefault(k, v)
        self.checkItems(d.items(), self.items + self.more_items)

    def test_eq(self):
        d = self.cls(self.items)
        self.assertEqual(d, d)
        self.assertEqual(d, self.cls(self.items))
        self.assertEqual(d, self.base(self.items))

        k0,v0 = self.items[0]

        d0 = self.cls()
        self.assertNotEqual(d, d0)

        d1 = self.cls(self.items)
        d1[k0] = v0 + 1
        self.assertNotEqual(d, d1)

        d2 = self.cls(self.items)
        del d2[k0]
        self.assertNotEqual(d, d2)

        d3 = self.cls(self.items)
        d3[self.more_items[0][0]] = 0
        self.assertNotEqual(d, d3)

        d4 = self.cls(self.more_items)
        self.assertNotEqual(d, d4)

    def test_len(self):
        d = self.cls(self.items)
        self.assertEqual(len(d), len(self.items))

    def test_bool(self):
        d = self.cls(self.items)
        self.assertTrue(d)
        d.clear()
        self.assertFalse(d)
        self.assertFalse(self.cls())

    # test iteration
    def test_iter(self):
        d = self.cls(self.items)
        self.checkItems([(k,d[k]) for k in d], self.items)
        self.checkItems([(k,d[k]) for k in d.iter()], self.items)
        items = []
        i = d.iter()
        try:
            while True:
                k = next(i)
                items.append((k, d[k]))
        except StopIteration:
            pass
        finally:
            self.checkItems(items, self.items)

    def test_keys(self):
        d = self.cls(self.items)
        self.checkItems(d.keys(), [k for k,v in self.items])

    def test_values(self):
        d = self.cls(self.items)
        self.checkItems(d.values(), [v for k,v in self.items])

    def test_cast_to_base(self):
        d = self.cls(self.items)
        b = self.base(d)
        self.checkItems(b.items(), d.items())

    # copying, serialization, etc
    def test_copy(self):
        d = self.cls(self.items)
        k0,v0 = self.items[0]
        d[k0] = {}
        c0 = copy.copy(d)
        self.assertIsNot(c0, d)
        self.assertEqual(c0, d)
        self.assertIs(c0[k0], d[k0])
        c1 = d.copy()
        self.assertIsNot(c1, d)
        self.assertEqual(c1, d)
        self.assertIs(c1[k0], d[k0])

    def test_deepcopy(self):
        d = self.cls(self.items)
        k0,v0 = self.items[0]
        d[k0] = {}
        c = copy.deepcopy(d)
        self.assertEqual(c, d)
        self.assertIsNot(c[k0], d[k0])
        self.assertEqual(c[k0], d[k0])

    def test_pickle(self):
        d = self.cls(self.simple)
        l = pickle.loads(pickle.dumps(d))
        self.assertItemsEqual(d.items(), l.items())

    def test_json(self):
        d = self.cls(self.simple)
        l = json.loads(json.dumps(d), object_hook=self.cls)
        self.assertItemsEqual(d.items(), l.items())

    # Add non-existing assertions in python26:
    try:
        unittest.TestCase.assertIs
    except AttributeError:  # python2.6:
        def assertIs(self, expr1, expr2):
            if expr1 is not expr2:
                self.fail('%r is not %r' % (expr1, expr2))

    try:
        unittest.TestCase.assertIsNot
    except AttributeError:  # python2.6:
        def assertIsNot(self, expr1, expr2):
            if expr1 is expr2:
                self.fail('unexpectedly identical: %s' % (expr1,))

    try:                    # python2:
        unittest.TestCase.assertItemsEqual
    except AttributeError:  # python3:
        try:
            assertItemsEqual = unittest.TestCase.assertCountEqual
        except AttributeError:
            def assertItemsEqual(self, a, b):
                self.assertEqual(sorted(a), sorted(b))

    def checkItems(self, a, b):
        return self.assertItemsEqual(a, b)
