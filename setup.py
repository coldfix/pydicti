# encoding: utf-8
from setuptools import setup

# see: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing
except ImportError:
    pass

# prepare long_description for PyPI:
long_description = None
try:
    long_description = open('README.rst').read()
    long_description += '\n' + open('CHANGES.rst').read()
except IOError:
    pass

tests_require = ['nose']
extras_require = {}
# Care for testing on python26:
try:
    from collections import OrderedDict
except ImportError:
    tests_require.append('ordereddict')
    extras_require['odicti'] = ['ordereddict']
else:
    extras_require['odicti'] = []

setup(
    name='pydicti',
    version='0.0.3',
    description='Case insensitive derivable dictionary',
    long_description=long_description,
    author='Thomas Gläßle',
    author_email='t_glaessle@gmx.de',
    url='https://github.com/coldfix/pydicti',
    license='Public Domain',
    py_modules=['pydicti'],
    extras_require=extras_require,
    tests_require=tests_require,
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)

