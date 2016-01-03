#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests initial parsing through the RedBaron() base function """


import baron
import re
from redbaron import (RedBaron, NameNode, EndlNode, IntNode, AssignmentNode,
                      PassNode, NodeList, CommaNode, DotNode, CallNode,
                      CommaProxyList)


def test_empty():
    RedBaron("")


def test_is_list():
    assert [] == list(RedBaron(""))


def test_name():
    red = RedBaron("a\n")
    assert len(red.node_list) == 2
    assert isinstance(red.node_list[0], NameNode)
    assert isinstance(red.node_list[1], EndlNode)
    assert red[0].value == "a"


def test_int():
    red = RedBaron("1\n")
    assert isinstance(red[0], IntNode)
    assert red[0].value == "1"


def test_assign():
    red = RedBaron("a = 2")
    assert isinstance(red[0], AssignmentNode)
    assert isinstance(red[0].value, IntNode)
    assert red[0].value.value == "2"
    assert isinstance(red[0].target, NameNode)
    assert red[0].target.value == "a"


def test_binary_operator():
    red = RedBaron("z +  42")
    assert red[0].value == "+"
    assert isinstance(red[0].first, NameNode)
    assert red[0].first.value == "z"
    assert isinstance(red[0].second, IntNode)
    assert red[0].second.value == "42"

    red = RedBaron("z  -      42")
    assert red[0].value == "-"
    assert isinstance(red[0].first, NameNode)
    assert red[0].first.value == "z"
    assert isinstance(red[0].second, IntNode)
    assert red[0].second.value == "42"


def test_pass():
    red = RedBaron("pass")
    assert isinstance(red[0], PassNode)


def test_copy():
    red = RedBaron("a")
    name = red[0]
    assert name.value == name.copy().value
    assert name is not name.copy()


def test_dumps():
    some_code = "ax + (z * 4)"
    red = RedBaron(some_code)
    assert some_code == red.dumps()


def test_fst():
    some_code = "ax + (z * 4)"
    red = RedBaron(some_code)
    assert baron.parse(some_code) == red.fst()


def test_get_helpers():
    red = RedBaron("a")
    assert red[0]._get_helpers() == []
    red = RedBaron("import a")
    assert red[0]._get_helpers() == ['modules', 'names']


def test_help_is_not_crashing():
    some_code = "ax + (z * 4)"
    red = RedBaron(some_code)
    red.help()
    red[0].help()


def test_assign_on_string_value():
    some_code = "ax + (z * 4)"
    red = RedBaron(some_code)
    binop = red[0]
    assert binop.first.value == "ax"
    binop.first.value = "pouet"
    assert binop.first.value == "pouet"


def test_assign_on_object_value():
    some_code = "ax + (z * 4)"
    red = RedBaron(some_code)
    binop = red[0]
    assert binop.first.value == "ax"
    binop.first = "pouet"  # will be parsed as a name
    assert binop.first.value == "pouet"
    assert binop.first.type == "name"
    binop.first = "42"  # will be parsed as a int
    assert binop.first.value == "42"
    assert binop.first.type == "int"


def test_assign_on_object_value_fst():
    some_code = "ax + (z * 4)"
    red = RedBaron(some_code)
    binop = red[0]
    binop.first = {"type": "name", "value": "pouet"}
    assert binop.first.value == "pouet"
    assert binop.first.type == "name"


def test_generate_helpers():
    red = RedBaron("def a(): pass")
    assert set(red[0]._identifiers) == set([
        "funcdef", "funcdef_", "defnode", "def", "def_"
        ])


def test_assign_node_list():
    red = RedBaron("[1, 2, 3]")
    l = red[0]
    l.value = "pouet"
    assert l.value[0].value == "pouet"
    assert l.value[0].type == "name"
    assert isinstance(l.value.node_list, NodeList)
    assert isinstance(l.value, CommaProxyList)
    l.value = ["pouet"]
    assert l.value[0].value == "pouet"
    assert l.value[0].type == "name"
    assert isinstance(l.value.node_list, NodeList)
    assert isinstance(l.value, CommaProxyList)


