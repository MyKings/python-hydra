#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from hydra import version
from hydra import author

setup(
    name='python-hydra',
    version=version,
    author=author,
    author_email='xsseroot@gmail.com',
    license='LICENSE',
    keywords="hydra, python-hydra",
    packages=['python-hydra'],
    url='https://github.com/MyKings/python-hydra',
    bugtrack_url='https://github.com/MyKings/python-hydra/issues',
)
