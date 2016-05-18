CHANGELOG
~~~~~~~~~

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