def test_assign_node_list_fst():
    red = RedBaron("[1, 2, 3]")
    l = red[0]
    l.value = {"type": "name", "value": "pouet"}
    assert l.value[0].value == "pouet"
    assert l.value[0].type == "name"
    assert isinstance(l.value.node_list, NodeList)
    assert isinstance(l.value, CommaProxyList)
    l.value = [{"type": "name", "value": "pouet"}]
    assert l.value[0].value == "pouet"
    assert l.value[0].type == "name"
    assert isinstance(l.value.node_list, NodeList)
    assert isinstance(l.value, CommaProxyList)


def test_assign_node_list_mixed():
    red = RedBaron("[1, 2, 3]")
    l = red[0]
    l.value = ["plop",
               {"type": "comma",
                "first_formatting": [],
                "second_formatting": []},
               {"type": "name", "value": "pouet"}]
    assert l.value[0].value == "plop"
    assert l.value[0].type == "name"
    assert l.value.node_list[1].type == "comma"
    assert l.value[1].value == "pouet"
    assert l.value[1].type == "name"
    assert l.value.node_list[2].value == "pouet"
    assert l.value.node_list[2].type == "name"
    assert isinstance(l.value.node_list, NodeList)
    assert isinstance(l.value, CommaProxyList)


def test_parent():
    red = RedBaron("a = 1 + caramba")
    assert red.parent is None
    assert red[0].parent is red
    assert red[0].on_attribute == "root"
    assert red[0].target.parent is red[0]
    assert red[0].target.on_attribute == "target"
    assert red[0].value.parent is red[0]
    assert red[0].value.on_attribute == "value"
    assert red[0].value.first.parent is red[0].value
    assert red[0].value.first.on_attribute == "first"
    assert red[0].value.second.parent is red[0].value
    assert red[0].value.second.on_attribute == "second"

    red = RedBaron("[1, 2, 3]")
    assert red.parent is None
    assert red[0].parent is red
    assert [x.parent for x in red[0].value.node_list] == [red[0]]*5
    assert [x.on_attribute for x in red[0].value.node_list] == ["value"]*5
    assert [x.parent for x in red[0].value] == [red[0]]*3
    assert [x.on_attribute for x in red[0].value] == ["value"]*3


def test_parent_copy():
    red = RedBaron("a = 1 + caramba")
    assert red[0].value.copy().parent is None


def test_parent_assign():
    red = RedBaron("a = 1 + caramba")
    assert red[0].target.parent is red[0]
    red[0].target = "plop"
    assert red[0].target.parent is red[0]
    assert red[0].target.on_attribute == "target"
    red[0].target = {"type": "name", "value": "pouet"}
    assert red[0].target.parent is red[0]
    assert red[0].target.on_attribute == "target"
    red[0].target = NameNode({"type": "name", "value": "pouet"})
    assert red[0].target.parent is red[0]
    assert red[0].target.on_attribute == "target"

    red = RedBaron("[1, 2, 3]")
    assert [x.parent for x in red[0].value] == [red[0]]*3
    assert [x.on_attribute for x in red[0].value] == ["value"]*3
    assert [x.parent for x in red[0].value.node_list] == [red[0]]*5
    assert [x.on_attribute for x in red[0].value.node_list] == ["value"]*5
    red[0].value = "pouet"
    assert [x.parent for x in red[0].value] == [red[0]]
    assert [x.on_attribute for x in red[0].value] == ["value"]
    red[0].value = ["pouet"]
    assert [x.parent for x in red[0].value] == [red[0]]
    assert [x.on_attribute for x in red[0].value] == ["value"]
    red[0].value = {"type": "name", "value": "plop"}
    assert [x.parent for x in red[0].value] == [red[0]]
    assert [x.on_attribute for x in red[0].value] == ["value"]
    red[0].value = [{"type": "name", "value": "plop"}]
    assert [x.parent for x in red[0].value] == [red[0]]
    assert [x.on_attribute for x in red[0].value] == ["value"]
    red[0].value = NameNode({"type": "name", "value": "pouet"})
    assert isinstance(red[0].value.node_list, NodeList)
    assert isinstance(red[0].value, CommaProxyList)
    assert [x.parent for x in red[0].value] == [red[0]]
    assert [x.on_attribute for x in red[0].value] == ["value"]
    red[0].value = [NameNode({"type": "name", "value": "pouet"})]
    assert [x.parent for x in red[0].value] == [red[0]]
    assert [x.on_attribute for x in red[0].value] == ["value"]


