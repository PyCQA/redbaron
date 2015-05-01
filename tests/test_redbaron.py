#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Main redbaron test module """

from redbaron import RedBaron, truncate


def test_other_name_assignment():
    red = RedBaron("a = b")
    assert red.assign is red[0]


def test_index():
    red = RedBaron("a = [1, 2, 3]")
    assert red[0].value.value[2].index_on_parent == 2
    assert red[0].index_on_parent == 0
    assert red[0].value.index_on_parent is None


def test_index_raw():
    red = RedBaron("a = [1, 2, 3]")
    assert red[0].value.value.node_list[2].index_on_parent_raw == 2
    assert red[0].index_on_parent == 0
    assert red[0].value.index_on_parent_raw is None


def test_regression_find_all_recursive():
    red = RedBaron("a.b()")
    assert red[0].value("name", recursive=False) == [red.name, red("name")[1]]


def test_truncate():
    assert "1234" == truncate("1234", 2)
    assert "12345" == truncate("12345", 4)
    assert "1...6" == truncate("123456", 5)
    assert "123456...0" == truncate("12345678901234567890", 10)

