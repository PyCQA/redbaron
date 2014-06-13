#!/usr/bin/python
# -*- coding:Utf-8 -*-

from setuptools import setup

setup(name='redbaron',
      version='0.1',
      description='Abstraction on top of baron, a FST for python to make writing refactoring code a realistic task',
      author='Laurent Peuch',
      long_description=open("README.md", "r").read(),
      author_email='cortex@worlddomination.be',
      url='https://github.com/Psycojoker/redbaron',
      install_requires=['baron>=0.2', 'pygments'],
      license= 'lgplv3+',
      py_modules=["redbaron"],
      keywords='baron fst ast refactoring',
     )
