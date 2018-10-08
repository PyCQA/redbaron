#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests the root method """

import pytest
# pylint: disable=redefined-outer-name
from redbaron import RedBaron


@pytest.fixture
def red():
    return RedBaron("""\
@deco
def a(c, d):
    b = c + d
""")


def test_root(red):
    nodes = [
        red.def_,
        red.def_.decorators,
        red.def_.decorators.node_list[0],
        red.def_.decorators.node_list[0].value,
        red.def_.decorators.node_list[0].value.value,
        red.def_.decorators.node_list[0].value.value[0],
        red.def_.decorators.node_list[1],
        red.def_.first_formatting,
        red.def_.first_formatting[0],
        red.def_.second_formatting,
        red.def_.third_formatting,
        red.def_.arguments,
        red.def_.arguments.node_list[0],
        red.def_.arguments.node_list[1],
        red.def_.arguments.node_list[2],
        red.def_.fourth_formatting,
        red.def_.fifth_formatting,
        red.def_.sixth_formatting,
        red.def_.value.node_list,
        red.def_.value.node_list[0],
        red.def_.value.node_list[1],
        red.def_.value.node_list[1].target,
        red.def_.value.node_list[1].value,
        red.def_.value.node_list[1].value.first,
        red.def_.value.node_list[1].value.second,
        red.def_.value.node_list[2]
    ]

    for node in nodes:
        assert red is node.root


def test_get_root():
    red = RedBaron("def a(b=c):\n    return 42")
    assert red is red.find("int").root
