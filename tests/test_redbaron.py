#!/usr/bin/python
# -*- coding:Utf-8 -*-


import pytest
from baron.utils import string_instance
from redbaron import (RedBaron, NodeList, truncate, CommaProxyList,
                      DotProxyList, LineProxyList, DecoratorsLineProxyList)

@pytest.fixture
def red():
    return RedBaron("""\
@deco
def a(c, d):
    b = c + d
""")


fst = red()
bounding_boxes = [
    (((1, 1),  (4, 0)),  ((1, 1), (4, 0)), fst),
    (((1, 1),  (4, 0)),  ((1, 1), (4, 0)), fst.def_),
    (((1, 1),  (2, 0)),  ((1, 1), (2, 0)), fst.def_.decorators.node_list),
    (((1, 1),  (1, 5)),  ((1, 1), (1, 5)), fst.def_.decorators.node_list[0]),
    (((1, 2),  (1, 5)),  ((1, 1), (1, 4)), fst.def_.decorators.node_list[0].value),
    (((1, 2),  (1, 5)),  ((1, 1), (1, 4)), fst.def_.decorators.node_list[0].value.value),
    (((1, 2),  (1, 5)),  ((1, 1), (1, 4)), fst.def_.decorators.node_list[0].value.value[0]),
    (((1, 6),  (2, 0)),  ((1, 1), (2, 0)), fst.def_.decorators.node_list[1]),
    (((2, 4),  (2, 4)),  ((1, 1), (1, 1)), fst.def_.first_formatting),
    (((2, 4),  (2, 4)),  ((1, 1), (1, 1)), fst.def_.first_formatting[0]),
    (((2, 6),  (2, 5)),  ((1, 1), (1, 0)), fst.def_.second_formatting),
    (((2, 7),  (2, 6)),  ((1, 1), (1, 0)), fst.def_.third_formatting),
    (((2, 7),  (2, 10)), ((1, 1), (1, 4)), fst.def_.arguments),
    (((2, 7),  (2, 7)),  ((1, 1), (1, 1)), fst.def_.arguments.node_list[0]),
    (((2, 8),  (2, 9)),  ((1, 1), (1, 2)), fst.def_.arguments.node_list[1]),
    (((2, 10), (2, 10)), ((1, 1), (1, 1)), fst.def_.arguments.node_list[2]),
    (((2, 11), (2, 10)), ((1, 1), (1, 0)), fst.def_.fourth_formatting),
    (((2, 12), (2, 11)), ((1, 1), (1, 0)), fst.def_.fifth_formatting),
    (((2, 13), (2, 12)), ((1, 1), (1, 0)), fst.def_.sixth_formatting),
    (((2, 13), (4, 0)),  ((1, 1), (3, 0)), fst.def_.value),
    (((2, 13), (3, 4)),  ((1, 1), (2, 4)), fst.def_.value.node_list[0]),
    (((3, 5),  (3, 13)), ((1, 1), (1, 9)), fst.def_.value.node_list[1]),
    (((3, 5),  (3, 5)),  ((1, 1), (1, 1)), fst.def_.value.node_list[1].target),
    (((3, 9),  (3, 13)), ((1, 1), (1, 5)), fst.def_.value.node_list[1].value),
    (((3, 9),  (3, 9)),  ((1, 1), (1, 1)), fst.def_.value.node_list[1].value.first),
    (((3, 13), (3, 13)), ((1, 1), (1, 1)), fst.def_.value.node_list[1].value.second),
    (((3, 14), (4, 0)),  ((1, 1), (2, 0)), fst.def_.value.node_list[2])
]

@pytest.fixture(params = bounding_boxes)
def bounding_box_fixture(request):
    return request.param

def test_bounding_box(red, bounding_box_fixture):
    absolute_bounding_box, bounding_box, node = bounding_box_fixture
    assert bounding_box == node.bounding_box
    assert absolute_bounding_box == node.absolute_bounding_box


def test_bounding_box_of_attribute(red):
    assert ((2, 1), (2, 3)) == red.def_.get_absolute_bounding_box_of_attribute("def")


def test_bounding_box_of_attribute_no_attribute(red):
    with pytest.raises(KeyError):
        red.def_.get_absolute_bounding_box_of_attribute("xxx")


def test_bounding_box_of_attribute_no_index(red):
    with pytest.raises(IndexError):
        red.get_absolute_bounding_box_of_attribute(1)

    with pytest.raises(IndexError):
        red.get_absolute_bounding_box_of_attribute(-1)


def test_bounding_box_empty():
    red = RedBaron("a()")
    assert ((1, 3), (1, 2)) == red.atomtrailers.value[1].value.absolute_bounding_box

fst = RedBaron("""\
@deco

def a(c, d):
    b = c + d
    e = 1
""")

