#!/usr/bin/python
# -*- coding:Utf-8 -*-


from redbaron import RedBaron
from redbaron.nodes import NameNode, EndlNode


def test_empty():
    RedBaron("")


def test_is_list():
    assert [] == list(RedBaron(""))


def test_name():
    red = RedBaron("a\n")
    assert len(red) == 2
    assert isinstance(red[0], NameNode)
    assert isinstance(red[1], EndlNode)
    assert red[0].value == "a"
