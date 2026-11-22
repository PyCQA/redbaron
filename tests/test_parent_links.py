import pytest

from redbaron import RedBaron


def test_insert_after_inserted_node():
    red = RedBaron('class A:\n    a = 1\n    b = 2\n')
    red.class_.value[0].insert_after('c = 3')
    red.class_.value[1].insert_after('d = 4')
    assert red.dumps() == 'class A:\n    a = 1\n    c = 3\n    d = 4\n    b = 2\n'


def test_help_after_inserting_root_node(capsys):
    red = RedBaron("foo = 42\nprint('bar')\n")
    red.print_.insert_before('baz')
    red.help()
    assert 'baz' in capsys.readouterr().out
    for node in red.node_list:
        assert node.parent is red
        assert node.root is red
        assert node.absolute_bounding_box is not None


@pytest.mark.parametrize('operation', ['insert', 'extend', 'replace', 'slice'])
def test_proxy_list_mutations_preserve_parent_links(operation):
    red = RedBaron('result = [1, 2, 3]\n')
    values = red.list_.value
    if operation == 'insert':
        values.insert(1, '4')
    elif operation == 'extend':
        values.extend(['4', '5'])
    elif operation == 'replace':
        values[1] = '4'
    else:
        values[1:2] = ['4', '5']
    for node in values.node_list:
        assert node.parent is red.list_
        assert node.on_attribute == 'value'
        assert node.root is red
        assert node.absolute_bounding_box is not None
