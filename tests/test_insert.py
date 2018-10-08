#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests the code insertion features """

import pytest
# pylint: disable=redefined-outer-name
import redbaron
from redbaron import RedBaron

# (alekum): switch off debug mode, to reproduce a bug with __repr__ implicit recursion
redbaron.DEBUG = False


def assert_with_indent(left, right):
    # Replace is not strictly necessary but shows indents
    assert left.dumps().replace(' ', '.') == right.replace(' ', '.')


@pytest.fixture
def red_A_B():
    return RedBaron("""\
class A:
    pass

class B:
    pass
""")


@pytest.fixture
def red_nested():
    return RedBaron("""\
class A:
    class B:
        pass
""")


def test_insert_with_class_0(red_A_B):
    red_A_B.insert(0, "a = 1")

    assert_with_indent(red_A_B, """\
a = 1
class A:
    pass

class B:
    pass
""")


def test_insert_with_class_1(red_A_B):
    red_A_B.insert(1, "a = 1")

    assert_with_indent(red_A_B, """\
class A:
    pass

a = 1
class B:
    pass
""")


def test_insert_with_class_2(red_A_B):
    red_A_B.insert(2, "a = 1")

    assert_with_indent(red_A_B, """\
class A:
    pass

class B:
    pass
a = 1
""")


def test_insert_with_class_3(red_A_B):
    red_A_B.insert(3, "a = 1")

    assert_with_indent(red_A_B, """\
class A:
    pass

class B:
    pass
a = 1
""")


def test_insert_class_with_class_0(red_A_B):
    red_A_B.insert(0, "class C:\n    pass")

    assert_with_indent(red_A_B, """\
class C:
    pass
class A:
    pass

class B:
    pass
""")


def test_insert_class_with_class_1(red_A_B):
    red_A_B.insert(1, "class C:\n    pass")

    assert_with_indent(red_A_B, """\
class A:
    pass

class C:
    pass
class B:
    pass
""")


def test_insert_class_with_class_2(red_A_B):
    red_A_B.insert(2, "class C:\n    pass")

    assert_with_indent(red_A_B, """\
class A:
    pass

class B:
    pass
class C:
    pass
""")


def test_insert_class_with_class_3(red_A_B):
    red_A_B.insert(3, "class C:\n    pass")

    assert_with_indent(red_A_B, """\
class A:
    pass

class B:
    pass
class C:
    pass
""")


def test_insert_with_nested_class_0(red_nested):
    red_nested.insert(0, "a = 1")

    assert_with_indent(red_nested, """\
a = 1
class A:
    class B:
        pass
""")


def test_insert_with_nested_class_1(red_nested):
    red_nested.insert(1, "a = 1")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
a = 1
""")


def test_insert_inside_nested_class_0(red_nested):
    red_nested[0].insert(0, "a = 1")

    assert_with_indent(red_nested, """\
class A:
    a = 1
    class B:
        pass
""")


def test_insert_inside_nested_class_1(red_nested):
    red_nested[0].insert(1, "a = 1")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
    a = 1
""")


def test_insert_inside_nested_class_2(red_nested):
    red_nested[0].insert(0, "def a(self):\n    pass")

    assert_with_indent(red_nested, """\
class A:
    def a(self):
        pass
    class B:
        pass
""")


def test_insert_class_inside_nested_class_0(red_nested):
    red_nested[0].insert(0, "class C:\n    pass")

    assert_with_indent(red_nested, """\
class A:
    class C:
        pass
    class B:
        pass
""")


def test_insert_class_inside_nested_class_1(red_nested):
    red_nested[0].insert(1, "class C:\n    pass")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
    class C:
        pass
""")


def test_append_inside_nested_class(red_nested):
    red_nested[0].append("a = 1")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
    a = 1
""")


def test_append_class_inside_nested_class(red_nested):
    red_nested[0].append("class C:\n    pass")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
    class C:
        pass
""")


def test_append_method_in_nested_with_methods():
    red = RedBaron("""\
class A:
    def a(self):
        pass

    def b(self):
        pass

""")

    red[0].append("def c(self):\n    pass")

    assert_with_indent(red, """\
class A:
    def a(self):
        pass

    def b(self):
        pass

    def c(self):
        pass
