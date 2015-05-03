from redbaron import RedBaron


def test_import_modules():
    red = RedBaron("import a, b.c, d.e as f")
    assert red[0].modules() == ['a', 'b.c', 'd.e']


def test_import_names():
    red = RedBaron("import a, b.c, d.e as f")
    assert red[0].names() == ['a', 'b.c', 'f']


def test_from_import_names():
    red = RedBaron("from qsd import a, c, e as f")
    assert red[0].names() == ['a', 'c', 'f']


def test_from_import_modules():
    red = RedBaron("from qsd import a, c, e as f")
    assert red[0].modules() == ['a', 'c', 'e']


def test_from_import_full_path_names():
    red = RedBaron("from qsd import a, c, e as f")
    assert red[0].full_path_names() == ['qsd.a', 'qsd.c', 'qsd.f']


def test_from_import_full_path_modules():
    red = RedBaron("from qsd import a, c, e as f")
    assert red[0].full_path_modules() == ['qsd.a', 'qsd.c', 'qsd.e']


def test_to_python_int_node():
    red = RedBaron("1")
    assert red[0].value == "1"
    assert red[0].to_python() == 1


def test_to_python_float_node():
    red = RedBaron("1.1")
    assert red[0].value == "1.1"
    assert red[0].to_python() == 1.1

def test_to_python_octa_node():
    red = RedBaron("0011")
    assert red[0].value == "0011"
    assert red[0].to_python() == 9

# TODO to_python for HexaNode, LongNode "strings, tuples, lists, dicts, booleans, and None"
