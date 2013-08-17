## pydicti

Case insensitive derivable dictionary.

- [License](#license)
- [Global namespace](#global-namespace)
- [Overview](#overview)


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

```python
keys = ['Hello', 'beautiful', 'world!']
values = [1, 2, 3]
z = list(zip(keys, values))
i = dicti(z)
assert "WorLD!" in i and "universe" not in i
assert i.get('hEllo') == 1
```

However, the in calls like `.keys()` or `.items()` the keys are returned
as in their original case:

```python
assert "Hello" in list(i.keys())
```

`dicti` can be "derived" from  another custom dictionary extension using
it as the underlying dictionary to gain additional properties like order
preservation:

```python
from collections import OrderedDict
odicti = build_dicti(OrderedDict)
oi = odicti(z)
assert list(oi.keys()) == keys
```

The equality  comparison preserves  the semantics of  the base  type and
reflexitivity as best  as possible. This has impact  on the transitivity
of the comparison operator:

```python
rz = list(zip(reversed(keys), reversed(values)))
roi = odicti(rz)
assert roi == i and i == oi
assert oi != roi and roi != oi  # NOT transitive!
assert oi == i and i == oi      # reflexive
```

Be careful  with reflexitivity when  comparing to non-`dicti`  types and
even more so if both operands are  not subclasses of each other. Here it
is important  to know about  coercion rules.  `o == oli`  actually calls
`oli.__eq__(o)` if `oli` is of a subclass of the type of of `o`. See:

http://docs.python.org/2/reference/datamodel.html#coercion-rules

```python
>>> o = OrderedDict(oi)
>>> oli = Dicti(oi.lower_dict())
>>> assert oli == o and o == oli    # reflexive (coercion rules)
>>> print(o.__eq__(oli))            # dependends on OrderedDict.__eq__
False
```

Note that `dicti` is the type corresponding to `builtins.dict`:

```python
assert build_dicti(dict) is dicti
```

The  method   `Dicti`  is  convenient  for   creating  case  insensitive
dictionaries from a given object automatically using the objects type as
the underlying dictionary type.

```python
assert oi == Dicti(o)
assert type(oi) is type(Dicti(o))
```

The  subclassing approach  works well  with "badly"  written code  as in
`json` that checks for `isinstance(dict)`:

```python
import json
assert oi == json.loads(json.dumps(oi), object_pairs_hook=odicti)
```