def test_node_next():
    red = RedBaron("[1, 2, 3]")
    assert red.next is None
    assert red[0].next is None
    inner = red[0].value.node_list
    assert inner[0].next == inner[1]
    assert inner[1].next == inner[2]
    assert inner[2].next == inner[3]
    assert inner[3].next == inner[4]
    assert inner[4].next is None


def test_node_next_recursive():
    red = RedBaron("def a():\n    b = 1\ndef c():\n    d = 1")
    assert red.next is None
    assert red.next_recursive is None
    first, second = red.find_all('def')
    assert first.next is second
    inner = first.value.node_list
    assert inner[0].next == inner[1]
    assert inner[0].next_recursive == inner[1]
    assert inner[1].next == inner[2]
    assert inner[1].next_recursive == inner[2]
    assert inner[2].next == None
    assert inner[2].next_recursive == second


def test_node_previous():
    red = RedBaron("[1, 2, 3]")
    assert red.previous is None
    assert red[0].previous is None
    inner = red[0].value.node_list
    assert inner[4].previous == inner[3]
    assert inner[3].previous == inner[2]
    assert inner[2].previous == inner[1]
    assert inner[1].previous == inner[0]
    assert inner[0].previous is None


def test_node_previous_recursive():
    red = RedBaron("def a():\n    b = 1\ndef c():\n    d = 1")
    assert red.previous is None
    assert red.previous_recursive is None
    first, second = red.find_all('def')
    assert second.previous is first
    inner = second.value.node_list
    assert inner[2].previous == inner[1]
    assert inner[2].previous_recursive == inner[1]
    assert inner[1].previous == inner[0]
    assert inner[1].previous_recursive == inner[0]
    assert inner[0].previous == None
    assert inner[0].previous_recursive == first


def test_node_next_generator():
    red = RedBaron("[1, 2, 3]")
    assert list(red[0].value[2].next_generator()) == list(red[0].value[3:])


def test_node_previous_generator():
    red = RedBaron("[1, 2, 3]")
    assert list(red[0].value.node_list[2].previous_generator()) \
        == list(reversed(red[0].value.node_list[:2]))


def test_map():
    red = RedBaron("[1, 2, 3]")
    assert red('int').map(lambda x: x.value) == NodeList(["1", "2", "3"])


def test_apply():
    red = RedBaron("a()\nb()")
    assert red('call').apply(lambda x: x.stuff) == red('call')


def test_filter():
    red = RedBaron("[1, 2, 3]")
    assert red[0].value.filter(lambda x: x.type != "comma") == red('int')
    assert isinstance(red[0].value.filter(lambda x: x.type != "comma"), NodeList)


def test_indent_root():
    red = RedBaron("pouet")
    assert red[0].indentation == ""
    red = RedBaron("pouet\nplop\npop")
    assert [x.indentation for x in red.node_list] == ["", "", "", "", ""]
    assert [x.get_indentation_node() for x in red.node_list] \
        == [None, None, red.node_list[1], None, red.node_list[3]]


def test_in_while():
    red = RedBaron("while a:\n    pass\n")
    node_list = red[0].value.node_list
    assert node_list[-2].indentation == "    "
    assert node_list[-1].indentation == ""
    assert node_list[-2].get_indentation_node() is red[0].value.node_list[-3]
    assert node_list[-1].get_indentation_node() is None
    assert node_list[-3].get_indentation_node() is None
    assert node_list[-2].indentation_node_is_direct()


def test_one_line_while():
    red = RedBaron("while a: pass\n")
    assert red[0].value.node_list[0].indentation == ""
    assert red[0].value.node_list[-2].get_indentation_node() is None
    assert not red[0].value.node_list[-2].indentation_node_is_direct()


def test_inner_node():
    red = RedBaron("while a: pass\n")
    assert red[0].test.indentation == ""
    assert red[0].value.node_list[-2].get_indentation_node() is None
    assert not red[0].value.node_list[-2].indentation_node_is_direct()


