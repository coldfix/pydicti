CHANGELOG
~~~~~~~~~

1.1.6
=====
Date: 04.11.2021

- update the badges on the landing page


1.1.5
=====
Date: 04.11.2021

- maintenance release for testing automatic releases using GitHub Actions


1.1.4
=====
Date: 17.10.2020

- use ``str.casefold()`` on python3
- make normalization function a parameter of ``build_dict``, so that
  user-defined normalization functions can be passed


1.1.3
=====
Date: 28.06.2019

- avoid key recomputation in ``__setitem__``


1.1.2
=====
Date: 28.06.2019

- leave item order invariant under assignment in odicti (#2)
- leave key case invariant under assignment


1.1.1
=====
Date: 25.03.2019

- fix deprecated MutableMapping import (error on py38)


1.1.0
=====
Date: 19.03.2019

- drop py2.6 support
- fix version number in long_description


1.0.0
=====
Date: 19.03.2019

- make str representation more dict-like
- misc cleanup


0.0.6
=====
Date: 08.09.2016

- fix UnicodeDecodeError in setup when UTF-8 is not the default encoding


0.0.5
=====
Date: 18.05.2016

- fix pickling on py 3.5
- the 'name' parameter to build_dicti can now be a qualname


0.0.4
=====
Date: 01.02.2014

- add coverage reports
- use more extensive unit tests
- add support for pickle


0.0.3
=====
Date: 26.01.2014

- add support for python26
- make dependency on ``OrderedDict`` optional
- migrate to setuptools in order to use testing commands
- support `ordereddict.OrderedDict`_ as fallback

.. _`ordereddict.OrderedDict`: https://pypi.python.org/pypi/ordereddict/1.1

0.0.2
=====
Date: 29.12.2013

- fix ``dicti.pop``
- support ``deepcopy(dicti)``
- make nosetest automatically execute the doctests

