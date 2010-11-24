#!/usr/bin/env python
# encoding: utf-8
"""
setup.py
"""

from setuptools import setup, find_packages
import os

execfile(os.path.join('src', 'nprslurp', 'version.py'))

setup(
    name = 'nprslurp',
    version = VERSION,
    description = 'nprslurp downloads npr shows.',
    author = 'Kurtiss Hare',
    author_email = 'kurtiss@gmail.com',
    url = 'http://www.github.com/kurtiss/nprslurp',
    packages = find_packages('src'),
    package_dir = {'':'src'},
    scripts = ['bin/nprslurp'],
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe = False
)