def test_indentation_endl():
    red = RedBaron("a.b.c.d")
    assert red[0].value[-3].indentation == ""
    assert red[0].value[-2].get_indentation_node() is None
    assert not red[0].value[-2].indentation_node_is_direct()


def test_filtered_endl():
    red = RedBaron("while a:\n    pass\n")
    assert red[0].value.node_list.filtered() == (red[0].value.node_list[-2],)


def test_filtered_comma():
    red = RedBaron("[1, 2, 3]")
    assert red[0].value.filtered() \
        == tuple(red[0].value.filter(lambda x: not isinstance(x, CommaNode)))


def test_filtered_dot():
    red = RedBaron("a.b.c(d)")
    assert red[0].value.filtered() \
        == tuple(red[0].value.filter(lambda x: not isinstance(x, DotNode)))


SOME_DATA_FOR_TEST = """\
def plop():
    def a():
        with b as c:
            d = e
"""

def test_parent_find_empty():
    red = RedBaron("a")
    assert red[0].parent_find('a') is None


def test_parent_find_direct():
    red = RedBaron(SOME_DATA_FOR_TEST)
    target = red.assignment.target
    assert target.parent_find('with') is red.with_


def test_parent_find_two_levels():
    red = RedBaron(SOME_DATA_FOR_TEST)
    target = red.assignment.target
    assert target.parent_find('def') is red.find('def', name='a')


def test_parent_find_two_levels_options():
    red = RedBaron(SOME_DATA_FOR_TEST)
    target = red.assignment.target
    assert target.parent_find('def', name='plop') is red.def_
    assert target.parent_find('def', name='dont_exist') is None


def test_find_empty():
    red = RedBaron("")
    assert red.find("stuff") is None
    assert red.find("something_else") is None
    assert red.find("something_else", useless="pouet") is None
    assert red.something_else is None


def test_find():
    red = RedBaron("def a(): b = c")
    assert red.find("name") is red[0].value[0].target
    assert red.find("name", value="c") is red[0].value[0].value
    assert red.name is red[0].value[0].target


def test_find_other_properties():
    red = RedBaron("def a(): b = c")
    assert red.def_ == red[0]
    assert red.funcdef == red[0]
    assert red.funcdef_ == red[0]


def test_find_case_insensitive():
    red = RedBaron("a")
    assert red.find("NameNode") is red[0]
    assert red.find("NaMeNoDe") is red[0]
    assert red.find("namenode") is red[0]


def test_find_kwarg_lambda():
    red = RedBaron("[1, 2, 3, 4]")
    assert red.find("int", value=lambda x: int(x) % 2 == 0) == red("int")[1]
    assert red("int", value=lambda x: int(x) % 2 == 0) == red('int')[1::2]


def test_find_lambda():
    red = RedBaron("[1, 2, 3, 4]")
    assert red.find("int", lambda x: int(x.value) % 2 == 0) == red('int')[1]
    assert red("int", lambda x: int(x.value) % 2 == 0) == red('int')[1::2]


def test_find_kwarg_regex_instance():
    red = RedBaron("plop\npop\npouf\nabcd")
    assert red.find("name", value=re.compile("^po")) == red[1]


def test_find_all_kwarg_regex_instance():
    red = RedBaron("plop\npop\npouf\nabcd")
    assert red("name", value=re.compile("^po")) \
        == red("name", value=lambda x: x.startswith("po"))


def test_find_kwarg_regex_syntaxe():
    red = RedBaron("plop\npop\npouf\nabcd")
    assert red.find("name", value="re:^po") == red[1]


def test_find_all_kwarg_regex_syntaxe():
    red = RedBaron("plop\npop\npouf\nabcd")
    assert red("name", value="re:^po") \
        == red("name", value=lambda x: x.startswith("po"))


def test_find_kwarg_glob_syntaxe():
    red = RedBaron("plop\npop\npouf\nabcd")
    assert red.find("name", value="g:po*") == red[1]


def test_find_all_kwarg_glob_syntaxe():
    red = RedBaron("plop\npop\npouf\nabcd")
    assert red("name", value="g:po*") \
        == red("name", value=lambda x: x.startswith("po"))


