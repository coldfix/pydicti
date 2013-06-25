"""
Case insensitive dictionary on top of a user defined underlying dictionary.

Entries in a `dicti` can be accessed case invariantly:

    >>> from pydicti import dicti, build_dicti, Dicti
    >>> keys = ['Hello', 'beautiful', 'world!']
    >>> values = [1, 2, 3]
    >>> z = list(zip(keys, values))
    >>> i = dicti(z)
    >>> assert "WorLD!" in i and "universe" not in i

However, the in calls like `.keys()` or `.items()` the keys are returned
as in their original case:

    >>> assert "Hello" in list(i.keys())

`dicti` can be "derived" from  another custom dictionary extension using
it as the underlying dictionary to gain additional properties like order
preservation:

    >>> from collections import OrderedDict
    >>> odicti = build_dicti(OrderedDict)
    >>> oi = odicti(z)
    >>> assert list(oi.keys()) == keys

The equality  comparison preserves  the semantics of  the base  type and
reflexitivity as best  as possible. This has impact  on the transitivity
of the comparison operator:

    >>> rz = list(zip(reversed(keys), reversed(values)))
    >>> roi = odicti(rz)
    >>> assert roi == i and i == oi
    >>> assert oi != roi and roi != oi  # NOT transitive!
    >>> assert oi == i and i == oi      # reflexive

Be careful with reflexitivity when comparing non-`dicti` types:

    >>> o = OrderedDict(oi)
    >>> oli = Dicti(oi.lower_dict())
    >>> assert oli == o
    >>> print(o == oli) # dependends on implementation of OrderedDict
    >>> print(o.__eq__(oli))

Note that `dicti` is the type corresponding to `builtins.dict`:

    >>> assert build_dicti(dict) is dicti

The  method   `Dicti`  is  convenient  for   creating  case  insensitive
dictionaries from a given object automatically using the objects type as
the underlying dictionary type.

    >>> assert oi == Dicti(o)
    >>> assert type(oi) is type(Dicti(o))

The subclassing approach works well with "badly" written code as in `json`
that checks for `isinstance(dict)`:

    >>> import json
    >>> assert oi == json.loads(json.dumps(oi), object_pairs_hook=odicti)

"""

import collections
from abc import ABCMeta

# internally used to allow keys that are not strings
def _lower(s):
    """Convert to lower case if possible."""
    try:
        return s.lower()
    except AttributeError:
        return s

# base class
class _dicti(collections.MutableMapping):
    """
    Dictionary with case insensitive lookups.

    Behaves  like  `dict`  except  that lookups  are  always  done  case
    insensitive. Case sensitivity is retained  in so far that calls like
    `.keys()` or `.items()` return the keys in their original form.

    Passing   dictionaries   that   have  multiple   keys   with   equal
    `.lower()`-case to the constructor, to `.update()` or to `.__eq__()`
    is undefined behaviour.

    Note that `dicti` is inherited from `collections.MutableMapping` and
    not from `builtins.dict`. This  means that `isinstance(dict)` checks
    will fail and  hence `json.dump()` will not  work automatically with
    `dicti` without some additional work.


    Implementation rationale (known pitfalls):

    When  subclassing  `builtins.dict`,  calling  `dict(Dicti(v))`  will
    bypass the `__iter__`+`__getitem__` interface  and return the actual
    dictionary. This means subclassing enforces us to use a two step key
    lookup like  done below. This  may lead to performance  issues. Also
    subclassing  has  some really  quirky  behaviour  when it  comes  to
    comparison.

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
_super = {}
def build_dicti(base):
    """
    Create `dicti` class using `base` as the underlying dictionary.

    `base`  is required  to  be a  `collections.MutableMapping`. If  the
    class has already been created, this will not create a new type, but
    rather lookup the existing type in a table.

    """
    if base not in _built_dicties:
        if not issubclass(base, collections.MutableMapping):
            raise TypeError("Not a mapping type: %s" % base)
        class Super(base, metaclass=ABCMeta):
            pass
        class Dicti(_dicti):
            pass
        Dicti.dict_ = base
        _built_dicties[base] = Dicti
        Super.register(Dicti)
        _super[base] = Super
    return _built_dicties[base]

def Dicti(obj):
    """
    Create case insensitive dictionary object from existing dictionary.

    The type of  `obj` is used as the type  of the underlying dictionary
    for the returned case insensitive dictionary.

    Since  this method  has the  same  name as  was used  to create  the
    class within  `build_dicti` this  allows `repr()`-esentations  to be
    invertible without further work.

    """
    return build_dicti(type(obj))(obj)

# `dicti` is the default case insensitive dictionary
dicti = build_dicti(dict)

# `odicti` is an ordered, case insensitive dictionary type
odicti = build_dicti(collections.OrderedDict)

