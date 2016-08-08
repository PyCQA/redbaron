# -*- coding:Utf-8 -*-

"""Test for at method"""

import pytest
import redbaron
from redbaron import RedBaron

redbaron.DEBUG = True

red = RedBaron("""\
class Foo(object):
    def __init__(self):
        self.a = None
    def bar(self):
        for x in range(5):
            yield self.a + x
""")


def test_at():
    assert red.at(1) is red.class_
    assert red.at(2) is red.find_all('DefNode')[0]
    assert red.at(3) is red.find('AtomtrailersNode')
    assert red.at(4) is red.find_all('DefNode')[1]
    assert red.at(5) is red.find('ForNode')
    assert red.at(6) is red.find('YieldNode')