def test_identifier_find_kwarg_lambda():
    red = RedBaron("stuff\n1\n'string'")
    assert red.find(lambda x: x in ["name", "int"]) == red[0]
    assert red(lambda x: x in ["name", "int"]) == red[:2].node_list


def test_identifier_find_kwarg_regex_instance():
    red = RedBaron("stuff\n1\n'string'")
    assert red.find(re.compile("^[ni]")) == red[0]


def test_identifier_find_all_kwarg_regex_instance():
    red = RedBaron("stuff\n1\n'string'")
    assert red(re.compile("^[ni]")) == red[:2].node_list


def test_identifier_find_kwarg_regex_syntaxe():
    red = RedBaron("stuff\n1\n'string'")
    assert red.find("re:^[ni]") == red[0]


def test_identifier_find_all_kwarg_regex_syntaxe():
    red = RedBaron("stuff\n1\n'string'")
    assert red("re:^[ni]") == red[:2].node_list


def test_identifier_find_kwarg_glob_syntaxe():
    red = RedBaron("stuff\n1\n'string'")
    assert red.find("g:s*") == red[-1]


def test_identifier_find_all_kwarg_glob_syntaxe():
    red = RedBaron("stuff\n1\n'string'")
    assert red("g:s*") == red[2:].node_list


def test_find_kwarg_list_tuple_instance():
    red = RedBaron("pouet\n'string'\n1")
    assert red.find("name", value=["pouet", 1]) == red[0]
    assert red.find("name", value=("pouet", 1)) == red[0]


def test_find_all_kwarg_list_tuple_instance():
    red = RedBaron("pouet\nstuff\n1")
    assert red("name", value=["pouet", "stuff"]) == red[:2].node_list
    assert red("name", value=("pouet", "stuff")) == red[:2].node_list


def test_identifier_find_kwarg_list_tuple_instance():
    red = RedBaron("pouet\n'string'\n1")
    assert red.find(["name", "string"]) == red[0]
    assert red.find(("name", "string")) == red[0]


def test_identifier_find_all_kwarg_list_tuple_instance():
    red = RedBaron("pouet\n'string'\n1")
    assert red(["name", "string"]) == red[:2].node_list
    assert red(("name", "string")) == red[:2].node_list


def test_default_test_value_find():
    red = RedBaron("badger\nmushroom\nsnake")
    assert red.find("name", "snake") == red.find("name", value="snake")


def test_default_test_value_find_all():
    red = RedBaron("badger\nmushroom\nsnake")
    assert red("name", "snake") == red("name", value="snake")


def test_default_test_value_find_def():
    red = RedBaron("def a(): pass\ndef b(): pass")
    assert red.find("def", "b") == red.find("def", name="b")


def test_default_test_value_find_class():
    red = RedBaron("class a(): pass\nclass b(): pass")
    assert red.find("class", "b") == red.find("class", name="b")


def test_copy_correct_isntance():
    red = RedBaron("a()")
    assert isinstance(red[0].value[1].copy(), CallNode)


def test_indentation_no_parent():
    red = RedBaron("a")
    assert red[0].copy().get_indentation_node() is None
    assert red[0].copy().indentation == ''


def test_replace():
    red = RedBaron("1 + 2")
    red[0].replace("caramba")
    assert isinstance(red[0], NameNode)
    assert red.dumps() == "caramba"


def test_insert_before():
    red = RedBaron("a = 1\nprint(pouet)\n")
    red.print_.insert_before("chocolat")
    assert red.dumps() == "a = 1\nchocolat\nprint(pouet)\n"


def test_insert_after():
    red = RedBaron("a = 1\nprint(pouet)\n")
    red.print_.insert_after("chocolat")
    assert red.dumps() == "a = 1\nprint(pouet)\nchocolat\n"


def test_insert_before_offset():
    red = RedBaron("a = 1\nprint(pouet)\n")
    red.print_.insert_before("chocolat", offset=1)
    assert red.dumps() == "chocolat\na = 1\nprint(pouet)\n"


def test_insert_after_offset():
    red = RedBaron("a = 1\nprint(pouet)\n")
    red[0].insert_after("chocolat", offset=1)
    assert red.dumps() == "a = 1\nprint(pouet)\nchocolat\n"
