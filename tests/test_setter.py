#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests the setter methods """

import pytest
# pylint: disable=redefined-outer-name
from redbaron import RedBaron
from baron.utils import string_instance


def test_setitem_nodelist():
    red = RedBaron("[1, 2, 3]")
    red[0].value.node_list[2] = "2 + 'pouet'"
    red.dumps()
    assert red[0].value.node_list[2].type == "binary_operator"
    assert red[0].value.node_list[2].parent is red[0]
    assert red[0].value.node_list[2].on_attribute == "value"


def test_set_attr_on_import():
    red = RedBaron("import a")
    red[0].value = "a.b.c as d, qsd, plop as pouet"
    assert red.dumps() == "import a.b.c as d, qsd, plop as pouet"


def test_set_attr_on_list():
    red = RedBaron("[]")
    red[0].value = "1, 2, 3"
    assert red[0].value[0].type == "int"


def test_set_attr_on_list_empty():
    red = RedBaron("[1, 2, 3]")
    red[0].value = ""
    assert len(red[0].value) == 0


def test_set_attr_on_set():
    red = RedBaron("{1,}")
    red[0].value = "1, 2, 3"
    assert red[0].value[0].type == "int"


def test_set_attr_on_tuple():
    red = RedBaron("(1,)")
    red[0].value = "1, 2, 3"
    assert red[0].value[0].type == "int"


def test_set_attr_on_tuple_empty():
    red = RedBaron("(1,)")
    red[0].value = ""
    assert len(red[0].value) == 0


def test_set_attr_on_repr():
    red = RedBaron("`1`")
    red[0].value = "1, 2, 3"
    assert red[0].value[0].type == "int"


def test_set_attr_on_dict():
    red = RedBaron("{}")
    red[0].value = "1: 2, 3: 4"
    assert red[0].value[0].key.type == "int"


def test_set_attr_on_dict_empty():
    red = RedBaron("{1: 2, 3: 4}")
    red[0].value = ""
    assert len(red[0].value) == 0


def test_set_attr_def_name():
    red = RedBaron("def a(): pass")
    red[0].name = "plop"
    assert isinstance(red[0].name, string_instance)


def test_set_attr_def_arguments():
    red = RedBaron("def a(): pass")
    red[0].arguments = "x, y=z, *args, **kwargs"
    assert len(red[0].arguments.filtered()) == 4


def test_set_attr_def_value_simple():
    red = RedBaron("def a(): pass")
    red[0].value = "plop"
    assert red[0].value.dumps() == "\n    plop\n"


def test_set_attr_def_value_simple_indented():
    red = RedBaron("def a(): pass")
    red[0].value = "    plop"
    assert red[0].value.dumps() == "\n    plop\n"


def test_set_attr_def_value_simple_endl():
    red = RedBaron("def a(): pass")
    red[0].value = "\nplop"
    assert red[0].value.dumps() == "\n    plop\n"


def test_set_attr_def_value_simple_space_endl():
    red = RedBaron("def a(): pass")
    red[0].value = "  \nplop"
    assert red[0].value.dumps() == "\n    plop\n"


def test_set_attr_def_value_simple_space_endl_space():
    red = RedBaron("def a(): pass")
    red[0].value = "  \n   plop"
    assert red[0].value.dumps() == "\n    plop\n"


def test_set_attr_def_value_simple_too_much_space():
    red = RedBaron("def a(): pass")
    red[0].value = "                          plop"
    assert red[0].value.dumps() == "\n    plop\n"


def test_set_attr_def_value_simple_endl_too_much_space():
    red = RedBaron("def a(): pass")
    red[0].value = "\n                          plop"
    assert red[0].value.dumps() == "\n    plop\n"


def test_set_attr_def_value_simple_space_endl_too_much_space():
    red = RedBaron("def a(): pass")
    red[0].value = "  \n                        plop"
    assert red[0].value.dumps() == "\n    plop\n"


def test_set_attr_def_value_complex():
    red = RedBaron("def a(): pass")
    red[0].value = "plop\nplouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_value_endl_complex():
    red = RedBaron("def a(): pass")
    red[0].value = "\nplop\nplouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_value_indent_complex():
    red = RedBaron("def a(): pass")
    red[0].value = "    plop\n    plouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_value_endl_indent_complex():
    red = RedBaron("def a(): pass")
    red[0].value = "\n    plop\n    plouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_value_space_endl_indent_complex():
    red = RedBaron("def a(): pass")
    red[0].value = "    \n    plop\n    plouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_too_small_indent_complex():
    red = RedBaron("def a(): pass")
    red[0].value = " plop\n plouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_endl_too_small_indent_complex():
    red = RedBaron("def a(): pass")
    red[0].value = "\n plop\n plouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_space_endl_too_small_indent_complex():
    red = RedBaron("def a(): pass")
    red[0].value = " \n plop\n plouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_too_much_indent_complex():
    red = RedBaron("def a(): pass")
    red[0].value = "            plop\n            plouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_endl_too_much_indent_complex():
    red = RedBaron("def a(): pass")
    red[0].value = "\n            plop\n            plouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_space_endl_too_much_indent_complex():
    red = RedBaron("def a(): pass")
    red[0].value = "            \n            plop\n            plouf"
    assert red[0].value.dumps() == "\n    plop\n    plouf\n"


def test_set_attr_def_space_complex_with_more_complex_indent():
    red = RedBaron("def a(): pass")
    red[0].value = "plop\nif a:\n    pass\n"
    assert red[0].value.dumps() == "\n    plop\n    if a:\n        pass\n"


code_for_block_setattr = """
class A():
    def a():
        pass

    def b():
        pass


def c():
    def zomg():
        pass
    plop


def d():
    pass
"""


def test_set_attr_def_advanced_dont_break_next_block_indent():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="c").value = "return 42"
    assert len(red.find("def", name="c")("endl")) == 4
    assert red.find("def", name="c").value.node_list[-1].indent == ""


def test_set_attr_def_advanced_dont_break_next_block_indent_one_endl():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="c").value = "return 42\n"
    assert len(red.find("def", name="c")("endl")) == 4
    assert red.find("def", name="c").value.node_list[-1].indent == ""


def test_set_attr_def_advanced_dont_break_next_block_indent_two_endl():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="c").value = "return 42\n\n"
    assert len(red.find("def", name="c")("endl")) == 4
    assert red.find("def", name="c").value.node_list[-1].indent == ""


def test_set_attr_def_advanced_in_class_dont_break_next_block_indent():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="a").value = "return 42"
    assert len(red.find("def", name="a")("endl")) == 3
    assert red.find("def", name="a").value.node_list[-1].indent == "    "


def test_set_attr_def_advanced_in_class_dont_break_next_block_indent_one_endl():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="a").value = "return 42\n"
    assert len(red.find("def", name="a")("endl")) == 3
    assert red.find("def", name="a").value.node_list[-1].indent == "    "


def test_set_attr_def_advanced_in_class_at_the_end_dont_break_next_block_indent():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="b").value = "return 42"
    assert len(red.find("def", name="b")("endl")) == 4
    assert red.find("def", name="b").value.node_list[-1].indent == ""


def test_set_attr_def_advanced_in_class_at_the_end_dont_break_next_block_indent_one_endl():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="b").value = "return 42\n"
    assert len(red.find("def", name="b")("endl")) == 4
    assert red.find("def", name="b").value.node_list[-1].indent == ""


def test_set_attr_def_advanced_in_class_at_the_end_dont_break_next_block_indent_two_endl():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="b").value = "return 42\n\n"
    assert len(red.find("def", name="b")("endl")) == 4
    assert red.find("def", name="b").value.node_list[-1].indent == ""


def test_set_attr_def_advanced_inline_dont_break_next_block_indent():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="zomg").value = "return 42"
    assert len(red.find("def", name="zomg")("endl")) == 3
    assert red.find("def", name="zomg").value.node_list[-1].indent == "    "


