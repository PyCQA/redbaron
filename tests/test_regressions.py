import pytest

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


@pytest.mark.parametrize(
    'original_src, transformed_src',
    (
        (
            "\nimport i1\nimport i2\n",
            "\nimport i1\nimport i2\nimport i1\n",
        ),
        (
            "\nimport i1\nimport i2\n\nif True:\n    main()\n",
            "\nimport i1\nimport i2\nimport i1\n\nif True:\n    main()\n",
        ),
    )
)
def test_does_not_dumps_extra_trailing_lf_after_root_insert_if_nested(
        original_src,
        transformed_src,
):
    red = RedBaron(original_src)
    imp1, imp2 = red.find_all('import')
    imp2.insert_after(imp1)
    assert red.dumps() == transformed_src
