# encoding: utf-8
"""
Case insensitive derivable dictionary.


Installation
~~~~~~~~~~~~

You can install the newest version of *pydicti* from PyPI:

.. code:: bash

    pip install pydicti

Alternatively, you can just take the file ``pydicti.py`` and redistribute
it with your application.


Overview
~~~~~~~~

- ``class dicti``: default case insensitive dictionary type
- ``class odicti``: ordered case insensitive dictionary type
- ``def build_dicti``: create a case insensitive dictionary class
- ``def Dicti``: create a case insensitive copy of a dictionary

dicti
=====

Object of type ``dicti`` are dictionaries that feature case insensitive
item access:

.. code:: python

    >>> d = dicti(Hello='foo', world='bar')
    >>> d['heLLO']
    'foo'
    >>> 'WOrld' in d
    True

Internally however, the keys retain their original case:

.. code:: python

    >>> sorted(d.keys())
    ['Hello', 'world']

odicti
======

The type ``odicti`` instanciates order-preserving case insensitive
dictionaries. It is available if either `collections.OrderedDict`_ or
`ordereddict.OrderedDict`_ exists:

.. code:: python

    >>> odicti(zip('abc', range(3)))
    odicti([('a', 0), ('b', 1), ('c', 2)])

.. _`collections.OrderedDict`: http://docs.python.org/3.3/library/collections.html#collections.OrderedDict
.. _`ordereddict.OrderedDict`: https://pypi.python.org/pypi/ordereddict/1.1

build_dicti
===========

With ``build_dicti`` you can create custom case insensitive dictionaries.
This function is what is used to create the ``pydicti.dicti`` and
``pydicti.odicti`` types. Note that calling ``build_dicti`` several times
with the same argument will result in identical types:

.. code:: python

    >>> build_dicti(dict) is dicti
    True
    >>> build_dicti(OrderedDict) is odicti
    True

``build_dicti`` uses subclassing to inherit the semantics of the given base
dictionary type:

.. code:: python

    >>> issubclass(odicti, OrderedDict)
    True

Dicti
=====

The function ``Dicti`` is convenient for creating case insensitive
copies of dictionary instances:

.. code:: python

    >>> o = OrderedDict(zip('abcdefg', range(7)))
    >>> oi = Dicti(o)
    >>> type(oi) is odicti
    True


JSON
~~~~

The subclassing approach allows to plug your dictionary instance into
places where typechecking with ``isinstance`` is used, like in the json_
module:

.. code:: python

    >>> import json
    >>> d == json.loads(json.dumps(d), object_hook=dicti)
    True

.. _json: http://docs.python.org/3.3/library/json.html

Above python26 you can use ``json.loads(s, object_pairs_hook=odicti)`` to
deserialize ordered dictionaries.


Pitfalls
~~~~~~~~

The equality comparison tries preserves the semantics of the base type as
well as reflexitivity. This has impact on the transitivity of the
comparison operator:

.. code:: python

    >>> i = dicti(oi)
    >>> roi = odicti(reversed(list(oi.items())))
    >>> roi == i and i == oi
    True
    >>> oi != roi and roi != oi  # NOT transitive!
    True
    >>> oi == i and i == oi      # reflexive
    True

The `coercion rules`_ in python allow this to work pretty well when
performing comparisons between types that are subclasses of each other. Be
careful otherwise, however.

.. _`coercion rules`: http://docs.python.org/2/reference/datamodel.html#coercion-rules


License
~~~~~~~

Copyright © 2013 Thomas Gläßle <t_glaessle@gmx.de>

This work  is free. You can  redistribute it and/or modify  it under the
terms of the Do What The Fuck  You Want To Public License, Version 2, as
published by Sam Hocevar. See the COPYING file for more details.

This program  is free software.  It comes  without any warranty,  to the
extent permitted by applicable law.

"""
__all__ = ['build_dicti', 'Dicti', 'odicti', 'dicti']

import sys as _sys
from collections import MutableMapping as _MutableMapping
from copy import deepcopy as _deepcopy

try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        pass

# internally used to allow keys that are not strings
def _lower(s):
    """Convert to lower case if possible."""
    try:
        return s.lower()
    except AttributeError:
        return s

