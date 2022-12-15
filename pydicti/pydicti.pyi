from typing import (
    TypeVar, Type, Callable, Optional,
    Mapping, Dict, OrderedDict
)


DictObj = TypeVar('DictObj', bound=Mapping)
DictType = TypeVar('DictType', bound=Type[Mapping])
KeyTransform = Callable[[str], str]


# Public:

__version__: str
dicti: Type[Dict]
odicti: Type[OrderedDict]


def build_dicti(
    base: DictType,
    name: Optional[str] = ...,
    module: Optional[str] = ...,
    normalize: KeyTransform = ...,
) -> DictType:
    ...


def Dicti(obj: DictObj) -> DictObj:
    ...


# Internal:

def normalize_case(s: str) -> str:
    ...


def _make_dicti(
    dict_: DictType,
    normalize: KeyTransform = ...
) -> DictType:
    ...