""")


def test_append_class_in_nested_with_methods():
    red = RedBaron("""\
class A:
    def a(self):
        pass

    def b(self):
        pass

""")

    red[0].append("class C:\n    pass")

    assert_with_indent(red, """\
class A:
    def a(self):
        pass

    def b(self):
        pass

    class C:
        pass
""")


def test_insert_line_in_def_with_if():
    red = RedBaron("""\
def a(self, a):
    if a == 42:
        return True
    return False
""")

    red.def_.insert(0, "a = 1")

    assert_with_indent(red, """\
def a(self, a):
    a = 1
    if a == 42:
        return True
    return False
""")


def test_insert_nested_line_in_def_with_if():
    red = RedBaron("""\
def a(self, a):
    if a == 42:
        return True
    return False
""")

    red.def_.if_.insert(0, "a = 1")

    assert_with_indent(red, """\
def a(self, a):
    if a == 42:
        a = 1
        return True
    return False
""")


def test_insert_newline_in_def_with_if():
    red = RedBaron("""\
def a(self, a):
    if a == 42:
        return True
    return False
""")

    red.def_.if_.insert(0, "a = 1")
    assert_with_indent(red, """\
def a(self, a):
    if a == 42:
        a = 1
        return True
    return False
""")

    red.def_.if_.insert(0, "")
    assert_with_indent(red, """\
def a(self, a):
    if a == 42:

        a = 1
        return True
    return False
""")

    red.def_.if_.insert(0, "b = 2")

    assert_with_indent(red, """\
def a(self, a):
    if a == 42:
        b = 2

        a = 1
        return True
    return False
""")


def test_append_newline_line_in_def_with_if():
    red = RedBaron("""\
def a(self, a):
    if a == 42:
        return True
    return False
""")

    red.def_.if_.append("")
    red.def_.if_.extend(["", "a = 1", ""])

    assert_with_indent(red, """\
def a(self, a):
    if a == 42:
        return True


        a = 1

    return False
""")


def test_extend_newline_and_def_in_def():
    red = RedBaron("""\
def a(self, a):
    return False
""")

    red.def_.extend(["", "def b():\n    return True", ""])
    red.def_.extend(["", "def b():\n    return True", ""])

    assert_with_indent(red, """\
def a(self, a):
    return False

    def b():
        return True


    def b():
        return True

""")


def test_append_newline_and_def_in_nested_class():
    red = RedBaron("""\
class A:
    class B:
        pass
""")

    # red.class_.class_.append("def b():\n    return True")
    red.class_.class_.append("a = 1")

    assert_with_indent(red, """\
class A:
    class B:
        pass
        a = 1
""")


def test_append_newline_and_def_in_class_with_space():
    red = RedBaron("""\
def a(self, a):
    return False
""")

    red.def_.append("")
    red.def_.append("class b:\n    def c(self):\n        return True")
    red.def_.append("")
    red.def_.append("class b:\n    def c(self):\n        return True")
    red.def_.append("")

    assert_with_indent(red, """\
def a(self, a):
    return False

    class b:
        def c(self):
            return True

    class b:
        def c(self):
            return True

""")


def test_append_newline_and_async_def_in_class_with_space():
    red = RedBaron("""\
async def a(self, a):
    return False
""")

    red.def_.append("")
    red.def_.append("class b:\n    def c(self):\n        return True")
    red.def_.append("")
    red.def_.append("class b:\n    async def c(self):\n        return True")
    red.def_.append("")

    assert_with_indent(red, """\
async def a(self, a):
    return False

    class b:
        def c(self):
            return True

    class b:
        async def c(self):
            return True

""")


def test_append_newline_and_def_in_class_without_space():
    red = RedBaron("""\
def a(self, a):
    return False
""")

    red.def_.append("")
    red.def_.append("class b:\n    def c(self):\n        return True")
    red.def_.append("class b:\n    def c(self):\n        return True")
    red.def_.append("")

    assert_with_indent(red, """\
def a(self, a):
    return False

    class b:
        def c(self):
            return True
    class b:
        def c(self):
            return True

""")


def test_dont_add_newlines_after_import():
    red = RedBaron("import a\n\nimport b\n\npouet\n")
    red.append("plop")
    assert red.dumps() == "import a\n\nimport b\n\npouet\nplop\n"