def test_set_attr_def_advanced_inline_dont_break_next_block_indent_one_endl():
    red = RedBaron(code_for_block_setattr)
    red.find("def", name="zomg").value = "return 42\n"
    assert len(red.find("def", name="zomg")("endl")) == 3
    assert red.find("def", name="zomg").value.node_list[-1].indent == "    "


def test_set_attr_def_async_dont_break_initial_formatting():
    red = RedBaron("async    def a(): pass")
    assert red.dumps() == "async    def a(): pass\n"


def test_set_attr_def_set_async():
    red = RedBaron("def a(): pass")
    red[0].async_ = True
    assert red.dumps() == "async def a(): pass\n"


def test_set_attr_def_unset_async():
    red = RedBaron("async def a(): pass")
    red[0].async_ = False
    assert red.dumps() == "def a(): pass\n"


def test_set_attr_def_async_dont_break_initial_formatting_indent():
    red = RedBaron("class A:\n    async    def a(): pass")
    assert red.dumps() == "class A:\n    async    def a(): pass\n"


def test_set_attr_def_set_async_indent():
    red = RedBaron("class A:\n    def a(): pass")
    red.def_.async_ = True
    assert red.dumps() == "class A:\n    async def a(): pass\n"


def test_set_attr_def_unset_async_indent():
    red = RedBaron("class A:\n    async def a(): pass")
    red.def_.async_ = False
    assert red.dumps() == "class A:\n    def a(): pass\n"


def test_set_attr_def_set_return_annotation():
    red = RedBaron("def a(): pass")
    red[0].return_annotation = "Int"
    assert red.dumps() == "def a() -> Int: pass\n"


def test_set_attr_def_set_return_annotation_keep_formatting():
    red = RedBaron("def a() ->    Int: pass")
    red[0].return_annotation = "pouet"
    assert red.dumps() == "def a() ->    pouet: pass\n"


def test_set_attr_def_unset_return_annotation():
    red = RedBaron("def a() -> Int: pass")
    red[0].return_annotation = ""
    assert red.dumps() == "def a(): pass\n"


def test_set_decorator_def():
    red = RedBaron("def a(): pass")
    red[0].decorators = "@decorator"
    assert len(red[0].decorators.node_list) == 2
    assert red[0].decorators.dumps() == "@decorator\n"


def test_set_decorator_def_endl():
    red = RedBaron("def a(): pass")
    red[0].decorators = "@decorator\n"
    assert len(red[0].decorators.node_list) == 2
    assert red[0].decorators.dumps() == "@decorator\n"


def test_set_decorator_def_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = "    @decorator"
    assert len(red[0].decorators.node_list) == 2
    assert red[0].decorators.dumps() == "@decorator\n"


def test_set_decorator_def_indent_endl():
    red = RedBaron("def a(): pass")
    red[0].decorators = "    @decorator\n"
    assert len(red[0].decorators.node_list) == 2
    assert red[0].decorators.dumps() == "@decorator\n"


def test_set_decorator_def_too_small_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = " @decorator"
    assert len(red[0].decorators.node_list) == 2
    assert red[0].decorators.dumps() == "@decorator\n"


def test_set_decorator_def_too_small_indent_endl():
    red = RedBaron("def a(): pass")
    red[0].decorators = " @decorator\n"
    assert len(red[0].decorators.node_list) == 2
    assert red[0].decorators.dumps() == "@decorator\n"


def test_set_decorator_def_too_big_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = "       @decorator"
    assert len(red[0].decorators.node_list) == 2
    assert red[0].decorators.dumps() == "@decorator\n"


def test_set_decorator_def_too_big_indent_endl():
    red = RedBaron("def a(): pass")
    red[0].decorators = "       @decorator\n"
    assert len(red[0].decorators.node_list) == 2
    assert red[0].decorators.dumps() == "@decorator\n"


def test_set_decorator_def_complex():
    red = RedBaron("def a(): pass")
    red[0].decorators = "@plop\n@plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_def_complex_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = "    @plop\n    @plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_def_complex_endl_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = "\n    @plop\n    @plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_def_complex_space_endl_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = "      \n    @plop\n    @plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_def_complex_too_small_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = " @plop\n @plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_def_complex_endl_too_small_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = "\n @plop\n @plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_def_complex_space_endl_too_small_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = " \n @plop\n @plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_def_complex_too_big_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = "     @plop\n     @plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_def_complex_endl_too_big_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = "\n     @plop\n     @plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_def_complex_space_endl_too_big_indent():
    red = RedBaron("def a(): pass")
    red[0].decorators = " \n     @plop\n     @plouf"
    assert len(red[0].decorators.node_list) == 4
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_set_decorator_indented_def():
    red = RedBaron(code_for_block_setattr)
    red.find("def", "b").decorators = "@pouet"
    assert len(red.find("def", "b").decorators.node_list) == 2
    assert red.find("def", "b").decorators.node_list[-1].indent == "    "


def test_set_decorators_indented_def():
    red = RedBaron(code_for_block_setattr)
    red.find("def", "b").decorators = "@pouet\n@plop"
    assert len(red.find("def", "b").decorators.node_list) == 4
    assert red.find("def", "b").decorators.node_list[-1].indent == "    "
    assert red.find("def", "b").decorators.node_list[-3].indent == "    "


def test_assign_node_setattr_target():
    red = RedBaron("a = b")
    red[0].target = "plop"
    assert red.dumps() == "plop = b"
    with pytest.raises(Exception):
        red[0].target = "raise"


def test_assign_node_setattr_value():
    red = RedBaron("a = b")
    red[0].value = "plop"
    assert red.dumps() == "a = plop"
    with pytest.raises(Exception):
        red[0].value = "raise"


def test_assign_node_setattr_operator():
    red = RedBaron("a = b")
    red[0].operator = '+'
    assert red.dumps() == "a += b"
    red[0].operator = '+='
    assert red.dumps() == "a += b"
    red[0].operator = '='
    assert red.dumps() == "a = b"
    red[0].operator = '-'
    assert red.dumps() == "a -= b"
    red[0].operator = ''
    assert red.dumps() == "a = b"
    with pytest.raises(Exception):
        red[0].operator = "raise"


def test_assign_node_setattr_annotation():
    red = RedBaron("a = b")
    red[0].annotation = "Int"
    assert red.dumps() == "a : Int = b"


def test_assign_node_setattr_annotation_existing():
    red = RedBaron("a : Str = b")
    red[0].annotation = "Int"
    assert red.dumps() == "a : Int = b"


def test_assign_node_setattr_remove():
    red = RedBaron("a : Int = b")
    red[0].annotation = ""
    assert red.dumps() == "a = b"


def test_standalone_annotation():
    red = RedBaron("a : Int")
    red[0].annotation = "Str"
    assert red.dumps() == "a : Str"


def test_star_var():
    red = RedBaron("a, *b = c")
    red[0].target[1].value = "(x, y)"
    assert red.dumps() == "a, *(x, y) = c"


def test_await_setattr_value():
    red = RedBaron("await a")
    red[0].value = "b"
    assert red[0].dumps() == "await b"


def test_await_setattr_value_expr():
    red = RedBaron("await a")
    with pytest.raises(Exception):
        red[0].value = "def a(): pass"


def test_for_setattr_value():
    red = RedBaron("for i in a: pass")
    red[0].value = "continue"
    assert red[0].value.dumps() == "\n    continue\n"


def test_for_setattr_target():
    red = RedBaron("for i in a: pass")
    red[0].target = "caramba"
    assert red.dumps() == "for i in caramba: pass\n"
    assert red[0].target.type == "name"
    with pytest.raises(Exception):
        red[0].target = "raise"


def test_for_setattr_iterator():
    red = RedBaron("for i in a: pass")
    red[0].iterator = "caramba"
    assert red.dumps() == "for caramba in a: pass\n"
    assert red[0].iterator.type == "name"
    with pytest.raises(Exception):
        red[0].iterator = "raise"


def test_set_attr_for_async_dont_break_initial_formatting():
    red = RedBaron("async    for a in b: pass")
    assert red.dumps() == "async    for a in b: pass\n"


def test_set_attr_for_set_async():
    red = RedBaron("for a in b: pass")
    red[0].async_ = True
    assert red.dumps() == "async for a in b: pass\n"


