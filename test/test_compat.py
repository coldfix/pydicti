import unittest

class TestCase(unittest.TestCase):
    # Add non-existing assertions in python26:
    try:
        unittest.TestCase.assertIs
    except AttributeError:
        def assertIs(self, expr1, expr2):
            if expr1 is not expr2:
                self.fail('%r is not %r' % (expr1, expr2))

    try:
        unittest.TestCase.assertIsNot
    except AttributeError:
        def assertIsNot(self, expr1, expr2, msg=None):
            if expr1 is expr2:
                self.fail('unexpectedly identical: %s' % (expr1,))
