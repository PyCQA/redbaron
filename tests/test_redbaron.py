#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Main redbaron test module """

import re
import sys
from redbaron import RedBaron, truncate


python_version = sys.version_info[0]
if python_version == 3:
    unicode_type = str
    unicode_chr = chr
else:
    unicode_type = unicode
    unicode_chr = unichr


def test_other_name_assignment():
    red = RedBaron("a = b")
    assert red.assign is red[0]


def test_index():
    red = RedBaron("a = [1, 2, 3]")
    assert red[0].value.value[2].index_on_parent == 2
    assert red[0].index_on_parent == 0
    assert red[0].value.index_on_parent is None


def test_index_raw():
    red = RedBaron("a = [1, 2, 3]")
    assert red[0].value.value.node_list[2].index_on_parent_raw == 2
    assert red[0].index_on_parent == 0
    assert red[0].value.index_on_parent_raw is None


def test_regression_find_all_recursive():
    red = RedBaron("a.b()")
    assert red[0].value("name", recursive=False) == [red.name, red("name")[1]]


def test_truncate():
    assert "1234" == truncate("1234", 2)
    assert "12345" == truncate("12345", 4)
    assert "1...6" == truncate("123456", 5)
    assert "123456...0" == truncate("12345678901234567890", 10)

def test_html_repr():
    def strip_html_tags(s):
        assert isinstance(s, unicode_type)
        s = re.sub(r'<[^>]+>', '', s)
        s = re.sub(r'\n+', '\n', s)
        s = re.sub(r'&#([0-9]+);', lambda m: unicode_chr(int(m.group(1))), s)
        return s
    source = (
        b"first = line  # commentaire en fran\xC3\x87ais\n"
        b'wait()\n'
        b"if second_line:\n"
        b"    # l'unicode est support\xC3\xA9\n"
        b"    third(line)\n")
    if python_version == 3:
        source = source.decode('utf-8')
    red = RedBaron(source)
    assert strip_html_tags(red._repr_html_()) == (
        u'Index' u'node'
        u'0' u'first = line\n'
        u'1' u'  # commentaire en fran\xC7ais\n'
        u'2' u'wait()\n'
        u'3' u'if second_line:\n'
        u"    # l'unicode est support\xE9\n"
        u'    third(line)\n')
    assert strip_html_tags(red.node_list[1:4]._repr_html_()) == (
        u'Index' u'node'
        u'0' u'  # commentaire en fran\xC7ais\n'
        u'1' u"'\\n'\n"
        u'2' u'wait()\n')

