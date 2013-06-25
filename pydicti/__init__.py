"""
Case insensitive dictionary on top of a user defined underlying dictionary.

The case of the keys is preserved  as they are set. However, entries can
be accessed case invariantly.

    >>> keys = ['Hello', 'beautiful', 'world!']
    >>> values = [1, 2, 3]
    >>> i = dicti(zip(keys, values))
    >>> "WORLD!" in i
    True

    >>> "universe" not in i
    True

    >>> "Hello" in list(i.keys())
    True

`dicti` can be "derived" from  another custom dictionary extension using
it as the underlying dictionary.

    >>> from collections import OrderedDict
    >>> odicti = build_dicti(OrderedDict)
    >>> oi = odicti(zip(keys, values))
    >>> "hELLo" in oi
    True

    >>> list(oi.keys())
    ['Hello', 'beautiful', 'world!']

    >>> Dicti(o) == oi
    True

Note that `dicti` is the type corresponding to `builtins.dict`:

    >>> build_dicti(dict) is dicti
    True

The  method   `Dicti`  is  convenient  for   creating  case  insensitive
dictionaries from a given object automatically using the objects type as
the underlying dictionary type.

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

# make class
def _make_dicti(dict_):
    class Dicti(dict_):
        """
        Dictionary with case insensitive lookups.

        Behaves like  `dict` except  that lookups  are always  done case
        insensitive. Case sensitivity  is retained in so  far that calls
        like `.keys()` or  `.items()` return the keys  in their original
        form.

        Passing  dictionaries   that  have  multiple  keys   with  equal
        `.lower()`-case  to  the  constructor,   to  `.update()`  or  to
        `.__eq__()` is undefined behaviour.

            >>> keys = ['Hello', 'beautiful', 'world!']
            >>> values = [1, 2, 3]
            >>> i = dicti(zip(keys, values))
            >>> "WORLD" in i
            True
            >>> "universe" in i
            False
            >>> "Hello" in list(i.keys())
            True

        Note  that `dicti`  is  inherited  from `builtins.dict`  instead
        of   from   `collections.MutableMapping`.    This   means   that
        `isinstance(d,dict)` checks will  succeed and `json.dump()` will
        work automatically with `dicti`.

        """

        # Constructor:
        def __init__(self, data={}, **kwargs):
            """Initialize a case insensitive dictionary from the arguments."""
            dict_.__init__(self)
            self.update(data, **kwargs)

        # MutableMapping methods:
        def __getitem__(self, key):
            """Get the value for `key` case insensitively."""
            return dict_.__getitem__(self, _lower(key))[1]

        def __setitem__(self, key, value):
            """Set the value for `key` and assume new case."""
            dict_.__setitem__(self, _lower(key), (key, value))

        def __delitem__(self, key):
            """Delete the item for `key` case insensitively."""
            dict_.__delitem__(self, _lower(key))

        def __iter__(self):
            """Iterate over all keys in their original case."""
            return (dict_.__getitem__(self, k)[0]
                    for k in dict_.__iter__(self))

        # Implemented by `dict_`
        # __len__

        # Implemented by `MutableMapping`:
        __contains__ = collections.MutableMapping.__contains__
        keys         = collections.MutableMapping.keys
        items        = collections.MutableMapping.items
        values       = collections.MutableMapping.values
        get          = collections.MutableMapping.get
        pop          = collections.MutableMapping.pop
        popitem      = collections.MutableMapping.popitem
        clear        = collections.MutableMapping.clear
        update       = collections.MutableMapping.update
        setdefault   = collections.MutableMapping.setdefault

        # Methods for polymorphism with `builtins.dict`:
        def copy(self):
            return self.__copy__()

        def iter(self):
            return iter(self.__iter__())

        # Standard operations:
        def __eq__(self, other):
            """Compare values using case insensitive keys."""
            if type(other) is type(self):
                pass
            elif isinstance(other, type(self)):
                return other == self
            elif isinstance(other, collections.MutableMapping):
                if not hasattr(other, 'lower_items'):
                    global Dicti
                    other = Dicti(other)
            else:
                return NotImplemented
            # TODO: implement this with less copying
            # NOTE: this discards comparison semantics defined in dict_ for
            # the sake of reflexitivity:
            return dict(self.lower_items()) == dict(other.lower_items())

        def __copy__(self):
            """Create a copy of the dictionary."""
            return self.__class__(self.values())

        def __repr__(self):
            """Representation string. Usually `dicti` or `Dicti(type)`."""
            return '%s(%r)' % (self.__class__.__name__, dict_(self.items()))

        def __str__(self):
            """Display string - like the underlying dictionary."""
            return '%r' % dict_(self.items())

        # extra methods:
        def lower_items(self):
            """Iterate over (key,value) pairs with lowercase keys."""
            return ((k, self[k]) for k in dict_.__iter__(self))

    return Dicti


_built_dicties = {}
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
        _built_dicties[base] = _make_dicti(base)
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