def test_set_attr_for_unset_async():
    red = RedBaron("async for a in b: pass")
    red[0].async_ = False
    assert red.dumps() == "for a in b: pass\n"


def test_set_attr_for_async_dont_break_initial_formatting_indent():
    red = RedBaron("class A:\n    async    for a in b: pass")
    assert red.dumps() == "class A:\n    async    for a in b: pass\n"


def test_set_attr_for_set_async_indent():
    red = RedBaron("class A:\n    for a in b: pass")
    red.for_.async_ = True
    assert red.dumps() == "class A:\n    async for a in b: pass\n"


def test_set_attr_for_unset_async_indent():
    red = RedBaron("class A:\n    async for a in b: pass")
    red.for_.async_ = False
    assert red.dumps() == "class A:\n    for a in b: pass\n"


def test_while_setattr_value():
    red = RedBaron("while a: pass")
    red[0].value = "continue"
    assert red[0].value.dumps() == "\n    continue\n"


def test_while_setattr_test():
    red = RedBaron("while a: pass")
    red[0].test = "caramba"
    assert red.dumps() == "while caramba: pass\n"
    assert red[0].test.type == "name"
    with pytest.raises(Exception):
        red[0].test = "raise"


def test_class_setattr_value():
    red = RedBaron("class a: pass")
    red[0].value = "def z(): pass"
    assert red[0].value.dumps() == "\n    def z(): pass\n"


def test_class_setattr_decorators():
    red = RedBaron("class a: pass")
    red[0].decorators = "@plop\n@plouf"
    assert red[0].decorators.dumps() == "@plop\n@plouf\n"


def test_class_setattr_inherit_from():
    red = RedBaron("class a: pass")
    red[0].inherit_from = "A"
    assert red[0].dumps() == "class a(A): pass\n"


def test_with_setattr_value():
    red = RedBaron("with a: pass")
    red[0].value = "def z(): pass"
    assert red[0].value.dumps() == "\n    def z(): pass\n"


def test_with_setattr_context():
    red = RedBaron("with a: pass")
    red[0].contexts = "a as b, b as c"
    assert red[0].dumps() == "with a as b, b as c: pass\n"


def test_set_attr_with_async_dont_break_initial_withmatting():
    red = RedBaron("async    with a as b: pass")
    assert red.dumps() == "async    with a as b: pass\n"


def test_set_attr_with_set_async():
    red = RedBaron("with a as b: pass")
    red[0].async_ = True
    assert red.dumps() == "async with a as b: pass\n"


def test_set_attr_with_unset_async():
    red = RedBaron("async with a as b: pass")
    red[0].async_ = False
    assert red.dumps() == "with a as b: pass\n"


def test_set_attr_with_async_dont_break_initial_withmatting_indent():
    red = RedBaron("class A:\n    async    with a as b: pass")
    assert red.dumps() == "class A:\n    async    with a as b: pass\n"


def test_set_attr_with_set_async_indent():
    red = RedBaron("class A:\n    with a as b: pass")
    red.with_.async_ = True
    assert red.dumps() == "class A:\n    async with a as b: pass\n"


def test_set_attr_with_unset_async_indent():
    red = RedBaron("class A:\n    async with a as b: pass")
    red.with_.async_ = False
    assert red.dumps() == "class A:\n    with a as b: pass\n"


def test_with_context_item_value():
    red = RedBaron("with a: pass")
    red[0].contexts[0].value = "plop"
    assert red[0].dumps() == "with plop: pass\n"


def test_with_context_item_as():
    red = RedBaron("with a: pass")
    red[0].contexts[0].as_ = "plop"
    assert red[0].contexts[0].as_ != ""
    assert red[0].dumps() == "with a as plop: pass\n"


def test_with_context_item_as_empty_string():
    red = RedBaron("with a as b: pass")
    red[0].contexts[0].as_ = ""
    assert red[0].contexts[0].as_ is ""
    assert red[0].dumps() == "with a: pass\n"


def test_if_setattr_value():
    red = RedBaron("if a: pass")
    red[0].value[0].value = "continue"
    assert red[0].value[0].value.dumps() == "\n    continue\n"


def test_setattr_if_test():
    red = RedBaron("if a: pass")
    red[0].value[0].test = "caramba"
    assert red.dumps() == "if caramba: pass\n"
    assert red[0].value[0].test.type == "name"
    with pytest.raises(Exception):
        red[0].value[0].test = "raise"


def test_elif_setattr_value():
    red = RedBaron("if a: pass\nelif b: pass")
    red[0].value[1].value = "continue"
    assert red[0].value[1].value.dumps() == "\n    continue\n"


def test_setattr_elif_test():
    red = RedBaron("if a: pass\nelif b: pass")
    red[0].value[1].test = "caramba"
    assert red.dumps() == "if a: pass\nelif caramba: pass\n"
    assert red[0].value[1].test.type == "name"
    with pytest.raises(Exception):
        red[0].value[1].test = "raise"


def test_else_setattr_value():
    red = RedBaron("if a: pass\nelse: pass")
    red[0].value[1].value = "continue"
    assert red[0].value[1].value.dumps() == "\n    continue\n"


def test_try_setattr_value():
    red = RedBaron("try: pass\nexcept: pass\n")
    red[0].value = "continue"
    assert red[0].value.dumps() == "\n    continue\n"


def test_finally_setattr_value():
    red = RedBaron("try: pass\nfinally: pass\n")
    red[0].finally_.value = "continue"
    assert red[0].finally_.value.dumps() == "\n    continue\n"


def test_finally_getattr_on_try():
    red = RedBaron("try: pass\nfinally: pass\n")
    assert red[0].finally_ is getattr(red[0], "finally")


def test_except_setattr_value():
    red = RedBaron("try: pass\nexcept: pass\n")
    red[0].excepts[0].value = "continue"
    assert red[0].excepts[0].value.dumps() == "\n    continue\n"


def test_except_setattr_exception():
    red = RedBaron("try: pass\nexcept: pass\n")
    red[0].excepts[0].exception = "Plop"
    assert red[0].excepts[0].dumps() == "except Plop: pass\n"


def test_except_setattr_exception_none():
    red = RedBaron("try: pass\nexcept Pouet: pass\n")
    red[0].excepts[0].exception = ""
    assert red[0].excepts[0].dumps() == "except: pass\n"


def test_except_setattr_exception_none_with_target():
    red = RedBaron("try: pass\nexcept Pouet as plop: pass\n")
    red[0].excepts[0].exception = ""
    assert red[0].excepts[0].dumps() == "except: pass\n"


def test_except_setattr_target():
    red = RedBaron("try: pass\nexcept Pouet: pass\n")
    red[0].excepts[0].target = "plop"
    assert red[0].excepts[0].dumps() == "except Pouet as plop: pass\n"


def test_except_setattr_target_raise_no_exception():
    red = RedBaron("try: pass\nexcept: pass\n")
    with pytest.raises(Exception):
        red[0].excepts[0].target = "plop"


def test_except_setattr_target_none():
    red = RedBaron("try: pass\nexcept Pouet as plop: pass\n")
    red[0].excepts[0].target = ""
    assert red[0].excepts[0].delimiter == ""
    assert red[0].excepts[0].dumps() == "except Pouet: pass\n"


def test_except_setattr_delimiter_comma():
    red = RedBaron("try: pass\nexcept Pouet as plop: pass\n")
    red[0].excepts[0].delimiter = ","
    assert red[0].excepts[0].delimiter == ","
    assert red[0].excepts[0].dumps() == "except Pouet, plop: pass\n"


def test_except_setattr_delimiter_as():
    red = RedBaron("try: pass\nexcept Pouet, plop: pass\n")
    red[0].excepts[0].delimiter = "as"
    assert red[0].excepts[0].delimiter == "as"
    assert red[0].excepts[0].dumps() == "except Pouet as plop: pass\n"


def test_except_setattr_delimiter_bad():
    red = RedBaron("try: pass\nexcept Pouet, plop: pass\n")
    with pytest.raises(Exception):
        red[0].excepts[0].delimiter = "pouet"


