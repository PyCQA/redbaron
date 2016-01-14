#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests the bounding_box feature """

import pytest
# pylint: disable=redefined-outer-name
from redbaron import RedBaron


@pytest.fixture
def red():
    return RedBaron("""\
@deco
def a(c, d):
    b = c + d
""")


fst = red()
bounding_boxes = [
    (((1, 1),  (4, 0)),  ((1, 1), (4, 0)), fst),
    (((1, 1),  (4, 0)),  ((1, 1), (4, 0)), fst.def_),
    (((1, 1),  (2, 0)),  ((1, 1), (2, 0)), fst.def_.decorators.node_list),
    (((1, 1),  (1, 5)),  ((1, 1), (1, 5)), fst.def_.decorators.node_list[0]),
    (((1, 2),  (1, 5)),  ((1, 1), (1, 4)), fst.def_.decorators.node_list[0].value),
    (((1, 2),  (1, 5)),  ((1, 1), (1, 4)), fst.def_.decorators.node_list[0].value.value),
    (((1, 2),  (1, 5)),  ((1, 1), (1, 4)), fst.def_.decorators.node_list[0].value.value[0]),
    (((1, 6),  (2, 0)),  ((1, 1), (2, 0)), fst.def_.decorators.node_list[1]),
    (((2, 4),  (2, 4)),  ((1, 1), (1, 1)), fst.def_.first_formatting),
    (((2, 4),  (2, 4)),  ((1, 1), (1, 1)), fst.def_.first_formatting[0]),
    (((2, 6),  (2, 5)),  ((1, 1), (1, 0)), fst.def_.second_formatting),
    (((2, 7),  (2, 6)),  ((1, 1), (1, 0)), fst.def_.third_formatting),
    (((2, 7),  (2, 10)), ((1, 1), (1, 4)), fst.def_.arguments),
    (((2, 7),  (2, 7)),  ((1, 1), (1, 1)), fst.def_.arguments.node_list[0]),
    (((2, 8),  (2, 9)),  ((1, 1), (1, 2)), fst.def_.arguments.node_list[1]),
    (((2, 10), (2, 10)), ((1, 1), (1, 1)), fst.def_.arguments.node_list[2]),
    (((2, 11), (2, 10)), ((1, 1), (1, 0)), fst.def_.fourth_formatting),
    (((2, 12), (2, 11)), ((1, 1), (1, 0)), fst.def_.fifth_formatting),
    (((2, 13), (2, 12)), ((1, 1), (1, 0)), fst.def_.sixth_formatting),
    (((2, 13), (4, 0)),  ((1, 1), (3, 0)), fst.def_.value),
    (((2, 13), (3, 4)),  ((1, 1), (2, 4)), fst.def_.value.node_list[0]),
    (((3, 5),  (3, 13)), ((1, 1), (1, 9)), fst.def_.value.node_list[1]),
    (((3, 5),  (3, 5)),  ((1, 1), (1, 1)), fst.def_.value.node_list[1].target),
    (((3, 9),  (3, 13)), ((1, 1), (1, 5)), fst.def_.value.node_list[1].value),
    (((3, 9),  (3, 9)),  ((1, 1), (1, 1)), fst.def_.value.node_list[1].value.first),
    (((3, 13), (3, 13)), ((1, 1), (1, 1)), fst.def_.value.node_list[1].value.second),
    (((3, 14), (4, 0)),  ((1, 1), (2, 0)), fst.def_.value.node_list[2])
]

@pytest.fixture(params=bounding_boxes)
def bounding_box_fixture(request):
    return request.param

def test_bounding_box(bounding_box_fixture):
    absolute_bounding_box, bounding_box, node = bounding_box_fixture
    assert bounding_box == node.bounding_box
    assert absolute_bounding_box == node.absolute_bounding_box


def test_bounding_box_of_attribute(red):
    assert ((2, 1), (2, 3)) == red.def_.get_absolute_bounding_box_of_attribute("def")


def test_bounding_box_of_attribute_no_attribute(red):
    with pytest.raises(KeyError):
        red.def_.get_absolute_bounding_box_of_attribute("xxx")


def test_bounding_box_of_attribute_no_index(red):
    with pytest.raises(IndexError):
        red.get_absolute_bounding_box_of_attribute(1)

    with pytest.raises(IndexError):
        red.get_absolute_bounding_box_of_attribute(-1)


def test_bounding_box_empty():
    red = RedBaron("a()")
    assert ((1, 3), (1, 2)) == red.atomtrailers.value[1].value.absolute_bounding_box


RED = RedBaron("""\
class A:
    ''' Class docstring

    Class description
    '''
    attrA = [ a,
         b,
            c,
               d]

    def a(self):
        ''' Function a docstring

        Function description
        '''
        pass

    attrB = valB

    @myDecorator
    def b(self):
        ''' Function b docstring

        Function description
        '''
        pass

    attrC = [ a,
         b,
            c,
               d]\
""")


def test_bounding_box_with_proxy_list():
    assert ((1, 1), (32, 0)) == RED.absolute_bounding_box
    assert ((1, 1), (32, 0)) == RED.class_.absolute_bounding_box
    assert ((2, 5), (5, 7)) == RED.class_.value[0].absolute_bounding_box
    assert ((6, 5), (9, 17)) == RED.class_.value[1].absolute_bounding_box
    assert ((10, 1), (11, 4)) == RED.class_.value[2].absolute_bounding_box
    assert ((11, 5), (18, 4)) == RED.class_.value[3].absolute_bounding_box
    assert ((18, 5), (18, 16)) == RED.class_.value[4].absolute_bounding_box
    assert ((19, 1), (20, 4)) == RED.class_.value[5].absolute_bounding_box
    assert ((20, 5), (28, 4)) == RED.class_.value[6].absolute_bounding_box
    assert ((28, 5), (31, 17)) == RED.class_.value[7].absolute_bounding_box
    with pytest.raises(IndexError):
        RED.class_.value[8]


def test_bounding_box_of_attribute_with_proxy_list():
    assert ((1, 1), (32, 0)) == RED.absolute_bounding_box
    assert ((1, 1), (32, 0)) == RED.class_.absolute_bounding_box
    assert ((2, 5), (5, 7)) == RED.class_.value.get_absolute_bounding_box_of_attribute(0)
    assert ((6, 5), (9, 17)) == RED.class_.value.get_absolute_bounding_box_of_attribute(1)
    assert ((10, 1), (11, 4)) == RED.class_.value.get_absolute_bounding_box_of_attribute(2)
    assert ((11, 5), (18, 4)) == RED.class_.value.get_absolute_bounding_box_of_attribute(3)
    assert ((18, 5), (18, 16)) == RED.class_.value.get_absolute_bounding_box_of_attribute(4)
    assert ((19, 1), (20, 4)) == RED.class_.value.get_absolute_bounding_box_of_attribute(5)
    assert ((20, 5), (28, 4)) == RED.class_.value.get_absolute_bounding_box_of_attribute(6)
    assert ((28, 5), (31, 17)) == RED.class_.value.get_absolute_bounding_box_of_attribute(7)
    with pytest.raises(IndexError):
        RED.class_.value.get_absolute_bounding_box_of_attribute(8)
