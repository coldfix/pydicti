from typing import Dict
from pydicti import build_dicti, dicti, odicti, Dicti
from collections import OrderedDict


class V:
    pass


v: V = V()
d: Dict[str, V] = {}
o: OrderedDict[str, V] = OrderedDict()


# ----------------------------------------
# dicti
# ----------------------------------------

_: Dict[str, V] = dicti()
_
_: Dict[str, V] = dicti(d)
_

# ----------------------------------------
# odicti
# ----------------------------------------

_: OrderedDict[str, V] = odicti()
_
_: OrderedDict[str, V] = odicti(o)
_


# ----------------------------------------
# Dicti
# ----------------------------------------

_: Dict[str, V] = Dicti(d)
_
_: OrderedDict[str, V] = Dicti(o)
_


# ----------------------------------------
# build_dicti
# ----------------------------------------

# dict
_: Dict[str, V]           = build_dicti(dict)()
_
_: Dict[str, V]           = build_dicti(dict)(d)
_

# OrderedDict
_: OrderedDict[str, V]    = build_dicti(OrderedDict)()
_
_: OrderedDict[str, V]    = build_dicti(OrderedDict)(o)
_
