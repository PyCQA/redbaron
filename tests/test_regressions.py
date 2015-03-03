from redbaron import RedBaron


def test_mixmatch_with_redbaron_base_node_and_proxy_list_on_parent():
    red = RedBaron("foo = 42\nprint('bar')\n")
    red.insert(0, "baz")
    assert red[0].on_attribute == "root"
    assert red[0].parent is red