def test_call_setattr_value():
    red = RedBaron("a()")
    red[0].value[1].value = "b=2, *pouet"
    assert red.dumps() == "a(b=2, *pouet)"


def test_assert_setattr_value():
    red = RedBaron("assert a")
    red[0].value = "42 + pouet"
    assert red.dumps() == "assert 42 + pouet"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass"


def test_assert_setattr_message():
    red = RedBaron("assert a")
    red[0].message = "plop"
    assert red.dumps() == "assert a, plop"


def test_assert_setattr_message_none():
    red = RedBaron("assert a, plop")
    red[0].message = ""
    assert red.dumps() == "assert a"


def test_associative_parenthesis_setattr_value():
    red = RedBaron("(plop)")
    red[0].value = "1 + 43"
    assert red.dumps() == "(1 + 43)"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass"


def test_atom_trailers_setattr_value():
    red = RedBaron("a(plop)")
    red[0].value = "a.plop[2](42)"
    assert red.dumps() == "a.plop[2](42)"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass"


def test_binary_setattr_value():
    red = RedBaron("0b101001")
    red[0].value = "0b1100"
    assert red.dumps() == "0b1100"
    with pytest.raises(Exception):
        red[0].value = "not_binary"


def test_binary_operator_setattr_value():
    red = RedBaron("a - b")
    red[0].value = "+"
    assert red.dumps() == "a + b"
    with pytest.raises(Exception):
        red[0].value = "some illegal stuff"


def test_binary_operator_setattr_first():
    red = RedBaron("a + b")
    red[0].first = "caramba"
    assert red.dumps() == "caramba + b"
    with pytest.raises(Exception):
        red[0].first = "def a(): pass"


def test_binary_operator_setattr_second():
    red = RedBaron("a + b")
    red[0].second = "caramba"
    assert red.dumps() == "a + caramba"
    with pytest.raises(Exception):
        red[0].second = "def a(): pass"


def test_boolean_operator_setattr_value():
    red = RedBaron("a and b")
    red[0].value = "or"
    assert red.dumps() == "a or b"
    with pytest.raises(Exception):
        red[0].value = "some illegal stuff"


def test_boolean_operator_setattr_first():
    red = RedBaron("a and b")
    red[0].first = "caramba"
    assert red.dumps() == "caramba and b"
    with pytest.raises(Exception):
        red[0].first = "def a(): pass"


def test_boolean_operator_setattr_second():
    red = RedBaron("a and b")
    red[0].second = "caramba"
    assert red.dumps() == "a and caramba"
    with pytest.raises(Exception):
        red[0].second = "def a(): pass"


def test_comparison_setattr_value():
    red = RedBaron("a > b")
    red[0].value = "<"
    assert red.dumps() == "a < b"
    with pytest.raises(Exception):
        red[0].value = "some illegal stuff"


def test_comparison_setattr_first():
    red = RedBaron("a > b")
    red[0].first = "caramba"
    assert red.dumps() == "caramba > b"
    with pytest.raises(Exception):
        red[0].first = "def a(): pass"


def test_comparison_setattr_second():
    red = RedBaron("a > b")
    red[0].second = "caramba"
    assert red.dumps() == "a > caramba"
    with pytest.raises(Exception):
        red[0].second = "def a(): pass"


def test_call_argument_setattr_value():
    red = RedBaron("a(b)")
    red[0].value[1].value[0].value = "caramba"
    assert red.dumps() == "a(caramba)"
    with pytest.raises(Exception):
        red[0].value[1].value[0].value = "def a(): pass"


def test_call_argument_setattr_name():
    red = RedBaron("a(b)")
    red[0].value[1].value[0].target = "caramba"
    assert red.dumps() == "a(caramba=b)"
    red[0].value[1].value[0].target = ""
    assert red.dumps() == "a(b)"
    with pytest.raises(Exception):
        red[0].value[1].value[0].value = "def a(): pass"


def test_decorator_setattr_value():
    red = RedBaron("@pouet\ndef a(): pass\n")
    red[0].decorators[0].value = "a.b.c"
    assert red.dumps() == "@a.b.c\ndef a(): pass\n"
    assert red[0].decorators[0].value.type == "dotted_name"
    with pytest.raises(Exception):
        red[0].decorators[0].value = "def a(): pass"
    with pytest.raises(Exception):
        red[0].decorators[0].value = "a()"


def test_decorator_setattr_call():
    red = RedBaron("@pouet\ndef a(): pass\n")
    red[0].decorators[0].call = "(*a)"
    assert red.dumps() == "@pouet(*a)\ndef a(): pass\n"
    with pytest.raises(Exception):
        red[0].decorators[0].call = "def a(): pass"
    with pytest.raises(Exception):
        red[0].decorators[0].call = ".stuff"


def test_decorator_setattr_call_none():
    red = RedBaron("@pouet(zob)\ndef a(): pass\n")
    red[0].decorators[0].call = ""
    assert red.dumps() == "@pouet\ndef a(): pass\n"


def test_def_argument_setattr_value():
    red = RedBaron("def a(b): pass")
    red[0].arguments[0].value = "plop"
    assert red.dumps() == "def a(b=plop): pass\n"
    with pytest.raises(Exception):
        red[0].arguments[0].value = "def a(): pass\n"


def test_def_argument_setattr_annotation():
    red = RedBaron("def a(b): pass")
    red[0].arguments[0].annotation = "Int"
    assert red.dumps() == "def a(b : Int): pass\n"


def test_def_argument_setattr_annotation_value():
    red = RedBaron("def a(b : Int): pass")
    red[0].arguments[0].value = "plop"
    assert red.dumps() == "def a(b : Int=plop): pass\n"


def test_def_argument_setattr_remove_annotation():
    red = RedBaron("def a(b : Int): pass")
    red[0].arguments[0].annotation = ""
    assert red.dumps() == "def a(b): pass\n"


def test_list_argument_setattr_annotation():
    red = RedBaron("def a(*b): pass")
    red[0].arguments[0].annotation = "Int"
    assert red.dumps() == "def a(*b : Int): pass\n"


def test_list_argument_setattr_remove_annotation():
    red = RedBaron("def a(*b : Int): pass")
    red[0].arguments[0].annotation = ""
    assert red.dumps() == "def a(*b): pass\n"


def test_dict_argument_setattr_annotation():
    red = RedBaron("def a(**b): pass")
    red[0].arguments[0].annotation = "Int"
    assert red.dumps() == "def a(**b : Int): pass\n"


def test_dict_argument_setattr_remove_annotation():
    red = RedBaron("def a(**b : Int): pass")
    red[0].arguments[0].annotation = ""
    assert red.dumps() == "def a(**b): pass\n"


def test_del_setattr_value():
    red = RedBaron("del a")
    red[0].value = "a, b, c"
    assert red.dumps() == "del a, b, c"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_dict_argument_setattr_value():
    red = RedBaron("a(**b)")
    red[0].value[1].value[0].value = "plop"
    assert red.dumps() == "a(**plop)"
    with pytest.raises(Exception):
        red[0].value[1].value[0].value = "def a(): pass\n"


def test_dict_item_setattr_value():
    red = RedBaron("{a: b}")
    red[0].value[0].value = "plop"
    assert red.dumps() == "{a: plop}"
    with pytest.raises(Exception):
        red[0].value[0].value = "def a(): pass\n"


def test_dict_item_setattr_key():
    red = RedBaron("{a: b}")
    red[0].value[0].key = "plop"
    assert red.dumps() == "{plop: b}"
    with pytest.raises(Exception):
        red[0].value[0].key = "def a(): pass\n"


def test_exec_setattr_value():
    red = RedBaron("exec a")
    red[0].value = "plop"
    assert red.dumps() == "exec plop"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_exec_setattr_globals():
    red = RedBaron("exec a in b")
    red[0].globals = "pouet"
    assert red.dumps() == "exec a in pouet"
    with pytest.raises(Exception):
        red[0].globals = "def a(): pass\n"


