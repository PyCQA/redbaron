import sys
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


def test_from_import_names_parenthesis():
    red = RedBaron("from qsd import (a, c, e as f)")
    assert red[0].names() == ['a', 'c', 'f']


def test_from_import_modules():
    red = RedBaron("from qsd import a, c, e as f")
    assert red[0].modules() == ['a', 'c', 'e']


def test_from_import_full_path_names():
    red = RedBaron("from qsd import a, c, e as f")
    assert red[0].full_path_names() == ['qsd.a', 'qsd.c', 'qsd.f']


def test_from_import_full_path_names_parenthesis():
    red = RedBaron("from qsd import (a, c, e as f)")
    assert red[0].full_path_names() == ['qsd.a', 'qsd.c', 'qsd.f']


def test_from_import_full_path_modules():
    red = RedBaron("from qsd import a, c, e as f")
    assert red[0].full_path_modules() == ['qsd.a', 'qsd.c', 'qsd.e']


def test_from_import_full_path_modules_parenthesis():
    red = RedBaron("from qsd import (a, c, e as f)")
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
    if sys.version < '3':
        assert red[0].to_python() == 9


def test_to_python_hexa_node():
    red = RedBaron("0xFF")
    assert red[0].value == "0xFF"
    assert red[0].to_python() == 255


def test_to_python_long_node():
    # long doesn't exist anymore in python3
    if sys.version < '3':
        red = RedBaron("10L")
        assert red[0].value == "10L"
        assert red[0].to_python() == long("10L")


def test_to_python_binary_node():
    red = RedBaron("0b101010101")
    assert red[0].value == "0b101010101"
    assert red[0].to_python() == 341


def test_to_python_float_exponant_node():
    red = RedBaron("1.1e1")
    assert red[0].value == "1.1e1"
    assert red[0].to_python() == 11.0


def test_to_python_string_node():
    red = RedBaron("'pouet'")
    assert red[0].value == "'pouet'"
    assert red[0].to_python() == 'pouet'


def test_to_python_string_chain_node():
    red = RedBaron("'pouet' 'pop'")
    assert red[0].dumps() == "'pouet' 'pop'"
    assert red[0].to_python() == 'pouetpop'


def test_to_python_raw_string_node():
    red = RedBaron("r'pouet'")
    assert red[0].value == "r'pouet'"
    assert red[0].to_python() == r'pouet'


def test_to_python_binary_string_node():
    red = RedBaron("b'pouet'")
    assert red[0].value == "b'pouet'"
    assert red[0].to_python() == b'pouet'


def test_to_python_unicode_string_node():
    red = RedBaron("u'pouet'")
    assert red[0].value == "u'pouet'"
    assert red[0].to_python() == u'pouet'


def test_to_python_binary_raw_string_node():
    if sys.version < '3':
        red = RedBaron("br'pouet'")
        assert red[0].value == "br'pouet'"
        assert red[0].to_python() == eval("br'pouet'")


def test_to_python_unicode_raw_string_node():
    if sys.version < '3':
        red = RedBaron("ur'pouet'")
        assert red[0].value == "ur'pouet'"
        assert red[0].to_python() == eval("ur'pouet'")


def test_to_python_tuple_node():
    red = RedBaron("(1, 2, 3)")
    assert red[0].to_python() == (1, 2, 3)


def test_to_python_list_node():
    red = RedBaron("[1, 2, 3]")
    assert red[0].to_python() == [1, 2, 3]


def test_to_python_dict_node():
    red = RedBaron("{1: 2, 2: 3, 3: 4}")
    assert red[0].to_python() == {1: 2, 2: 3, 3: 4}


def test_to_python_name_node_boolean():
    red = RedBaron("False")
    assert red[0].to_python() == False
    red = RedBaron("True")
    assert red[0].to_python() == True


def test_to_python_name_node_None():
    red = RedBaron("None")
    assert red[0].to_python() == None


def test_to_python_with_spacing():
    red = RedBaron("{ 'pouet': d}")
    assert red.find("string").to_python() == 'pouet'


def test_to_python_name_node_otherwise_raise():
    red = RedBaron("foo")
    try:
        red[0].to_python()
    except Exception as e:
        message = 'to_python method only works on numbers, strings, list, tuple, dict, boolean and None. (using ast.literal_eval). The piece of code that you are trying to convert contains an illegale value, for example, a variable.'
        assert e.message == message
        assert e.args == (message,)