positions = [
    (fst.def_.decorators[0],                       [(1, 1)]),
    (fst.def_.decorators[0].value.value[0],        [(1, 2), (1, 3), (1, 4), (1, 5)]),
    # How to get this one ? (2, 0) and (2, 1) does not work, see out of scope
    #(fst.def_.decorators[1],                       [(?, ?)]),
    (fst.def_,                                     [(3, 1), (3, 2), (3, 3)]),
    (fst.def_.first_formatting[0],                 [(3, 4)]),
    (fst.def_,                                     [(3, 5), (3, 6)]),
    (fst.def_.arguments.node_list[0].target,                 [(3, 7)]),
    (fst.def_.arguments.node_list[1],                        [(3, 8)]),
    (fst.def_.arguments.node_list[1].second_formatting[0],   [(3, 9)]),
    (fst.def_.arguments.node_list[2].target,                 [(3, 10)]),
    (fst.def_,                                     [(3, 11), (3, 12)]),
    (fst.def_.value.node_list[0],                            [(4, 1), (4, 2), (4, 3), (4, 4)]),
    (fst.def_.value.node_list[1].target,                     [(4, 5)]),
    (fst.def_.value.node_list[1].first_formatting[0],        [(4, 6)]),
    (fst.def_.value.node_list[1],                            [(4, 7)]),
    (fst.def_.value.node_list[1].second_formatting[0],       [(4, 8)]),
    (fst.def_.value.node_list[1].value.first,                [(4, 9)]),
    (fst.def_.value.node_list[1].value.first_formatting[0],  [(4, 10)]),
    (fst.def_.value.node_list[1].value,                      [(4, 11)]),
    (fst.def_.value.node_list[1].value.second_formatting[0], [(4, 12)]),
    (fst.def_.value.node_list[1].value.second,               [(4, 13)]),
    (fst.def_.value.node_list[2],                            [(5, 1), (5, 2), (5, 3), (5, 4)]),
    (fst.def_.value.node_list[3].target,                     [(5, 5)]),
    (fst.def_.value.node_list[3].first_formatting[0],        [(5, 6)]),
    (fst.def_.value.node_list[3],                            [(5, 7)]),
    (fst.def_.value.node_list[3].second_formatting[0],       [(5, 8)]),
    (fst.def_.value.node_list[3].value,                      [(5, 9)]),
    # out of scope
    (fst,                                             [(2, 0),  (2, 1)]),
]


@pytest.fixture(params = positions)
def position_fixture(request):
    return request.param

def test_find_by_position(position_fixture):
    node, positions = position_fixture
    for position in positions:
        assert node == fst.find_by_position(position)

def test_other_name_assignment():
    red = RedBaron("a = b")
    assert red.assign is red[0]


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


def test_index():
    red = RedBaron("a = [1, 2, 3]")
    assert red[0].value.value.node_list[2].index_on_parent == 2
    assert red[0].index_on_parent == 0
    assert red[0].value.index_on_parent is None


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


def test_regression_find_all_recursive():
    red = RedBaron("a.b()")
    assert red[0].value("name", recursive=False) == [red.name, red("name")[1]]


def test_truncate():
    assert "1234" == truncate("1234", 2)
    assert "12345" == truncate("12345", 4)
    assert "1...6" == truncate("123456", 5)
    assert "123456...0" == truncate("12345678901234567890", 10)


def test_comma_proxy_list_len_empty():
    red = RedBaron("[]")
    comma_proxy_list = red[0].value
    assert len(comma_proxy_list) == 0


def test_comma_proxy_list_len_not_empty():
    red = RedBaron("[1, 2, 3]")
    comma_proxy_list = red[0].value
    assert len(comma_proxy_list) == 3


def test_comma_proxy_list_insert():
    red = RedBaron("[]")
    comma_proxy_list = red[0].value
    comma_proxy_list.insert(0, "1")
    assert red.dumps() == "[1]"


def test_comma_proxy_list_insert_2_at_top():
    red = RedBaron("[1]")
    comma_proxy_list = red[0].value
    comma_proxy_list.insert(0, "2")
    assert red.dumps() == "[2, 1]"


def test_comma_proxy_list_insert_2():
    red = RedBaron("[1]")
    comma_proxy_list = red[0].value
    comma_proxy_list.insert(1, "2")
    assert red.dumps() == "[1, 2]"


def test_comma_proxy_list_insert_2_middle():
    red = RedBaron("[1, 3]")
    comma_proxy_list = red[0].value
    comma_proxy_list.insert(1, "2")
    assert red.dumps() == "[1, 2, 3]"


def test_comma_proxy_list_append():
    red = RedBaron("[]")
    comma_proxy_list = red[0].value
    comma_proxy_list.append("1")
    assert red.dumps() == "[1]"


def test_comma_proxy_list_append_2():
    red = RedBaron("[1]")
    comma_proxy_list = red[0].value
    comma_proxy_list.append("2")
    assert red.dumps() == "[1, 2]"


def test_comma_proxy_list_append_3():
    red = RedBaron("[1, 2]")
    comma_proxy_list = red[0].value
    comma_proxy_list.append("3")
    assert red.dumps() == "[1, 2, 3]"


