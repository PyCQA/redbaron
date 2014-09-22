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
      install_requires=['baron>=0.3.1', 'pygments'],
      license= 'lgplv3+',
      py_modules=["redbaron"],
      keywords='baron fst ast refactoring',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                   'Topic :: Software Development',
                   'Topic :: Software Development :: Code Generators',
                   'Topic :: Software Development :: Libraries',
                   ],
     )
