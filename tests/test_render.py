#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests the rendering feature """

from redbaron import RedBaron


def test_rendering_iter():
    red = RedBaron("a + 2")
    assert list(red._generate_nodes_in_rendering_order()) == [red[0], red.name, red[0].first_formatting[0], red[0], red[0].second_formatting[0], red.int]
    assert list(red[0]._generate_nodes_in_rendering_order()) == [red[0], red.name, red[0].first_formatting[0], red[0], red[0].second_formatting[0], red.int]


def test_next_rendered():
    red = RedBaron("a + 2")
    f = red.name

    assert f.next_rendered is red[0].first_formatting[0]
    assert f.next_rendered.next_rendered is red[0]
    assert f.next_rendered.next_rendered.next_rendered is red[0].second_formatting[0]
    assert f.next_rendered.next_rendered.next_rendered.next_rendered is red.int


def test_previous_rendered():
    red = RedBaron("a + 2")
    f = red.int

    assert f.previous_rendered is red[0].second_formatting[0]
    assert f.previous_rendered.previous_rendered is red[0]
    assert red[0].first_formatting[0].previous_rendered is red.name


test_indent_code = """
def a():
    # plop
    1 + 2
    if caramba:
        plop
    pouf

"""

def test_next_rendered_trapped():
    red = RedBaron(test_indent_code)
    assert red("endl")[5].next_rendered is red.find("name", "pouf")

