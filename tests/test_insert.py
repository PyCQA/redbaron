#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests the code insertion features """

import pytest
# pylint: disable=redefined-outer-name
from redbaron import RedBaron


@pytest.fixture
def red():
    return RedBaron("""\
class A:
    pass

class B:
    pass
""")


def test_insert_with_class_0(red):
    red.insert(0, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
a = 1
class A:
    pass

class B:
    pass
"""


def test_insert_with_class_1(red):
    red.insert(1, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
class A:
    pass
a = 1

class B:
    pass
"""


def test_insert_with_class_2(red):
    red.insert(2, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
class A:
    pass

a = 1
class B:
    pass
"""


def test_insert_with_class_3(red):
    red.insert(3, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
class A:
    pass

class B:
    pass
a = 1
"""


def test_insert_with_class_after(red):
    red.insert(4, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
class A:
    pass

class B:
    pass
a = 1
"""


def test_insert_with_class_neg_1(red):
    red.insert(-1, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
class A:
    pass

class B:
    pass
a = 1
"""


def test_insert_with_class_neg_2(red):
    red.insert(-2, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
class A:
    pass

a = 1
class B:
    pass
"""


def test_insert_with_class_neg_3(red):
    red.insert(-3, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
class A:
    pass
a = 1

class B:
    pass
"""


def test_insert_with_class_neg_4(red):
    red.insert(-4, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
a = 1
class A:
    pass

class B:
    pass
"""


def test_insert_with_class_neg_before(red):
    red.insert(-5, "a = 1")

    print(red.dumps())
    assert red.dumps() == """\
a = 1
class A:
    pass

class B:
    pass
"""

