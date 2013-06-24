"""
Case insensitive dictionary on top of a user defined underlying dictionary.

The case of the keys is preserved as they are set. However, entries can be
accessed case invariantly.

>>> keys = ['Hello', 'beautiful', 'world!']
>>> values = [1, 2, 3]
>>> i = dicti(zip(keys, values))
>>> "WORLD!" in i
True

>>> "universe" in i
False

>>> "Hello" in list(i.keys())
True

``dicti`` can be "derived" from another custom dictionary extension using it
as the underlying dictionary.

>>> from collections import OrderedDict
>>> odicti = build_dicti(OrderedDict)
>>> oi = odicti(zip(keys, values))
>>> "hELLo" in oi
True

>>> list(oi.keys())
['Hello', 'beautiful', 'world!']

>>> Dicti(o) == oi
True

Note that ``dicti`` is the type corresponding to ``builtins.dict``:

>>> build_dicti(dict) is dicti
True

The method ``Dicti`` is convenient for creating case insensitive dictionaries
from a given object automatically using the objects type as the underlying
dictionary type.

>>> oi
Dicti(OrderedDict([('Hello', 1), ('beautiful', 2), ('world!', 3)]))
>>> o = OrderedDict(zip(keys, values))
>>> oi == Dicti(o)
True

>>> type(oi) is type(Dicti(o))
True

"""

import collections

# internally used to allow keys that are not strings
def _lower(s):
    """
    Convert to lower case if possible.
    """
    try:
        return s.lower()
    except AttributeError:
        return s

# base class
class dicti(collections.abc.MutableMapping):
    """
    Dictionary with case insensitive lookups.

    Behaves like ``dict`` except that lookups are always done case
    insensitive. Case sensitivity is retained in so far that ``.keys()`` etc
    return the keys in their original form.

    Passing dictionaries that have multiple keys with equal ``.lower()``-case
    to the constructor, to ``.update()`` or to ``.__eq__()`` is undefined
    behaviour.

    >>> keys = ['Hello', 'beautiful', 'world!']
    >>> values = [1, 2, 3]
    >>> i = dicti(zip(keys, values))
    >>> "WORLD" in i
    True
    >>> "universe" in i
    False
    >>> "Hello" in list(i.keys())
    True

    """

    # Underlying dictionary:
    dict_ = dict

    # Constructor:
    def __init__(self, data={}, **kwargs):
        """Initialize a case insensitive dictionary from the arguments."""
        self._data = self.dict_()
        self.update(data, **kwargs)

    # MutableMapping methods:
    def __getitem__(self, key):
        """Get the value for ``key`` case insensitively."""
        return self._data[_lower(key)][1]

    def __setitem__(self, key, value):
        """Set the value for ``key`` and assume new case."""
        self._data[_lower(key)] = (key, value)

    def __delitem__(self, key):
        """Delete the item for ``key`` case insensitively."""
        del self._data[_lower(key)]

    def __iter__(self):
        """Iterate over all keys in their original case."""
        return (k for k,v in self._data.values())

    def __len__(self):
        """Return the number of items in the dictionary."""
        return len(self._data)

    # Implemented by MutableMapping:
    # __contains__
    # keys
    # items
    # values
    # get
    # pop
    # popitem
    # clear
    # update
    # setdefault

    # Methods for polymorphism with ``builtins.dict``:
    def copy(self):
        return self.__copy__()

    def iter(self):
        return iter(self.__iter())

    # Standard operations:
    def __eq__(self, other):
        """Compare values for the same case insensitivey keys.""" 
        if type(other) == type(self):
            pass
        elif isinstance(other, collections.Mapping):
            other = self.__class__(other)
        else:
            return NotImplemented
        return self.dict_(self.lower_items()) == self.dict_(other.lower_items())

    def __copy__(self):
        """Create a copy of the dictionary."""
        return self.__class__(self._data.values())

    def __repr__(self):
        """Representation string. Usually ``dicti`` or ``Dicti(type)``."""
        return '%s(%r)' % (self.__class__.__name__, self.dict_(self.items()))
 
    # extra methods:
    def lower_items(self):
        """Iterate over (key,value) pairs with lowercase keys."""
        return ((k, v[1]) for k,v in self._data.items())


_built_dicties = {}
def build_dicti(base):
    """
    Create ``dicti`` class using ``base`` as the underlying dictionary.

    ``base`` is required to be a ``collections.abc.MutableMapping``. If the
    class has already been created, this will not create a new type, but rather
    lookup the existing type in a table.

    """
    if base not in _built_dicties:
        if not issubclass(base, collections.abc.MutableMapping):
            raise TypeError("Not a mapping type: %s" % base)
        class Dicti(dicti):
            pass
        Dicti.dict_ = base
        _built_dicties[base] = Dicti
    return _built_dicties[base]

def Dicti(obj):
    """
    Create a case insensitive dictionary object from an existing dictionary.

    The type of ``obj`` is used as the type of the underlying dictionary for
    the returned case insensitive dictionary.

    Since this method has the same name as was used to create the class within
    ``build_dicti`` this allows ``str()`` representations to be invertible
    without further work.

    """
    return build_dicti(type(obj))(obj)

# initialize ``build_dicti(dict)`` to be just ``dicti``
_built_dicties[dict] = dicti

# ``odicti`` is an ordered, case insensitive dictionary type
odicti = build_dicti(collections.OrderedDict)

