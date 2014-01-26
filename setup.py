#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup

tests_require = ['nose']
# Care for testing on python26:
try:
    from collections import OrderedDict
except ImportError:
    tests_require.append('ordereddict')

# see: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='pydicti',
    version='0.0.2',
    description='Case insensitive derivable dictionary',
    long_description=open('README.rst').read(),
    author='Thomas Gläßle',
    author_email='t_glaessle@gmx.de',
    url='https://github.com/coldfix/pydicti',
    license='Public Domain',
    py_modules=['pydicti'],
    tests_require=tests_require,
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)