def test_exec_setattr_globals_wasnt_set():
    red = RedBaron("exec a")
    red[0].globals = "pouet"
    assert red.dumps() == "exec a in pouet"
    with pytest.raises(Exception):
        red[0].globals = "def a(): pass\n"


def test_exec_setattr_globals_none():
    red = RedBaron("exec a in b")
    red[0].globals = ""
    assert red.dumps() == "exec a"
    with pytest.raises(Exception):
        red[0].globals = "def a(): pass\n"


def test_exec_setattr_locals():
    red = RedBaron("exec a in b")
    red[0].locals = "pouet"
    assert red.dumps() == "exec a in b, pouet"
    with pytest.raises(Exception):
        red[0].locals = "def a(): pass\n"


def test_exec_setattr_locals_none():
    red = RedBaron("exec a in b, c")
    red[0].locals = ""
    assert red.dumps() == "exec a in b"
    with pytest.raises(Exception):
        red[0].locals = "def a(): pass\n"


def test_exec_setattr_locals_no_globals_raise():
    red = RedBaron("exec a")
    with pytest.raises(Exception):
        red[0].locals = "pouet"


def test_from_import_setattr_value():
    red = RedBaron("from a import b")
    red[0].value = "a.b.c"
    assert red.dumps() == "from a.b.c import b"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_from_import_setattr_targets():
    red = RedBaron("from a import b")
    red[0].targets = "a as plop, d as oufti"
    assert red.dumps() == "from a import a as plop, d as oufti"
    with pytest.raises(Exception):
        red[0].targets = "def a(): pass\n"


def test_getitem_setattr_value():
    red = RedBaron("a[b]")
    red[0].value[1].value = "a.b.c"
    assert red.dumps() == "a[a.b.c]"
    with pytest.raises(Exception):
        red[0].value[1].value = "def a(): pass\n"


def test_nonlocal_setattr_value():
    red = RedBaron("nonlocal a")
    red[0].value = "a, b, c"
    assert red.dumps() == "nonlocal a, b, c"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_global_setattr_value():
    red = RedBaron("global a")
    red[0].value = "a, b, c"
    assert red.dumps() == "global a, b, c"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_lambda_setattr_value():
    red = RedBaron("lambda: plop")
    red[0].value = "42 * 3"
    assert red.dumps() == "lambda: 42 * 3"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_lambda_setattr_arguments():
    red = RedBaron("lambda: plop")
    red[0].arguments = "a, b=c, *d, **e"
    assert red.dumps() == "lambda a, b=c, *d, **e: plop"
    with pytest.raises(Exception):
        red[0].arguments = "def a(): pass\n"


def test_lambda_setattr_arguments_none():
    red = RedBaron("lambda a, b=c, *d, **e: plop")
    red[0].arguments = ""
    assert red.dumps() == "lambda: plop"


def test_list_argument_setattr_value():
    red = RedBaron("lambda *b: plop")
    red[0].arguments[0].value = "hop"
    assert red.dumps() == "lambda *hop: plop"
    with pytest.raises(Exception):
        red[0].arguments[0].value = "def a(): pass\n"


def test_print_setattr_value():
    red = RedBaron("print a")
    red[0].value = "hop, plop"
    assert red.dumps() == "print hop, plop"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_print_setattr_value_none():
    red = RedBaron("print a")
    red[0].value = ""
    assert red.dumps() == "print"


def test_print_setattr_value_none_to_not_none():
    red = RedBaron("print")
    red[0].value = "a"
    assert red.dumps() == "print a"


def test_print_setattr_destination():
    red = RedBaron("print >>zop")
    red[0].destination = "hop"
    assert red.dumps() == "print >>hop"
    with pytest.raises(Exception):
        red[0].destination = "def a(): pass\n"


def test_print_setattr_destination_none():
    red = RedBaron("print >>zop")
    red[0].destination = ""
    assert red.dumps() == "print"


def test_print_setattr_destination_none_to_not_none():
    red = RedBaron("print")
    red[0].destination = "hop"
    assert red.dumps() == "print >>hop"


def test_print_setattr_value_was_none_and_had_destination():
    red = RedBaron("print >>zop")
    red[0].value = "plop"
    assert red.dumps() == "print >>zop, plop"


def test_print_setattr_value_none_had_destination():
    red = RedBaron("print >>zop, plop")
    red[0].value = ""
    assert red.dumps() == "print >>zop"


def test_print_setattr_dest_none_had_value():
    red = RedBaron("print >>zop, plop")
    red[0].destination = ""
    assert red.dumps() == "print plop"


def test_print_setattr_dest_was_none_had_value():
    red = RedBaron("print zop")
    red[0].destination = "plop"
    assert red.dumps() == "print >>plop, zop"


def test_raise_setattr_value():
    red = RedBaron("raise a")
    red[0].value = "hop"
    assert red.dumps() == "raise hop"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_raise_setattr_value_none():
    red = RedBaron("raise a")
    red[0].value = ""
    assert red.dumps() == "raise"


def test_raise_setattr_value_was_none():
    red = RedBaron("raise")
    red[0].value = "a"
    assert red.dumps() == "raise a"


def test_raise_setattr_instance():
    red = RedBaron("raise a, b")
    red[0].instance = "hop"
    assert red.dumps() == "raise a, hop"
    with pytest.raises(Exception):
        red[0].instance = "def a(): pass\n"


def test_raise_setattr_instance_none():
    red = RedBaron("raise a, b")
    red[0].instance = ""
    assert red.dumps() == "raise a"


def test_raise_setattr_instance_was_none():
    red = RedBaron("raise a")
    red[0].instance = "b"
    assert red.dumps() == "raise a, b"


def test_raise_setattr_instance_no_value_raise():
    red = RedBaron("raise")
    with pytest.raises(Exception):
        red[0].instance = "b"


def test_raise_setattr_traceback():
    red = RedBaron("raise a, b, c")
    red[0].traceback = "hop"
    assert red.dumps() == "raise a, b, hop"
    with pytest.raises(Exception):
        red[0].traceback = "def a(): pass\n"


def test_raise_setattr_traceback_none():
    red = RedBaron("raise a, b, c")
    red[0].traceback = ""
    assert red.dumps() == "raise a, b"


def test_raise_setattr_traceback_was_none():
    red = RedBaron("raise a, b")
    red[0].traceback = "c"
    assert red.dumps() == "raise a, b, c"


def test_raise_setattr_traceback_raise():
    red = RedBaron("raise")
    with pytest.raises(Exception):
        red[0].traceback = "c"
    red = RedBaron("raise a")
    with pytest.raises(Exception):
        red[0].traceback = "c"


def test_raise_from_setattr_instance():
    red = RedBaron("raise a from b")
    red[0].instance = "hop"
    assert red.dumps() == "raise a from hop"


def test_raise_from_setattr_instance_remove():
    red = RedBaron("raise a from b")
    red[0].instance = ""
    assert red.dumps() == "raise a"


def test_raise_from_setattr_set_instance():
    red = RedBaron("raise a")
    red[0].instance = "b"
    assert red.dumps() == "raise a, b"
    red[0].comma_or_from = "from"
    assert red.dumps() == "raise a from b"
    red[0].comma_or_from = ","
    assert red.dumps() == "raise a, b"


def test_raise_from_setattr_set_comma():
    red = RedBaron("raise a from b")
    red[0].comma_or_from = ","
    assert red.dumps() == "raise a, b"


def test_raise_from_setattr_set_from():
    red = RedBaron("raise a, b")
    red[0].comma_or_from = "from"
    assert red.dumps() == "raise a from b"


def test_return_setattr_value():
    red = RedBaron("return a")
    red[0].value = "hop"
    assert red.dumps() == "return hop"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_return_setattr_value_none():
    red = RedBaron("return a")
    red[0].value = ""
    assert red.dumps() == "return"


def test_return_setattr_value_was_none():
    red = RedBaron("return")
    red[0].value = "a"
    assert red.dumps() == "return a"


def test_slice_setattr_lower():
    red = RedBaron("a[:]")
    red[0].value[1].value.lower = "hop"
    assert red.dumps() == "a[hop:]"
    with pytest.raises(Exception):
        red[0].value[1].value.lower = "def a(): pass\n"