def test_comma_proxy_list_pop():
    red = RedBaron("[1]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop(0)
    assert red.dumps() == "[]"


def test_comma_proxy_list_pop_2_at_top():
    red = RedBaron("[2, 1]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop(0)
    assert red.dumps() == "[1]"


def test_comma_proxy_list_pop_2():
    red = RedBaron("[1, 2]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop(1)
    assert red.dumps() == "[1]"


def test_comma_proxy_list_pop_2_middle():
    red = RedBaron("[1, 2, 3]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop(1)
    assert red.dumps() == "[1, 3]"


def test_comma_proxy_list_pop_no_index():
    red = RedBaron("[1, 2, 3]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop()
    assert red.dumps() == "[1, 2]"


def test_comma_proxy_list_del():
    red = RedBaron("[1]")
    comma_proxy_list = red[0].value
    del comma_proxy_list[0]
    assert red.dumps() == "[]"


def test_comma_proxy_list_del_2_at_top():
    red = RedBaron("[2, 1]")
    comma_proxy_list = red[0].value
    del comma_proxy_list[0]
    assert red.dumps() == "[1]"


def test_comma_proxy_list_del_2():
    red = RedBaron("[1, 2]")
    comma_proxy_list = red[0].value
    del comma_proxy_list[1]
    assert red.dumps() == "[1]"


def test_comma_proxy_list_del_2_middle():
    red = RedBaron("[1, 2, 3]")
    comma_proxy_list = red[0].value
    del comma_proxy_list[1]
    assert red.dumps() == "[1, 3]"


def test_comma_proxy_list_remove():
    red = RedBaron("[1]")
    comma_proxy_list = red[0].value
    comma_proxy_list.remove(comma_proxy_list[0])
    assert red.dumps() == "[]"


def test_comma_proxy_list_remove_2_at_top():
    red = RedBaron("[2, 1]")
    comma_proxy_list = red[0].value
    comma_proxy_list.remove(comma_proxy_list[0])
    assert red.dumps() == "[1]"


def test_comma_proxy_list_remove_2():
    red = RedBaron("[1, 2]")
    comma_proxy_list = red[0].value
    comma_proxy_list.remove(comma_proxy_list[1])
    assert red.dumps() == "[1]"


def test_comma_proxy_list_remove_2_middle():
    red = RedBaron("[1, 2, 3]")
    comma_proxy_list = red[0].value
    comma_proxy_list.remove(comma_proxy_list[1])
    assert red.dumps() == "[1, 3]"


def test_comma_proxy_list_set_item():
    red = RedBaron("[1]")
    comma_proxy_list = red[0].value
    comma_proxy_list[0] = "42"
    assert comma_proxy_list[0].type == "int"
    assert comma_proxy_list[0].value == 42
    comma_proxy_list[0] = "plop"
    assert comma_proxy_list[0].type == "name"
    assert comma_proxy_list[0].value == "plop"
    assert red.dumps() == "[plop]"


def test_comma_proxy_list_set_slice():
    red = RedBaron("[1, 2, 3]")
    comma_proxy_list = red[0].value
    comma_proxy_list[1:2] = ["42", "31", "23"]
    assert red.dumps() == "[1, 42, 31, 23, 3]"


def test_comma_proxy_list_delslice():
    red = RedBaron("[1, 2, 3, 4, 5, 6]")
    comma_proxy_list = red[0].value
    del comma_proxy_list[1:4]
    assert red.dumps() == "[1, 5, 6]"


def test_comma_proxy_list_getslice():
    red = RedBaron("[1, 2, 3, 4, 5, 6]")
    comma_proxy_list = red[0].value
    result = comma_proxy_list[1:2]
    expected_result = CommaProxyList(NodeList([comma_proxy_list[1]]))
    assert len(result) == len(expected_result)
    assert result[0] == expected_result[0]


def test_comma_proxy_list_on_attribute_default_on_value():
    # this is only for testing, the correct on_attribute is "value"
    red = RedBaron("[]")
    comma_proxy_list = red[0].value
    comma_proxy_list.append("1")
    assert comma_proxy_list[0].on_attribute == "value"


def test_comma_proxy_list_on_attribute():
    # this is only for testing, the correct on_attribute is "value"
    red = RedBaron("[]")
    comma_proxy_list = CommaProxyList(red[0].value.node_list, on_attribute="plop")
    comma_proxy_list.append("1")
    comma_proxy_list.append("1")
    assert comma_proxy_list[0].on_attribute == "plop"
    assert comma_proxy_list[1].on_attribute == "plop"
    assert comma_proxy_list.node_list[1].on_attribute == "plop"


def test_comma_proxy_list_extend():
    red = RedBaron("[]")
    comma_proxy_list = red[0].value
    comma_proxy_list.extend(["1"])
    assert red.dumps() == "[1]"


def test_comma_proxy_list_extend_2():
    red = RedBaron("[1]")
    comma_proxy_list = red[0].value
    comma_proxy_list.extend(["2", "plop", "42"])
    assert red.dumps() == "[1, 2, plop, 42]"


def test_comma_proxy_list_extend_3():
    red = RedBaron("[1, 2]")
    comma_proxy_list = red[0].value
    comma_proxy_list.extend(["3"])
    assert red.dumps() == "[1, 2, 3]"


def test_comma_proxy_list_dictionary():
    red = RedBaron("{1: 2}")
    # no assert, will fail if parsing is not good
    red[0].value.append("3: 4")


def test_comma_proxy_list_call():
    red = RedBaron("a(b)")
    red[0].value[1].value.append("**kwargs")
    assert red.dumps() == "a(b, **kwargs)"


def test_comma_proxy_list_class_inherit():
    red = RedBaron("class A(): pass")
    red[0].inherit_from.append("plop")
    assert red.dumps() == "class A(plop): pass\n"


def test_comma_proxy_list_from_import_targets():
    red = RedBaron("from a.b import c as d")
    red[0].targets.append("e")
    red[0].targets.append("f as g")
    assert red.dumps() == "from a.b import c as d, e, f as g"


def test_comma_proxy_list_def_arguments():
    red = RedBaron("def a(b): pass")
    red[0].arguments.append("**kwargs")
    assert red.dumps() == "def a(b, **kwargs): pass\n"


def test_comma_proxy_list_global_value():
    red = RedBaron("global a")
    red[0].value.append("b")
    assert red.dumps() == "global a, b"


def test_comma_proxy_list_import_value():
    red = RedBaron("import a")
    red[0].value.append("b.c.d as e")
    assert red.dumps() == "import a, b.c.d as e"


def test_comma_proxy_list_lambda_arguments():
    red = RedBaron("lambda x: 1 + 1")
    red[0].arguments.append("**kwargs")
    assert red.dumps() == "lambda x, **kwargs: 1 + 1"


def test_comma_proxy_list_print_value():
    red = RedBaron("print a")
    red[0].value.append("plop")
    assert red.dumps() == "print a, plop"


def test_comma_proxy_list_repr_value():
    red = RedBaron("`a`")
    red[0].value.append("plop")
    assert red.dumps() == "`a, plop`"


def test_comma_proxy_list_with_contexts():
    red = RedBaron("with a: pass")
    red[0].contexts.append("b as c")
    assert red.dumps() == "with a, b as c: pass\n"


def test_comma_proxy_list_delegation_from_parent_node_on_value():
    red = RedBaron("{1: 2}")
    # you don't need to do a .value here!
    red[0].append("3: 4")
    assert red.dumps() == "{1: 2, 3: 4}"


def test_comma_proxy_list_delegation_from_parent_node_on_value_getitem():
    red = RedBaron("{1: 2}")
    # you don't need to do a .value here!
    red[0][0]


def test_comma_proxy_list_delegation_from_parent_node_on_value_setitem():
    red = RedBaron("{1: 2}")
    # you don't need to do a .value here!
    red[0].append("3: 4")
    red[0][1] = "42: plop"
    assert red.dumps() == "{1: 2, 42: plop}"


def test_comma_proxy_list_delegation_from_parent_node_on_value_insert():
    red = RedBaron("[]")
    red[0].insert(0, "caramba")


def test_comma_proxy_list_delegation_from_parent_node_on_value_extend():
    red = RedBaron("[]")
    red[0].extend(["3", "42"])


def test_comma_proxy_list_delegation_from_parent_node_on_value_pop():
    red = RedBaron("[42]")
    red[0].pop()


def test_comma_proxy_list_delegation_from_parent_node_on_value_remove():
    red = RedBaron("[pouet]")
    red[0].remove(red[0][0])


def test_comma_proxy_list_delegation_from_parent_node_on_value_index():
    red = RedBaron("[42]")
    assert red[0].index(red[0][0]) == 0


def test_comma_proxy_list_delegation_from_parent_node_on_value_len():
    red = RedBaron("[pouf]")
    assert len(red[0]) == 1


def test_comma_proxy_list_delegation_from_parent_node_on_value_del():
    red = RedBaron("[abc, zop]")
    del red[0][0]
    assert len(red[0]) == 1


def test_comma_proxy_list_delegation_from_parent_node_on_value_contains():
    red = RedBaron("[a, b, c]")
    assert red[0][0] in red[0]


def test_comma_proxy_list_delegation_from_parent_node_on_value_iter():
    red = RedBaron("[42]")
    assert [x.value for x in red[0]] == [42]


def test_comma_proxy_list_delegation_from_parent_node_on_value_count():
    red = RedBaron("[pouet]")
    assert red[0].count(red[0][0]) == 1


def test_comma_proxy_list_delegation_from_parent_node_on_value_setslice():
    red = RedBaron("[]")
    red[0][1:1] = ["pouet", "plop"]


def test_comma_proxy_list_delegation_from_parent_node_on_value_delslice():
    red = RedBaron("[pif, paf, pouf]")
    del red[0][1:2]


def test_comma_proxy_list_delegation_from_parent_node_on_value_getslice():
    red = RedBaron("[plop, pouet]")
    assert isinstance(red[0][1:1], CommaProxyList)


def test_dot_proxy_list_len():
    red = RedBaron("a.b.c")
    assert len(red[0].value) == 3


def test_dot_proxy_list_insert():
    red = RedBaron("a.b")
    red[0].value.insert(0, "c")
    assert red.dumps() == "c.a.b"


def test_dot_proxy_list_insert_2_at_top():
    red = RedBaron("a.b")
    red[0].value.insert(2, "c")
    assert red.dumps() == "a.b.c"


def test_dot_proxy_list_append():
    red = RedBaron("a.b")
    red[0].value.append("c")
    assert red.dumps() == "a.b.c"


def test_dot_proxy_list_pop():
    red = RedBaron("a.b.c.d")
    red[0].value.pop(0)
    assert red.dumps() == "b.c.d"


def test_dot_proxy_list_pop_2():
    red = RedBaron("a.b.c")
    red[0].value.pop(1)
    assert red.dumps() == "a.c"


def test_dot_proxy_list_pop_no_index():
    red = RedBaron("a.b.c")
    red[0].value.pop()
    assert red.dumps() == "a.b"


def test_dot_proxy_list_del():
    red = RedBaron("a.b.c")
    del red[0].value[0]
    assert red.dumps() == "b.c"


def test_dot_proxy_list_del_2():
    red = RedBaron("a.b.c")
    del red[0].value[1]
    assert red.dumps() == "a.c"


def test_dot_proxy_list_remove():
    red = RedBaron("a.b.c")
    red[0].value.remove(red[0].value[0])
    assert red.dumps() == "b.c"


def test_dot_proxy_list_remove_2():
    red = RedBaron("a.b.c")
    red[0].value.remove(red[0].value[1])
    assert red.dumps() == "a.c"


def test_dot_proxy_list_set_item():
    red = RedBaron("a.b.c")
    red[0].value[0] = "plop"
    assert red[0].value[0].type == "name"
    assert red[0].value[0].value == "plop"
    assert red.dumps() == "plop.b.c"


def test_dot_proxy_list_set_slice():
    red = RedBaron("a.b.c")
    red[0].value[1:2] = ["caramba", "compote"]
    assert red.dumps() == "a.caramba.compote.c"


def test_dot_proxy_list_delslice():
    red = RedBaron("a.b.c.d.e.f")
    del red[0].value[1:4]
    assert red.dumps() == "a.e.f"


def test_dot_proxy_list_getslice():
    red = RedBaron("a.b.c.d")
    result = red[0].value[1:3]
    expected_result = DotProxyList(NodeList([red[0].value[1], red[0].value[2]]))
    assert len(result) == len(expected_result)
    assert result[0] == expected_result[0]


def test_dot_proxy_list_extend():
    red = RedBaron("a.b.c")
    red[0].value.extend(["zob"])
    assert red.dumps() == "a.b.c.zob"


def test_dot_proxy_list_extend_2():
    red = RedBaron("a.b.c")
    red[0].value.extend(["f", "plop", "ss"])
    assert red.dumps() == "a.b.c.f.plop.ss"


def test_dot_proxy_list_append_call():
    red = RedBaron("a.b")
    red[0].value.append("()")
    assert red.dumps() == "a.b()"


def test_dot_proxy_list_dotted_name_as_name():
    red = RedBaron("import a.b as c")
    red[0][0].append("plop")
    assert red.dumps() == "import a.b.plop as c"


def test_dot_proxy_list_from_import_node():
    red = RedBaron("from a.b.c import d")
    red[0].append("plop")
    assert red.dumps() == "from a.b.c.plop import d"


def test_dot_proxy_list_append_getitem():
    red = RedBaron("a.b")
    red[0].value.append("[stuff]")
    assert red.dumps() == "a.b[stuff]"


def test_dot_proxy_list_dotted_name_as_name_heading_dots():
    red = RedBaron("import .a.b")
    red[0][0].append("plop")
    assert red.dumps() == "import .a.b.plop"


def test_dot_proxy_list_dotted_name_as_name_heading_dots_remove():
    red = RedBaron("import .a.b")
    red[0][0].pop()
    assert red.dumps() == "import .a"


def test_dot_proxy_list_dotted_name_as_name_heading_two_dots_remove():
    red = RedBaron("import ..a.b")
    red[0][0].pop()
    assert red.dumps() == "import ..a"


def test_dot_proxy_list_dotted_name_as_name_heading_two_dots_remove_first():
    red = RedBaron("import ..a.b")
    red[0][0].pop(0)
    assert red.dumps() == "import ..b"


def test_line_proxy_list_len():
    red = RedBaron("while a:\n    pass\n")
    assert len(red[0].value) == 1


def test_line_proxy_list_insert():
    red = RedBaron("while a:\n    pass\n")
    red[0].value.insert(0, "c")
    assert red.dumps() == "while a:\n    c\n    pass\n"


def test_line_proxy_list_insert_2_at_top():
    red = RedBaron("while a:\n    pass\n")
    red[0].value.insert(1, "c")
    assert red.dumps() == "while a:\n    pass\n    c\n"


def test_line_proxy_list_insert_2_at_middle():
    red = RedBaron("while a:\n    pass\n    pass\n")
    red[0].value.insert(1, "c")
    assert red.dumps() == "while a:\n    pass\n    c\n    pass\n"


def test_line_proxy_list_append():
    red = RedBaron("while a:\n    pass\n")
    red[0].value.append("c")
    assert red.dumps() == "while a:\n    pass\n    c\n"


def test_line_proxy_list_pop():
    red = RedBaron("while a:\n    c\n    pass\n")
    red[0].value.pop(0)
    assert red.dumps() == "while a:\n    pass\n"


def test_line_proxy_list_pop_2():
    red = RedBaron("while a:\n    pass\n    c\n    pass\n")
    red[0].value.pop(1)
    assert red.dumps() == "while a:\n    pass\n    pass\n"


def test_line_proxy_list_pop_no_index():
    red = RedBaron("while a:\n    pass\n    c\n    pass\n")
    red[0].value.pop()
    assert red.dumps() == "while a:\n    pass\n    c\n"


def test_line_proxy_list_del():
    red = RedBaron("while a:\n    pass\n    c\n    pass\n")
    del red[0].value[0]
    assert red.dumps() == "while a:\n    c\n    pass\n"


def test_line_proxy_list_del_2():
    red = RedBaron("while a:\n    pass\n    c\n    pass\n")
    del red[0].value[2]
    assert red.dumps() == "while a:\n    pass\n    c\n"


def test_line_proxy_list_remove():
    red = RedBaron("while a:\n    pass\n    c\n")
    red[0].value.remove(red[0].value[0])
    assert red.dumps() == "while a:\n    c\n"


def test_line_proxy_list_remove_2():
    red = RedBaron("while a:\n    pass\n    c\n")
    red[0].value.remove(red[0].value[1])
    assert red.dumps() == "while a:\n    pass\n"


def test_line_proxy_list_set_item():
    red = RedBaron("while a:\n    pass\n")
    red[0].value[0] = "plop"
    assert red[0].value[0].type == "name"
    assert red[0].value[0].value == "plop"
    assert red.dumps() == "while a:\n    plop\n"


def test_line_proxy_list_set_slice():
    red = RedBaron("while a:\n    pass\n    a\n    plop\n    z\n")
    red[0].value[1:2] = ["caramba", "compote"]
    assert red.dumps() == "while a:\n    pass\n    caramba\n    compote\n    plop\n    z\n"


def test_line_proxy_list_delslice():
    red = RedBaron("while a:\n    pass\n    caramba\n    compote\n    plop\n    z\n")
    del red[0].value[1:4]
    assert red.dumps() == "while a:\n    pass\n    z\n"


def test_line_proxy_list_getslice():
    red = RedBaron("while a:\n    pass\n    caramba\n    compote\n    plop\n    z\n")
    result = red[0].value[1:3]
    expected_result = LineProxyList(NodeList([red[0].value[1], red[0].value[2]]))
    assert len(result) == len(expected_result)
    assert result[0] == expected_result[0]


def test_line_proxy_list_extend():
    red = RedBaron("while a:\n    pass\n")
    red[0].value.extend(["zob"])
    assert red.dumps() == "while a:\n    pass\n    zob\n"


def test_line_proxy_list_extend_2():
    red = RedBaron("while a:\n    pass\n")
    red[0].value.extend(["f", "plop", "ss"])
    assert red.dumps() == "while a:\n    pass\n    f\n    plop\n    ss\n"


def test_line_proxy_list_different_indentation():
    red = RedBaron("while a:\n      pass\n")
    red[0].value.append("c")
    assert red.dumps() == "while a:\n      pass\n      c\n"


forwarded_indented_code = """
class A():
    while b:
        pass
    while c:
        pass
"""

forwarded_indented_code_result = """
class A():
    while b:
        pass
        plop
    while c:
        pass
"""

def test_line_proxy_dont_break_next_block_identation():
    red = RedBaron(forwarded_indented_code)
    red.while_.append("plop")
    assert red.dumps() == forwarded_indented_code_result


def test_line_proxy_with_blank_line_list_len():
    red = RedBaron("while a:\n    pass\n\n    plop\n")
    assert len(red[0].value) == 3


def test_line_proxy_with_blank_line_list_insert():
    red = RedBaron("while a:\n    pass\n\n    plop\n")
    red[0].value.insert(1, "c")
    assert red.dumps() == "while a:\n    pass\n    c\n\n    plop\n"


def test_line_proxy_with_blank_line_list_insert_2_at_middle():
    red = RedBaron("while a:\n    pass\n\n    plop\n    pass\n")
    red[0].value.insert(1, "c")
    assert red.dumps() == "while a:\n    pass\n    c\n\n    plop\n    pass\n"


def test_line_proxy_with_blank_line_list_append():
    red = RedBaron("while a:\n    pass\n\n")
    red[0].value.append("c")
    assert red.dumps() == "while a:\n    pass\n\n    c\n"


def test_line_proxy_with_blank_line_list_pop_blank_line():
    red = RedBaron("while a:\n    pass\n    qsd\n\n    plop\n    c\n    pass\n")
    red[0].value.pop(2)
    assert red.dumps() == "while a:\n    pass\n    qsd\n    plop\n    c\n    pass\n"


def test_line_proxy_with_blank_line_list_pop():
    red = RedBaron("while a:\n    pass\n\n    plop\n    c\n    pass\n")
    red[0].value.pop()
    assert red.dumps() == "while a:\n    pass\n\n    plop\n    c\n"


def test_line_proxy_with_blank_line_list_pop_2():
    red = RedBaron("while a:\n    pass\n\n    pass\n    pass\n")
    red[0].value.pop(0)
    assert red.dumps() == "while a:\n\n    pass\n    pass\n"


def test_line_proxy_with_blank_line_list_del():
    red = RedBaron("while a:\n    pass\n\n    plop\n    c\n    pass\n")
    del red[0].value[0]
    assert red.dumps() == "while a:\n\n    plop\n    c\n    pass\n"


def test_line_proxy_with_blank_line_list_del_blank_line():
    red = RedBaron("while a:\n    pass\n\n    plop\n    c\n    pass\n")
    del red[0].value[1]
    assert red.dumps() == "while a:\n    pass\n    plop\n    c\n    pass\n"


def test_line_proxy_with_blank_line_list_remove():
    red = RedBaron("while a:\n    pass\n\n    plop\n    c\n    pass\n")
    red[0].value.remove(red[0].value[0])
    assert red.dumps() == "while a:\n\n    plop\n    c\n    pass\n"


def test_line_proxy_with_blank_line_list_remove_2():
    red = RedBaron("while a:\n    pass\n\n    plop\n    c\n    pass\n")
    red[0].value.remove(red[0].value[1])
    assert red.dumps() == "while a:\n    pass\n    plop\n    c\n    pass\n"


def test_line_proxy_with_blank_line_list_set_slice():
    red = RedBaron("while a:\n    pass\n\n    plop\n    a\n    plop\n    z\n")
    red[0].value[1:2] = ["caramba", "compote"]
    assert red.dumps() == "while a:\n    pass\n    caramba\n    compote\n    plop\n    a\n    plop\n    z\n"


def test_line_proxy_with_blank_line_list_delslice():
    red = RedBaron("while a:\n    pass\n\n    plop\n    caramba\n    compote\n    plop\n    z\n")
    del red[0].value[1:4]
    assert red.dumps() == "while a:\n    pass\n    compote\n    plop\n    z\n"


def test_line_proxy_with_blank_line_list_getslice():
    red = RedBaron("while a:\n    pass\n\n    plop\n    caramba\n    compote\n    plop\n    z\n")
    result = red[0].value[1:3]
    expected_result = LineProxyList(NodeList([red[0].value[1], red[0].value[2]]))
    assert len(result) == len(expected_result)
    assert result[0] == expected_result[0]


def test_line_proxy_with_blank_line_list_extend():
    red = RedBaron("while a:\n    pass\n\n    plop\n")
    red[0].value.extend(["zob"])
    assert red.dumps() == "while a:\n    pass\n\n    plop\n    zob\n"


def test_line_proxy_with_blank_line_list_different_indentation():
    red = RedBaron("while a:\n        pass\n\n        plop\n")
    red[0].value.append("c")
    assert red.dumps() == "while a:\n        pass\n\n        plop\n        c\n"


forwarded_indented_code = """
class A():
    while b:
        pass

        pass
    while c:
        pass
"""

forwarded_indented_code_result = """
class A():
    while b:
        pass

        pass
        plop
    while c:
        pass
"""

def test_line_proxy_with_blank_line_dont_break_next_block_identation():
    red = RedBaron(forwarded_indented_code)
    red.while_.append("plop")
    assert red.dumps() == forwarded_indented_code_result


def test_line_proxy_with_blank_line_class_node():
    red = RedBaron("class A:\n    pass\n\n    plop\n")
    assert len(red[0].value) == 3


def test_line_proxy_with_blank_line_elif_node():
    red = RedBaron("if a:\n    pass\nelif A:\n    pass\n\n    plop\n")
    assert len(red[0].value[1].value) == 3


def test_line_proxy_with_blank_line_else_node():
    red = RedBaron("if a:\n    pass\nelse:\n    pass\n\n    plop\n")
    assert len(red[0].value[1].value) == 3


def test_line_proxy_with_blank_line_except_node():
    red = RedBaron("try:\n    pass\nexcept:\n    pass\n\n    plop\n")
    assert len(red[0].excepts[0].value) == 3


def test_line_proxy_with_blank_line_finally_node():
    red = RedBaron("try:\n    pass\nfinally:\n    pass\n\n    plop\n")
    assert len(red[0].finally_.value) == 3


def test_regression_print_empty_proxy_list():
    red = RedBaron("a = {}")
    print(red)


def test_regression_tuple_proxy_list_append():
    red = RedBaron("(1, 2)")
    red[0].append("3")


def test_regression_help_proxy_list():
    red = RedBaron("(1, 2)")
    red[0].value.node_list.help()


def test_comma_proxy_list_indented_len_not_empty():
    red = RedBaron("[\n    1,\n    2,\n    3,\n]")
    comma_proxy_list = red[0].value
    assert len(comma_proxy_list) == 3


def test_comma_proxy_list_detect_style():
    red = RedBaron("[1, 2, 3]")
    comma_proxy_list = red[0].value
    assert comma_proxy_list.style == "flat"


def test_comma_proxy_list_indented_detect_style():
    red = RedBaron("[\n    1,\n    2,\n    3,\n]")
    comma_proxy_list = red[0].value
    assert comma_proxy_list.style == "indented"


def test_comma_proxy_list_indented_insert():
    red = RedBaron("[]")
    comma_proxy_list = red[0].value
    comma_proxy_list.style = "indented"
    comma_proxy_list.insert(0, "1")
    assert red.dumps() == "[\n    1,\n]"


def test_comma_proxy_list_indented_insert_2_at_top():
    red = RedBaron("[\n    1,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.insert(0, "2")
    assert red.dumps() == "[\n    2,\n    1,\n]"


def test_comma_proxy_list_indented_insert_2():
    red = RedBaron("[\n    1,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.insert(1, "2")
    assert comma_proxy_list.style == "indented"
    assert red.dumps() == "[\n    1,\n    2,\n]"


def test_comma_proxy_list_indented_insert_2_middle():
    red = RedBaron("[\n    1,\n    3,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.insert(1, "2")
    assert red.dumps() == "[\n    1,\n    2,\n    3,\n]"


def test_comma_proxy_list_indented_append():
    red = RedBaron("[]")
    comma_proxy_list = red[0].value
    comma_proxy_list.style = "indented"
    comma_proxy_list.append("1")
    assert red.dumps() == "[\n    1,\n]"


def test_comma_proxy_list_indented_append_2():
    red = RedBaron("[\n    1,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.append("2")
    assert red.dumps() == "[\n    1,\n    2,\n]"


def test_comma_proxy_list_indented_pop():
    red = RedBaron("[\n    1,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop(0)
    assert red.dumps() == "[]"


def test_comma_proxy_list_indented_pop_2_at_top():
    red = RedBaron("[\n    2,\n    1,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop(0)
    assert red.dumps() == "[\n    1,\n]"


def test_comma_proxy_list_indented_pop_2():
    red = RedBaron("[\n    1,\n    2,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop(1)
    assert red.dumps() == "[\n    1,\n]"


def test_comma_proxy_list_indented_pop_2_middle():
    red = RedBaron("[\n    1,\n    2,\n    3,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop(1)
    assert red.dumps() == "[\n    1,\n    3,\n]"


def test_comma_proxy_list_indented_pop_no_index():
    red = RedBaron("[\n    1,\n    2,\n    3,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.pop()
    assert red.dumps() == "[\n    1,\n    2,\n]"


def test_comma_proxy_list_indented_del():
    red = RedBaron("[\n    1,\n]")
    comma_proxy_list = red[0].value
    del comma_proxy_list[0]
    assert red.dumps() == "[]"


def test_comma_proxy_list_indented_del_2_at_top():
    red = RedBaron("[\n    2,\n    1,\n]")
    comma_proxy_list = red[0].value
    del comma_proxy_list[0]
    assert red.dumps() == "[\n    1,\n]"


def test_comma_proxy_list_indented_remove():
    red = RedBaron("[\n    1,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.remove(comma_proxy_list[0])
    assert red.dumps() == "[]"


def test_comma_proxy_list_indented_remove_2_at_top():
    red = RedBaron("[\n    2,\n    1,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list.remove(comma_proxy_list[0])
    assert red.dumps() == "[\n    1,\n]"


def test_comma_proxy_list_indented_set_item():
    red = RedBaron("[\n    1,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list[0] = "42"
    assert comma_proxy_list[0].type == "int"
    assert comma_proxy_list[0].value == 42
    comma_proxy_list[0] = "plop"
    assert comma_proxy_list[0].type == "name"
    assert comma_proxy_list[0].value == "plop"
    assert red.dumps() == "[\n    plop,\n]"


def test_comma_proxy_list_indented_set_slice():
    red = RedBaron("[\n    1,\n    2,\n    3,\n]")
    comma_proxy_list = red[0].value
    comma_proxy_list[1:2] = ["42", "31", "23"]
    assert red.dumps() == "[\n    1,\n    42,\n    31,\n    23,\n    3,\n]"


def test_comma_proxy_list_indented_delslice():
    red = RedBaron("[\n    1,\n    2,\n    3,\n    4,\n    5,\n    6,\n]")
    comma_proxy_list = red[0].value
    del comma_proxy_list[1:4]
    assert red.dumps() == "[\n    1,\n    5,\n    6,\n]"


comma_proxy_list_indented_code_to_test = """
with stuff:
    a = [
        1,
    ]
"""


comma_proxy_list_indented_code_to_test_expected_result = """
with stuff:
    a = [
        1,
        2,
    ]
"""

def test_comma_proxy_list_indented_in_indentation_case():
    red = RedBaron(comma_proxy_list_indented_code_to_test)
    red.list_.append("2")
    assert red.dumps() == comma_proxy_list_indented_code_to_test_expected_result


def test_decorator_line_proxy_with_blank_line_list_len_empty():
    red = RedBaron("def a():\n    pass\n")
    assert len(red[0].decorators) == 0


def test_decorator_line_proxy_list_len():
    red = RedBaron("@plop\n@pouet\ndef a():\n    pass\n")
    assert len(red[0].decorators) == 2


def test_decorator_line_proxy_list_insert():
    red = RedBaron("def a():\n    pass\n")
    red[0].decorators.insert(0, "@plop")
    assert red.dumps() == "@plop\ndef a():\n    pass\n"


def test_decorator_line_proxy_list_insert_2_at_middle():
    red = RedBaron("@plop\n@plouf\ndef a():\n    pass\n")
    red[0].decorators.insert(1, "@pop")
    assert red.dumps() == "@plop\n@pop\n@plouf\ndef a():\n    pass\n"


def test_decorator_line_proxy_list_append():
    red = RedBaron("@plop\ndef a():\n    pass\n\n")
    red[0].decorators.append("@c.d.e")
    assert red.dumps() == "@plop\n@c.d.e\ndef a():\n    pass\n\n"


def test_decorator_line_proxy_list_pop():
    red = RedBaron("@a\n@b\ndef a():\n    pass\n")
    red[0].decorators.pop(0)
    assert red.dumps() == "@b\ndef a():\n    pass\n"


def test_decorator_line_proxy_list_pop_2():
    red = RedBaron("@a\n@b\n@c\ndef a():\n    pass\n")
    red[0].decorators.pop(2)
    assert red.dumps() == "@a\n@b\ndef a():\n    pass\n"


def test_decorator_line_proxy_list_del():
    red = RedBaron("@plop\n@qsd\ndef a():\n    pass\n")
    del red[0].decorators[0]
    assert red.dumps() == "@qsd\ndef a():\n    pass\n"


def test_decorator_line_proxy_list_remove():
    red = RedBaron("@a\n@b\ndef a():\n    pass\n")
    red[0].decorators.remove(red[0].decorators[0])
    assert red.dumps() == "@b\ndef a():\n    pass\n"


def test_decorator_line_proxy_list_set_slice():
    red = RedBaron("def a():\n    pass\n")
    red[0].decorators[1:2] = ["@caramba", "@compote"]
    assert red.dumps() == "@caramba\n@compote\ndef a():\n    pass\n"
    assert isinstance(red[0].decorators, DecoratorsLineProxyList)


def test_decorator_line_proxy_list_delslice():
    red = RedBaron("@a\n@b\n@c\ndef a():\n    pass\n")
    del red[0].decorators[1:4]
    assert red.dumps() == "@a\ndef a():\n    pass\n"


def test_decorator_line_proxy_list_getslice():
    red = RedBaron("@a\n@b\n@c\ndef a():\n    pass\n")
    result = red[0].decorators[1:3]
    expected_result = DecoratorsLineProxyList(NodeList([red[0].decorators[1], red[0].decorators[2]]))
    assert len(result) == len(expected_result)
    assert result[0] == expected_result[0]


def test_decorator_line_proxy_list_extend():
    red = RedBaron("def a():\n    pass\n")
    red[0].decorators.extend(["@zob"])
    assert red.dumps() == "@zob\ndef a():\n    pass\n"




forwarded_indented_code_decorators = """
class A():
    def b(self):
        pass

    def c(self):
        pass
"""

forwarded_indented_code_result_decorators = """
class A():
    @plop
    def b(self):
        pass

    def c(self):
        pass
"""

def test_decorator_line_proxy_dont_break_next_block_identation():
    red = RedBaron(forwarded_indented_code_decorators)
    red.def_.decorators.append("@plop")
    assert red.dumps() == forwarded_indented_code_result_decorators


def test_line_proxy_correctly_indent_code_block():
    red = RedBaron("while True:\n    pass\n")
    red[0].extend(["if a:\n    pass\n\n"])
    assert red.dumps() == "while True:\n    pass\n    if a:\n        pass\n\n"


def test_root_as_line_proxy_list_len():
    red = RedBaron("a\nb\nc\n")
    assert len(red) == 3


def test_root_as_line_proxy_list_insert():
    red = RedBaron("a\nb\nc\n")
    red.insert(1, "c")
    assert red.dumps() == "a\nc\nb\nc\n"


def test_root_as_line_proxy_list_append():
    red = RedBaron("a\nb\nc\n")
    red.append("c")
    assert red.dumps() == "a\nb\nc\nc\n"


def test_root_as_line_proxy_list_pop():
    red = RedBaron("a\nb\nc\nc\n")
    red.pop()
    assert red.dumps() == "a\nb\nc\n"


def test_root_as_line_proxy_list_pop_2():
    red = RedBaron("a\nb\nc\n")
    red.pop(0)
    assert red.dumps() == "b\nc\n"


def test_root_as_line_proxy_list_del():
    red = RedBaron("b\nc\n")
    del red[0]
    assert red.dumps() == "c\n"


def test_root_as_line_proxy_list_del_blank_line():
    red = RedBaron("\na\nb\nc\n")
    del red[1]
    assert red.dumps() == "\nb\nc\n"


def test_root_as_line_proxy_list_remove():
    red = RedBaron("\n\na\nb\nc\n")
    red.remove(red[0])
    assert red.dumps() == "\na\nb\nc\n"


def test_root_as_line_proxy_list_remove_2():
    red = RedBaron("\n\na\nb\nc\n")
    red.remove(red[2])
    assert red.dumps() == "\n\nb\nc\n"


def test_root_as_line_proxy_list_set_slice():
    red = RedBaron("\n\na\nb\nc\n")
    red[1:2] = ["caramba", "compote"]
    assert red.dumps() == "\ncaramba\ncompote\na\nb\nc\n"


def test_root_as_line_proxy_list_delslice():
    red = RedBaron("\n\na\nb\nc\n")
    del red[1:4]
    assert red.dumps() == "\nc\n"


def test_root_as_line_proxy_list_getslice():
    red = RedBaron("\n\na\nb\nc\n")
    result = red[1:3]
    expected_result = LineProxyList(NodeList([red[1], red[2]]))
    assert len(result) == len(expected_result)
    assert result[0] == expected_result[0]


def test_root_as_line_proxy_list_extend():
    red = RedBaron("\n\na\nb\nc\n")
    red.extend(["zob"])
    assert red.dumps() == "\n\na\nb\nc\nzob\n"
