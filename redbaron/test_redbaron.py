#!/usr/bin/python
# -*- coding:Utf-8 -*-


from redbaron import RedBaron


def test_empty():
    RedBaron("")


def test_is_list():
    assert [] == list(RedBaron(""))
