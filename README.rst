pydicti
-------
|Build Status| |Coverage| |Version| |Downloads| |License|

Installation
~~~~~~~~~~~~

You can install the newest version of *pydicti* from PyPI_:

.. code:: bash

    pip install pydicti

Alternatively, you can just take the file ``pydicti.py`` and redistribute
it with your application.

.. _PyPI: https://pypi.python.org/pypi/pydicti/


Overview
~~~~~~~~

- ``class dicti``: default case insensitive dictionary type
- ``class odicti``: ordered case insensitive dictionary type
- ``def build_dicti``: create a case insensitive dictionary class
- ``def Dicti``: create a case insensitive copy of a dictionary

dicti
=====

Objects of type ``dicti`` are dictionaries that feature case insensitive
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
    Dicti(OrderedDict([('a', 0), ('b', 1), ('c', 2)]))

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


.. |Downloads| image:: http://coldfix.de:8080/d/pydicti/badge.svg
   :target: https://pypi.python.org/pypi/pydicti/
   :alt: Downloads

.. |Version| image:: http://coldfix.de:8080/v/pydicti/badge.svg
   :target: https://pypi.python.org/pypi/pydicti/
   :alt: Latest Version

.. |Build Status| image:: https://api.travis-ci.org/coldfix/pydicti.svg?branch=master
   :target: https://travis-ci.org/coldfix/pydicti
   :alt: Build Status

.. |Coverage| image:: https://coveralls.io/repos/coldfix/pydicti/badge.svg?branch=master
   :target: https://coveralls.io/r/coldfix/pydicti
   :alt: Coverage

.. |License| image:: http://coldfix.de:8080/license/pydicti/badge.svg
   :target: https://github.com/coldfix/pydicti/blob/master/COPYING
   :alt: License
