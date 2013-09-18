#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

# read long_description from README.rst
try:
    f = open('README.rst')
    long_description = f.read()
    f.close()
except:
    long_description = None

# invoke distutils
setup(
    name='pydicti',
    version='0.0.1',
    description='Case insensitive derivable dictionary',
    long_description=long_description,
    author='Thomas Gläßle',
    author_email='t_glaessle@gmx.de',
    url='https://github.com/coldfix/pydicti',
    license='Public Domain',
    py_modules=[
        'pydicti',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)

