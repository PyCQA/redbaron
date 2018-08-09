from redbaron import RedBaron


def test_mixmatch_with_redbaron_base_node_and_proxy_list_on_parent():
    red = RedBaron("foo = 42\nprint('bar')\n")
    red.insert(0, "baz")
    assert red[0].on_attribute == "root"
    assert red[0].parent is red


def test_can_modify_formatting_attributes_on_codeblocknodes():
    red = RedBaron("class Foo:\n    def bar(): pass")
    red.class_.first_formatting = "    "  # shouldn't raise
    red.def_.second_formatting = "      "  # same


def test_on_copied_blocknode_set_body():
    red = RedBaron("def foobar(): pass")
    z = red.def_.copy()
    z.value = "pouet"


def test_find_empty_call():
    red = RedBaron("a()")
    assert red.find("call") is red[0][1]