def test_slice_setattr_lower_none():
    red = RedBaron("a[a:]")
    red[0].value[1].value.lower = ""
    assert red.dumps() == "a[:]"


def test_slice_setattr_upper():
    red = RedBaron("a[:]")
    red[0].value[1].value.upper = "hop"
    assert red.dumps() == "a[:hop]"
    with pytest.raises(Exception):
        red[0].value[1].value.upper = "def a(): pass\n"


def test_slice_setattr_upper_none():
    red = RedBaron("a[:hop]")
    red[0].value[1].value.upper = ""
    assert red.dumps() == "a[:]"


def test_slice_setattr_step():
    red = RedBaron("a[:]")
    red[0].value[1].value.step = "hop"
    assert red.dumps() == "a[::hop]"
    with pytest.raises(Exception):
        red[0].value[1].value.step = "def a(): pass\n"


def test_slice_setattr_step_none():
    red = RedBaron("a[::hop]")
    red[0].value[1].value.step = ""
    assert red.dumps() == "a[:]"


def test_ternary_operator_setattr_first():
    red = RedBaron("a if b else c")
    red[0].first = "hop"
    assert red.dumps() == "hop if b else c"
    with pytest.raises(Exception):
        red[0].first = "def a(): pass\n"


def test_ternary_operator_setattr_second():
    red = RedBaron("a if b else c")
    red[0].second = "hop"
    assert red.dumps() == "a if b else hop"
    with pytest.raises(Exception):
        red[0].second = "def a(): pass\n"


def test_ternary_operator_setattr_value():
    red = RedBaron("a if b else c")
    red[0].value = "hop"
    assert red.dumps() == "a if hop else c"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_unitary_operator_setattr_target():
    red = RedBaron("-a")
    red[0].target = "hop"
    assert red.dumps() == "-hop"
    with pytest.raises(Exception):
        red[0].target = "def a(): pass\n"


def test_yield_setattr_value():
    red = RedBaron("yield a")
    red[0].value = "hop"
    assert red.dumps() == "yield hop"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_yield_setattr_value_none():
    red = RedBaron("yield a")
    red[0].value = ""
    assert red.dumps() == "yield"


def test_yield_setattr_value_was_none():
    red = RedBaron("yield")
    red[0].value = "a"
    assert red.dumps() == "yield a"


def test_yield_atom_setattr_value():
    red = RedBaron("(yield a)")
    red[0].value = "hop"
    assert red.dumps() == "(yield hop)"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_yield_atom_setattr_value_none():
    red = RedBaron("(yield a)")
    red[0].value = ""
    assert red.dumps() == "(yield)"


def test_yield_atom_setattr_value_was_none():
    red = RedBaron("(yield)")
    red[0].value = "a"
    assert red.dumps() == "(yield a)"


def test_yield_from_setattr_value():
    red = RedBaron("yield from a")
    red[0].value = "hop"
    assert red.dumps() == "yield from hop"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_list_comprehension_set_attr_result():
    red = RedBaron("[a for b in c]")
    red[0].result = "hop"
    assert red.dumps() == "[hop for b in c]"
    with pytest.raises(Exception):
        red[0].result = "def a(): pass\n"


def test_list_comprehension_set_attr_generators():
    red = RedBaron("[a for b in c]")
    red[0].generators = "for pouet in plop if zuto"
    assert red.dumps() == "[a for pouet in plop if zuto]"
    with pytest.raises(Exception):
        red[0].generators = "def a(): pass\n"


def test_generator_comprehension_set_attr_result():
    red = RedBaron("(a for b in c)")
    red[0].result = "hop"
    assert red.dumps() == "(hop for b in c)"
    with pytest.raises(Exception):
        red[0].result = "def a(): pass\n"


def test_generator_comprehension_set_attr_generators():
    red = RedBaron("(a for b in c)")
    red[0].generators = "for pouet in plop if zuto"
    assert red.dumps() == "(a for pouet in plop if zuto)"
    with pytest.raises(Exception):
        red[0].generators = "def a(): pass\n"


def test_set_comprehension_set_attr_result():
    red = RedBaron("{a for b in c}")
    red[0].result = "hop"
    assert red.dumps() == "{hop for b in c}"
    with pytest.raises(Exception):
        red[0].result = "def a(): pass\n"


def test_set_comprehension_set_attr_generators():
    red = RedBaron("{a for b in c}")
    red[0].generators = "for pouet in plop if zuto"
    assert red.dumps() == "{a for pouet in plop if zuto}"
    with pytest.raises(Exception):
        red[0].generators = "def a(): pass\n"


def test_dict_comprehension_set_attr_result():
    red = RedBaron("{a: z for b in c}")
    red[0].result = "hop: pop"
    assert red.dumps() == "{hop: pop for b in c}"
    with pytest.raises(Exception):
        red[0].result = "def a(): pass\n"


def test_dict_comprehension_set_attr_generators():
    red = RedBaron("{a: z for b in c}")
    red[0].generators = "for pouet in plop if zuto"
    assert red.dumps() == "{a: z for pouet in plop if zuto}"
    with pytest.raises(Exception):
        red[0].generators = "def a(): pass\n"


def test_comprehension_loop_setattr_iterator():
    red = RedBaron("{a: z for b in c}")
    red[0].generators[0].iterator = "plop"
    assert red.dumps() == "{a: z for plop in c}"
    with pytest.raises(Exception):
        red[0].generators[0].iterator = "def a(): pass\n"


def test_comprehension_loop_setattr_target():
    red = RedBaron("{a: z for b in c}")
    red[0].generators[0].target = "plop"
    assert red.dumps() == "{a: z for b in plop}"
    with pytest.raises(Exception):
        red[0].generators[0].target = "def a(): pass\n"


def test_comprehension_loop_setattr_ifs():
    red = RedBaron("{a: z for b in c}")
    red[0].generators[0].ifs = "if x if y if z"
    assert red.dumps() == "{a: z for b in c if x if y if z}"
    with pytest.raises(Exception):
        red[0].generators[0].ifs = "def a(): pass\n"


def test_comprehension_loop_setattr_ifs_none():
    red = RedBaron("{a: z for b in c if x if y if z}")
    red[0].generators[0].ifs = ""
    assert red.dumps() == "{a: z for b in c}"


def test_comprehension_if_setattr_value():
    red = RedBaron("[a for b in c if plop]")
    red[0].generators[0].ifs[0].value = "1 + 1 == 2"
    assert red.dumps() == "[a for b in c if 1 + 1 == 2]"
    with pytest.raises(Exception):
        red[0].generators[0].ifs[0].value = "def a(): pass\n"


def test_argument_generator_comprehension_set_attr_result():
    red = RedBaron("a(a for b in c)")
    red[0].value[1].value[0].result = "hop"
    assert red.dumps() == "a(hop for b in c)"
    with pytest.raises(Exception):
        red[0].value[1].value[0].result = "def a(): pass\n"


def test_argument_generator_comprehension_set_attr_generators():
    red = RedBaron("a(a for b in c)")
    red[0].value[1].value[0].generators = "for pouet in plop if zuto"
    assert red.dumps() == "a(a for pouet in plop if zuto)"
    with pytest.raises(Exception):
        red[0].value[1].value[0].generators = "def a(): pass\n"


def test_string_chain_set_attr_value():
    red = RedBaron("'a' 'b'")
    red[0].value = "'a'     'b' 'c'"
    assert red.dumps() == "'a'     'b' 'c'"
    with pytest.raises(Exception):
        red[0].value = "def a(): pass\n"


def test_dotted_as_name_setattr_value():
    red = RedBaron("import a")
    red[0].value[0].value = "a.b.c"
    assert red.dumps() == "import a.b.c"
    with pytest.raises(Exception):
        red[0].value[0].value = "def a(): pass\n"


def test_dotted_as_name_setattr_target():
    red = RedBaron("import a as qsd")
    red[0].value[0].target = "plop"
    assert red.dumps() == "import a as plop"
    with pytest.raises(Exception):
        red[0].value[0].target = "def a(): pass\n"


