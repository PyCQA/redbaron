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
    assert fst_def.at(4) is fst_def.find_all('AssignmentNode')[0]
    assert fst_def.at(5) is fst_def.find_all('AssignmentNode')[1]


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
    assert fst_class.at(3) is fst_class.find('AssignmentNode')
    assert fst_class.at(4) is fst_class.find_all('DefNode')[1]
    assert fst_class.at(5) is fst_class.find('ReturnNode')
