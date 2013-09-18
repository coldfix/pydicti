# encoding: utf-8
"""
Case insensitive derivable dictionary.


### License

Copyright © 2013 Thomas Gläßle <t_glaessle@gmx.de>

This work  is free. You can  redistribute it and/or modify  it under the
terms of the Do What The Fuck  You Want To Public License, Version 2, as
published by Sam Hocevar. See the COPYING file for more details.

This program  is free software.  It comes  without any warranty,  to the
extent permitted by applicable law.


### Global namespace

 - `def build_diciti(base)`: derive case insensitive dictionary class
 - `def Dicti(obj)`: create ci-dict instance using obj's class as base
 - `class dicti = build_dicti(dict)` standard ci-dict
 - `class odicti = build_odicti(OrderedDict)` ordered ci-dict


### Overview

Entries in a `dicti` can be accessed case invariantly:

>>> keys = ['Hello', 'beautiful', 'world!']
>>> values = [1, 2, 3]
>>> z = list(zip(keys, values))
>>> i = dicti(z)
>>> assert "WorLD!" in i and "universe" not in i
>>> assert i.get('hEllo') == 1

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

Be careful  with reflexitivity when  comparing to non-`dicti`  types and
even more so if both operands are  not subclasses of each other. Here it
is important  to know about  coercion rules.  `o == oli`  actually calls
`oli.__eq__(o)` if `oli` is of a subclass of the type of of `o`. See:

http://docs.python.org/2/reference/datamodel.html#coercion-rules 

>>> o = OrderedDict(oi)
>>> oli = Dicti(oi.lower_dict())
>>> assert oli == o and o == oli    # reflexive (coercion rules)
>>> print(o.__eq__(oli))            # dependends on OrderedDict.__eq__
False

Note that `dicti` is the type corresponding to `builtins.dict`:

>>> assert build_dicti(dict) is dicti

The  method   `Dicti`  is  convenient  for   creating  case  insensitive
dictionaries from a given object automatically using the objects type as
the underlying dictionary type.

>>> assert oi == Dicti(o)
>>> assert type(oi) is type(Dicti(o))

The  subclassing approach  works well  with "badly"  written code  as in
`json` that checks for `isinstance(dict)`:

>>> import json
>>> assert oi == json.loads(json.dumps(oi), object_pairs_hook=odicti)

"""
__all__ = ['build_dicti', 'Dicti', 'odicti', 'dicti']

import collections

# internally used to allow keys that are not strings
def _lower(s):
    """Convert to lower case if possible."""
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
            dict_.__init__(self)
            self.__case = {}
            self.update(*args, **kwargs)

        # MutableMapping methods:
        def __getitem__(self, key):
            """Get the value for `key` case insensitively."""
            return dict_.__getitem__(self, self.__case[_lower(key)])

        def __setitem__(self, key, value):
            """Set the value for `key` and assume new case."""
            lower = _lower(key)
            if lower in self.__case:
                dict_.__delitem__(self, self.__case[lower])
            dict_.__setitem__(self, key, value)
            self.__case[lower] = key

        def __delitem__(self, key):
            """Delete the item for `key` case insensitively."""
            lower = _lower(key)
            dict_.__delitem__(self, self.__case[lower])
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
            elif isinstance(other, collections.MutableMapping):
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

        def __repr__(self):
            """Representation string. Usually `dicti` or `Dicti(type)`."""
            return '%s(%r)' % (self.__class__.__name__, dict_(self.items()))

        def __str__(self):
            """Display string - like the underlying dictionary."""
            return '%r' % dict_(self.items())

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


# Execute the doctests if run from the command line.
# Verbose tests: python __init__.py -v
if __name__ == "__main__":
    import doctest
    doctest.testmod()