def test_dotted_as_name_setattr_target_none():
    red = RedBaron("import a as qsd")
    red[0].value[0].target = ""
    assert red.dumps() == "import a"


def test_dotted_as_name_setattr_target_was_none():
    red = RedBaron("import a")
    red[0].value[0].target = "qsd"
    assert red.dumps() == "import a as qsd"


def test_name_as_name_setattr_value():
    red = RedBaron("from x import a")
    red[0].targets[0].value = "a"
    assert red.dumps() == "from x import a"
    with pytest.raises(Exception):
        red[0].targets[0].value = "def a(): pass\n"


def test_name_as_name_setattr_target():
    red = RedBaron("from x import a as qsd")
    red[0].targets[0].target = "plop"
    assert red.dumps() == "from x import a as plop"
    with pytest.raises(Exception):
        red[0].targets[0].target = "def a(): pass\n"


def test_name_as_name_setattr_target_none():
    red = RedBaron("from x import a as qsd")
    red[0].targets[0].target = ""
    assert red.dumps() == "from x import a"


def test_name_as_name_setattr_target_was_none():
    red = RedBaron("from x import a")
    red[0].targets[0].target = "qsd"
    assert red.dumps() == "from x import a as qsd"


has_else_member_list = [("while True:\n    pass\n", "else"), ("for a in a:\n    pass\n", "else"),("try:\n    pass\nexcept:\n    pass\n", "else"), ("try:\n    pass\nexcept:\n    pass\n", "finally")]

@pytest.fixture(params=has_else_member_list)
def has_else_member(request):
    return request.param

simple_body = ["plop",
"    plop",
"\nplop",
"  \nplop",
"  \n   plop",
"                          plop",
"\n                          plop",
"  \n                        plop",
"plop\n",
"plop\n\n",
"plop\n\n\n\n\n",
]

@pytest.fixture(params=simple_body)
def else_simple_body(request):
    return request.param


two_lines_body = ["plop\nplouf",
"\nplop\nplouf",
"    plop\n    plouf",
"\n    plop\n    plouf",
"    \n    plop\n    plouf",
" plop\n plouf",
"\n plop\n plouf",
" \n plop\n plouf",
"            plop\n            plouf",
"\n            plop\n            plouf",
"            \n            plop\n            plouf"]

@pytest.fixture(params=two_lines_body)
def else_two_line_body(request):
    return request.param


simple_body_starting_with_else = [
    "%s:\n    pass",
    "%s:\n    pass\n",
    "    %s:\n        pass\n",
    "%s:\n    pass\n\n",
    "%s:\n    pass\n\n\n\n\n",
    "%s:\n    pass\n    \n",
    "%s:\n    pass\n    \n\n\n\n",
    "%s:\n        pass",
    "%s:\n        pass\n",
    " %s:\n        pass\n",
    " %s:\n        pass\n\n",
    " %s:\n        pass\n\n\n\n\n",
    " %s:\n        pass\n     \n",
    " %s:\n        pass\n      \n\n\n\n",
]

@pytest.fixture(params=simple_body_starting_with_else)
def else_simple_body_starting_with_else(request):
    return request.param


def test_while_else_simple(else_simple_body_starting_with_else, has_else_member):
    red = RedBaron(has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_simple_body_starting_with_else % has_else_member[1])
    assert red.dumps() == "%s%s:\n    pass\n" % (has_else_member[0], has_else_member[1])


def test_while_else_simple_root_level(else_simple_body, has_else_member):
    red = RedBaron("%s\n\ndef other_stuff(): pass\n" % has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_simple_body)
    assert red.dumps() == "%s%s:\n    plop\n\n\ndef other_stuff(): pass\n" % (has_else_member[0], has_else_member[1])


def test_while_else_not_simple_root_level(else_simple_body_starting_with_else, has_else_member):
    red = RedBaron("%s\n\ndef other_stuff(): pass\n" % has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_simple_body_starting_with_else % has_else_member[1])
    assert red.dumps() == "%s%s:\n    pass\n\n\ndef other_stuff(): pass\n" % (has_else_member[0], has_else_member[1])


def test_while_else_root_level_too_few_blanks_lines(else_simple_body, has_else_member):
    red = RedBaron("%s\ndef other_stuff(): pass\n" % has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_simple_body)
    assert red.dumps() == "%s%s:\n    plop\n\n\ndef other_stuff(): pass\n" % (has_else_member[0], has_else_member[1])


def test_while_else_root_level_too_few_blanks_lines_starting_with_else(else_simple_body_starting_with_else, has_else_member):
    red = RedBaron("%s\ndef other_stuff(): pass\n" % has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_simple_body_starting_with_else % has_else_member[1])
    assert red.dumps() == "%s%s:\n    pass\n\n\ndef other_stuff(): pass\n" % (has_else_member[0], has_else_member[1])


def test_while_else_root_level_too_much_blanks_lines(else_simple_body, has_else_member):
    red = RedBaron("%s\ndef other_stuff(): pass\n" % has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_simple_body)
    assert red.dumps() == "%s%s:\n    plop\n\n\ndef other_stuff(): pass\n" % (has_else_member[0], has_else_member[1])


def test_while_else_root_level_too_much_blanks_lines_starting_with_else(else_simple_body_starting_with_else, has_else_member):
    red = RedBaron("%s\ndef other_stuff(): pass\n" % has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_simple_body_starting_with_else % has_else_member[1])
    assert red.dumps() == "%s%s:\n    pass\n\n\ndef other_stuff(): pass\n" % (has_else_member[0], has_else_member[1])


def test_while_else_root_level_too_much_blanks_lines_starting_two_line_body(else_two_line_body, has_else_member):
    red = RedBaron("%s\ndef other_stuff(): pass\n" % has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_two_line_body)
    assert red.dumps() == "%s%s:\n    plop\n    plouf\n\n\ndef other_stuff(): pass\n" % (has_else_member[0], has_else_member[1])


def test_while_else(else_simple_body, has_else_member):
    red = RedBaron("%s" % has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_simple_body)
    assert red.dumps() == "%s%s:\n    plop\n" % (has_else_member[0], has_else_member[1])


def test_while_else_two_line_body(else_two_line_body, has_else_member):
    red = RedBaron("%s" % has_else_member[0])
    setattr(red[0], has_else_member[1] + "_", else_two_line_body)
    assert red.dumps() == "%s%s:\n    plop\n    plouf\n" % (has_else_member[0], has_else_member[1])


code_else_block_setattr_one_level = """\
def pouet():
    %s
"""

code_else_block_setattr_one_level_result = """\
def pouet():
    %s
    %s:
        pass
"""


def test_while_else_setattr_one_level_simple_body(else_simple_body, has_else_member):
    result_keyword = has_else_member[1]
    has_else_member = "\n    ".join(has_else_member[0].split("\n")).rstrip()
    red = RedBaron(code_else_block_setattr_one_level % has_else_member)
    setattr(red[0].value.node_list[1], result_keyword, else_simple_body.replace("plop", "pass"))
    assert red.dumps() == code_else_block_setattr_one_level_result % (has_else_member, result_keyword)


def test_while_else_setattr_one_level_simple_body_start_with_else(else_simple_body_starting_with_else, has_else_member):
    result_keyword = has_else_member[1]
    has_else_member = "\n    ".join(has_else_member[0].split("\n")).rstrip()
    red = RedBaron(code_else_block_setattr_one_level % has_else_member)
    setattr(red[0].value.node_list[1], result_keyword, else_simple_body_starting_with_else % result_keyword)
    assert red.dumps() == code_else_block_setattr_one_level_result % (has_else_member, result_keyword)


code_else_block_setattr_one_level_followed = """\
def pouet():
    %s

    pass
"""

code_else_block_setattr_one_level_followed_result = """\
def pouet():
    %s
    %s:
        pass

    pass
"""


