#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests the rendering feature """

import redbaron
from redbaron import (RedBaron, NodeList, CommaProxyList,
                      DotProxyList, LineProxyList, DecoratorsLineProxyList)

redbaron.DEBUG = True


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
    assert comma_proxy_list[0].value == "42"
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


def test_comma_proxy_list_nonlocal_value():
    red = RedBaron("nonlocal a")
    red[0].value.append("b")
    assert red.dumps() == "nonlocal a, b"


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
    assert [x.value for x in red[0]] == ["42"]


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


# XXX I have to reconsider this behavior with the new algo
# XXX this isn't making that much sens anymore
# def test_comma_proxy_list_indented_insert():
#     red = RedBaron("[]")
#     comma_proxy_list = red[0].value
#     comma_proxy_list.style = "indented"
#     comma_proxy_list.insert(0, "1")
#     assert red.dumps() == "[\n    1,\n]"


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


# XXX need to rethink this behavior
# def test_comma_proxy_list_indented_append():
#     red = RedBaron("[]")
#     comma_proxy_list = red[0].value
#     comma_proxy_list.style = "indented"
#     comma_proxy_list.append("1")
#     assert red.dumps() == "[\n    1,\n]"


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
    assert comma_proxy_list[0].value == "42"
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


def test_regression_first_method_of_a_class_decorators_append():
    red = RedBaron("class A:\n    def foo():\n        pass")
    red.def_.decorators.append("@staticmethod")
    assert red.dumps() == "class A:\n    @staticmethod\n    def foo():\n        pass\n"
