# -*- coding:Utf-8 -*-

"""Test for at method"""

import pytest
import redbaron
from redbaron import RedBaron, DecoratorNode, AssignmentNode, DefNode, EndlNode

redbaron.DEBUG = True

fst = RedBaron("""\
@deco

def foo(a, b):
    c = a + b
    e = 1
""")


def test_at():
    assert isinstance(fst.at(1), DecoratorNode) is True
    assert isinstance(fst.at(2), RedBaron) is True
    assert isinstance(fst.at(3), DefNode) is True
    assert isinstance(fst.at(4), AssignmentNode) is True
    assert isinstance(fst.at(5), AssignmentNode) is True
