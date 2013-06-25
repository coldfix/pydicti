
from collections import OrderedDict
from pydicti import *
import json

# Entries in a `dicti` can be accessed case invariantly:

keys = ['Hello', 'beautiful', 'world!']
values = [1, 2, 3]
z = list(zip(keys, values))
i = dicti(z)
assert "WorLD!" in i and "universe" not in i

# However, the in calls like `.keys()` or `.items()` the keys are returned
# as in their original case:

assert "Hello" in list(i.keys())

# `dicti` can be "derived" from  another custom dictionary extension using
# it as the underlying dictionary to gain additional properties like order
# preservation:

from collections import OrderedDict
odicti = build_dicti(OrderedDict)
oi = odicti(z)
assert list(oi.keys()) == keys


# The equality  comparison preserves  the semantics of  the base  type and
# reflexitivity as best  as possible. This has impact  on the transitivity
# of the comparison operator:

rz = list(zip(reversed(keys), reversed(values)))
roi = odicti(rz)
assert roi == i and i == oi
assert oi != roi and roi != oi  # NOT transitive!
assert oi == i and i == oi      # reflexive

# Be careful with reflexitivity when comparing non-`dicti` types:

o = OrderedDict(oi)
oli = Dicti(oi.lower_dict())
assert oli == o
print(o == oli)
print(o.__eq__(oli))

# Note that `dicti` is the type corresponding to `builtins.dict`:

assert build_dicti(dict) is dicti

# The  method   `Dicti`  is  convenient  for   creating  case  insensitive
# dictionaries from a given object automatically using the objects type as
# the underlying dictionary type.

assert oi == Dicti(o)
assert type(oi) is type(Dicti(o))

# The subclassing approach works well with "badly" written code as in `json`
# that checks for `isinstance(dict)`:

import json
assert oi == json.loads(json.dumps(oi), object_pairs_hook=odicti)
