#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests the rendering feature """

from redbaron import RedBaron


test_indent_code = """
def a():
    # plop
    1 + 2
    if caramba:
        plop
    pouf

"""


def test_increase_indentation():
    red = RedBaron(test_indent_code)
    red.increase_indentation(4)
    indented_code = "\n" + "\n".join(map(lambda x: "    " + x, test_indent_code.split("\n")[1:-2])) + "\n\n"
    assert red.dumps() == indented_code


def test_decrease_indentation():
    red = RedBaron(test_indent_code)
    red.decrease_indentation(4)
    indented_code = "\ndef a():\n" + "\n".join(map(lambda x: x[4:], test_indent_code.split("\n")[2:-2])) + "\n\n"
    assert red.dumps() == indented_code


def test_increase_indentation_single_node():
    red = RedBaron(test_indent_code)
    red.if_.value[0].increase_indentation(3)
    assert len(red.if_.value[0].indentation) == 8 + 3


def test_decrease_indentation_single_node():
    red = RedBaron(test_indent_code)
    red.if_.value[0].decrease_indentation(3)
    assert len(red.if_.value[0].indentation) == 5