def test_while_else_setattr_one_level_simple_body_followed(else_simple_body, has_else_member):
    result_keyword = has_else_member[1]
    has_else_member = "\n    ".join(has_else_member[0].split("\n")).rstrip()
    red = RedBaron(code_else_block_setattr_one_level_followed % has_else_member)
    setattr(red[0].value.node_list[1], result_keyword, else_simple_body.replace("plop", "pass"))
    assert red.dumps() == code_else_block_setattr_one_level_followed_result % (has_else_member, result_keyword)


def test_while_else_setattr_one_level_simple_body_start_with_else_followed(else_simple_body_starting_with_else, has_else_member):
    result_keyword = has_else_member[1]
    has_else_member = "\n    ".join(has_else_member[0].split("\n")).rstrip()
    red = RedBaron(code_else_block_setattr_one_level_followed % has_else_member)
    setattr(red[0].value.node_list[1], result_keyword, else_simple_body_starting_with_else % result_keyword)
    assert red.dumps() == code_else_block_setattr_one_level_followed_result % (has_else_member, result_keyword)


def test_get_last_member_to_clean_while():
    red = RedBaron("while True: pass")
    assert red[0]._get_last_member_to_clean() is red[0]


def test_get_last_member_to_clean_for():
    red = RedBaron("for a in a: pass")
    assert red[0]._get_last_member_to_clean() is red[0]


def test_get_last_member_to_clean_try_except():
    red = RedBaron("try: pass\nexcept: pass")
    assert red[0]._get_last_member_to_clean() is red[0].excepts[-1]


def test_get_last_member_to_clean_try_excepts():
    red = RedBaron("try: pass\nexcept: pass\nexcept: pass")
    assert red[0]._get_last_member_to_clean() is red[0].excepts[-1]


def test_get_last_member_to_clean_try_else():
    red = RedBaron("try: pass\nexcept: pass\nelse: pass")
    assert red[0]._get_last_member_to_clean() is red[0].else_


def test_get_last_member_to_clean_try_finally():
    red = RedBaron("try: pass\nexcept: pass\nelse: pass\nfinally: pass")
    assert red[0]._get_last_member_to_clean() is red[0].finally_


def test_get_last_member_to_clean_try_else_finally():
    red = RedBaron("try: pass\nexcept: pass\nfinally: pass")
    assert red[0]._get_last_member_to_clean() is red[0].finally_


def test_get_last_member_to_clean_try_finally_only():
    red = RedBaron("try: pass\nfinally: pass")
    assert red[0]._get_last_member_to_clean() is red[0].finally_


def test_remove_else_setattr():
    red = RedBaron("while True: pass\nelse: pass\n")
    red[0].else_ = ""
    assert red.dumps() == "while True: pass\n"


def test_remove_else_setattr_followed():
    red = RedBaron("while True: pass\nelse: pass\n\n\nstuff")
    red[0].else_ = ""
    assert red.dumps() == "while True: pass\n\n\nstuff"


def test_remove_else_setattr_indented():
    red = RedBaron("def a():\n    while True: pass\n    else: pass\n")
    red.while_.else_ = ""
    assert red.dumps() == "def a():\n    while True: pass\n"


def test_remove_else_setattr_indented_followed():
    red = RedBaron("def a():\n    while True: pass\n    else: pass\n\n\n    stuff\n")
    red.while_.else_ = ""
    assert red.dumps() == "def a():\n    while True: pass\n\n\n    stuff\n"


def test_try_setattr_excepts():
    red = RedBaron("try:\n    pass\nfinally:\n    pass")
    red[0].excepts = "except:\n    pass\n"
    assert red.dumps() == "try:\n    pass\nexcept:\n    pass\nfinally:\n    pass\n"


def test_try_setattr_excepts_replace():
    red = RedBaron("try:\n    pass\nexcept:\n    pouet\n")
    red[0].excepts = "except:\n    pass\n"
    assert red.dumps() == "try:\n    pass\nexcept:\n    pass\n"


def test_try_setattr_excepts_remove():
    red = RedBaron("try:\n    pass\nexcept:\n    pass\nfinally:\n    pass\n")
    red[0].excepts = ""
    assert red.dumps() == "try:\n    pass\nfinally:\n    pass\n"


def test_try_setattr_excepts_indented_input():
    red = RedBaron("try:\n    pass\nfinally:\n    pass")
    red[0].excepts = "    except:\n        pass\n"
    assert red.dumps() == "try:\n    pass\nexcept:\n    pass\nfinally:\n    pass\n"


def test_try_setattr_excepts_replace_followed():
    red = RedBaron("try:\n    pass\nexcept:\n    pouet\n\n\nplop\n")
    red[0].excepts = "except:\n    pass\n"
    assert red.dumps() == "try:\n    pass\nexcept:\n    pass\n\n\nplop\n"


def test_try_setattr_excepts_replace_followed_strip():
    red = RedBaron("try:\n    pass\nexcept:\n    pouet\n\n\nplop\n")
    red[0].excepts = "except:\n    pass\n\n\n\n"
    assert red.dumps() == "try:\n    pass\nexcept:\n    pass\n\n\nplop\n"


def test_try_setattr_excepts_replace_strip():
    red = RedBaron("try:\n    pass\nexcept:\n    pouet\n")
    red[0].excepts = "except:\n    pass\n\n\n\n"
    assert red.dumps() == "try:\n    pass\nexcept:\n    pass\n"


def test_try_setattr_excepts_indented():
    red = RedBaron("def a():\n    try:\n        pass\n    finally:\n        pass")
    red.try_.excepts = "    except:\n        pass\n"
    assert red.dumps() == "def a():\n    try:\n        pass\n    except:\n        pass\n    finally:\n        pass\n"


def test_try_setattr_excepts_indented_replace():
    red = RedBaron("def a():\n    try:\n        pass\n    except:\n        pouet")
    red.try_.excepts = "    except:\n        pass\n"
    assert red.dumps() == "def a():\n    try:\n        pass\n    except:\n        pass\n"


def test_try_setattr_excepts_indented_replace_followed():
    red = RedBaron("def a():\n    try:\n        pass\n    except:\n        pouet\n\n    plop\n")
    red.try_.excepts = "    except:\n        pass\n"
    assert red.dumps() == "def a():\n    try:\n        pass\n    except:\n        pass\n\n    plop\n"


def test_ifelseblock_setattr():
    red = RedBaron("if a:\n    pass\n")
    red[0].value = "if 1 + 1:\n    qsd\n"
    assert red.dumps() == "if 1 + 1:\n    qsd\n"


def test_ifelseblock_setattr_input_indented():
    red = RedBaron("if a:\n    pass\n")
    red[0].value = "    if 1 + 1:\n        qsd\n"
    assert red.dumps() == "if 1 + 1:\n    qsd\n"


def test_ifelseblock_setattr_trailing():
    red = RedBaron("if a:\n    pass\n")
    red[0].value = "if 1 + 1:\n    qsd\n\n\n\n\n"
    assert red.dumps() == "if 1 + 1:\n    qsd\n"


def test_ifelseblock_setattr_followed():
    red = RedBaron("if a:\n    pass\n\n\npouet\n")
    red[0].value = "if 1 + 1:\n    qsd\n\n\n\n\n"
    assert red.dumps() == "if 1 + 1:\n    qsd\n\n\npouet\n"


def test_ifelseblock_setattr_indented():
    red = RedBaron("def a():\n    if a:\n        pass\n")
    red[0].value.node_list[1].value = "if 1 + 1:\n    qsd\n"
    assert red.dumps() == "def a():\n    if 1 + 1:\n        qsd\n"


def test_ifelseblock_setattr_indented_trailing():
    red = RedBaron("def a():\n    if a:\n        pass\n")
    red[0].value.node_list[1].value = "if 1 + 1:\n    qsd\n\n\n\n"
    assert red.dumps() == "def a():\n    if 1 + 1:\n        qsd\n"


def test_ifelseblock_setattr_indented_followed():
    red = RedBaron("def a():\n    if a:\n        pass\n\n\n    pouet\n")
    red[0].value.node_list[1].value = "if 1 + 1:\n    qsd\n"
    assert red.dumps() == "def a():\n    if 1 + 1:\n        qsd\n\n    pouet\n"
