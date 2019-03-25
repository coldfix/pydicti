CHANGELOG
~~~~~~~~~

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

