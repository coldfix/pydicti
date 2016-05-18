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

# Care for testing on python26:
extras_require = {}
try:
    from collections import OrderedDict
except ImportError:
    extras_require['odicti'] = ['ordereddict']
else:
    extras_require['odicti'] = []

setup(
    name='pydicti',
    version='0.0.5',
    description='Case insensitive derivable dictionary',
    long_description=long_description,
    author='Thomas Gläßle',
    author_email='t_glaessle@gmx.de',
    url='https://github.com/coldfix/pydicti',
    license='WTFPL',
    py_modules=['pydicti'],
    extras_require=extras_require,
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development',
    ],
)