# make class
def _make_dicti(dict_):
    _marker = []
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

        Note  that `dicti`  is  inherited  from `builtins.dict`  instead
        of   from   `collections.MutableMapping`.    This   means   that
        `isinstance(d,dict)` checks will  succeed and `json.dump()` will
        work automatically with `dicti`.


        Implementation rationale (known pitfalls):

        When subclassing `builtins.dict`,  calling `dict(Dicti(v))` will
        bypass  the `__iter__`+`__getitem__`  interface  and access  the
        'internal' (inherited) dictionary. See:

        http://stackoverflow.com/questions/18317905/overloaded-iter-is-bypassed-when-deriving-from-dict

        When subclassing  `dict`, it is  therefore necessary to  set the
        internal dictionary such  that it can be  converted back without
        problem. This easiest  way to do this is a  two step key lookup.
        The  internal dictionary  stores  (original_case  => value)  and
        another is used to store (lower_case => original_case).

        """

        # Constructor:
        def __init__(self, *args, **kwargs):
            """Initialize a case insensitive dictionary from the arguments."""
            self.__case = {}        # create this member ASAP since
                                    # dict_.__init__() might call self.clear()
            dict_.__init__(self)
            self.update(*args, **kwargs)

        # MutableMapping methods:
        def __getitem__(self, key):
            """Get the value for `key` case insensitively."""
            return dict_.__getitem__(self, self.__case[_lower(key)])

        def __setitem__(self, key, value):
            """Set the value for `key` and assume new case."""
            # NOTE: this must be executed BEFORE dict_.__setitem__ in order
            # to leave a consistent state for base method:
            if key in self:
                del self[key]
            dict_.__setitem__(self, key, value)
            self.__case[_lower(key)] = key

        def __delitem__(self, key):
            """Delete the item for `key` case insensitively."""
            lower = _lower(key)
            dict_.__delitem__(self, self.__case[lower])
            # NOTE: this must be executed AFTER dict_.__delitem__ in order
            # to leave a consistent state for base method:
            del self.__case[lower]

        def __contains__(self, key):
            """Check if key is contained."""
            return _lower(key) in self.__case

        # Implemented by `dict_`
        # __iter__  # iterate in original case
        # __len__
        # keys
        # values
        # items / iteritems

        # Implemented by `MutableMapping`:
        get          = _MutableMapping.get
        popitem      = _MutableMapping.popitem
        update       = _MutableMapping.update
        setdefault   = _MutableMapping.setdefault

        def clear(self):
            """Remove all entries from the dictionary."""
            dict_.clear(self)
            # NOTE: this must be executed AFTER dict_.clear in order to
            # leave a consistent state for base method:
            self.__case.clear()

        def pop(self, key, default=_marker):
            """
            Remove specified key and return the corresponding value.

            If the default parameter is given, it will be returned in case
            the key is not in the dictionary. Otherwise, a KeyError will be
            raised.

            """
            if key in self:
                result = self[key]
                del self[key]
                return result
            if default is _marker:
                raise KeyError(key)
            return default

        # Methods for polymorphism with `builtins.dict`:
        def copy(self):
            """Create a copy of the dictionary."""
            return self.__copy__()

        def iter(self):
            """Return iterator over all keys in their original case."""
            return iter(self.__iter__())

        # Standard operations:
        def __eq__(self, other):
            """Compare values using case insensitive keys."""
            if type(other) is type(self):
                pass
            elif isinstance(other, _MutableMapping):
                if not hasattr(other, 'lower_dict'):
                    global Dicti
                    other = Dicti(other)
            else:
                return NotImplemented
            # TODO: implement this with less copying
            return self.lower_dict() == other.lower_dict()

        def __copy__(self):
            """Create a copy of the dictionary."""
            return self.__class__(self)

        def __deepcopy__(self, memo):
            """Create a deep copy of the dictionary."""
            copy = self.__class__()
            for k,v in self.items():
                copy[k] = _deepcopy(v, memo)
            return copy

        def __repr__(self):
            """Representation string - something like `dicti([<items>])`."""
            return '%s(%r)' % (self.__class__.__name__, list(self.items()))

        def __str__(self):
            """Display string - like the underlying dictionary."""
            return '%r' % dict_(self.items())

        # For now, let's assume that default pickling works fine for most
        # base classes. However, on python3 dict needs special treatment.
        # Its special pickling handler causes __setitem__ to be called on
        # unpickling before __case is restored or __setstate__ is called.
        # With the help of the __reduce__ method, this behaviour can be
        # overwritten.
        if dict_ is dict:
            def __reduce__(self):
                return Dicti, (), self.__getstate__()
            def __getstate__(self):
                return dict_(self)
            def __setstate__(self, state):
                self.__case = {}
                self.update(state.items())

        # extra methods:
        def lower_items(self):
            """Iterate over (key,value) pairs with lowercase keys."""
            return ((_lower(k), v) for k,v in self.items())

        def lower_dict(self):
            """Return an underlying dictionary type with lowercase keys."""
            # TODO: implement this as a view?
            return dict_(self.lower_items())

    return Dicti


_built_dicties = {}
def build_dicti(base, name=None, module=None):
    """
    Create a case insenstive subclass of `base`.

    :param MutableMapping base: base class
    :param str name: subclass name (defaults to base.__name__+'i')
    :param str module: module name for subclass (defaults to calling module)

    If  the class has already been created, this will not create a new type,
    but rather lookup the existing type in a table. The parameters `name`
    and `module` will not be used in this case.

    """
    try:
        cls = _built_dicties[base]
    except KeyError:
        if not issubclass(base, _MutableMapping):
            raise TypeError("Not a mapping type: %s" % base)
        cls = _make_dicti(base)
        name = name or base.__name__ + 'i'
        cls.__name__ = name.rsplit('.', 1)[-1]
        cls.__module__ = module or _sys._getframe(1).f_globals.get('__name__', '__main__')
        cls.__qualname__ = name
        _built_dicties[base] = cls
    return cls

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
try:
    OrderedDict
except NameError:
    pass
else:
    odicti = build_dicti(OrderedDict, 'odicti')

