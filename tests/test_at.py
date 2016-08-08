# -*- coding:Utf-8 -*-

"""Test for at method"""

import pytest
import redbaron
from redbaron import RedBaron

redbaron.DEBUG = True

fst_def = RedBaron("""\
@deco

def foo(a, b):
    c = a + b
    e = 1
""")


def test_at_def():
    assert fst_def.at(1) is fst_def.find('DecoratorNode')
    assert fst_def.at(2) is fst_def
    assert fst_def.at(3) is fst_def.def_
    assert fst_def.at(4) is fst_def.find('NameNode', value='c')
    assert fst_def.at(5) is fst_def.find('NameNode', value='e')


fst_class = RedBaron("""\
class Foo(object):
    def __init__(self):
        self.a = None
    def bar(self):
        return self.a + 5
""")


def test_at_class():
    assert fst_class.at(1) is fst_class.class_
    assert fst_class.at(2) is fst_class.find_all('DefNode')[0]
    assert fst_class.at(3) is fst_class.find('AtomtrailersNode')
    assert fst_class.at(4) is fst_class.find_all('DefNode')[1]
    assert fst_class.at(5) is fst_class.find('ReturnNode')


fst_simple = RedBaron("""\
a = 5

b = 6
""")


def test_at_simple():
    assert fst_simple.at(1) is fst_simple.find_all('NameNode')[0]
    assert fst_simple.at(2) is fst_simple
    assert fst_simple.at(3) is fst_simple.find_all('NameNode')[1]
