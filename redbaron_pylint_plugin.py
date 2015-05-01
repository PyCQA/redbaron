#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" pylint helper plugin for validating RedBaron

Handles special cases like RedBaron's magic use of imports to create
missing nodes.
Taken in part from https://bitbucket.org/pfctdayelise/pylint-pytest/downloads
"""

from astroid import MANAGER
from astroid import nodes
from astroid.builder import AstroidBuilder

PYTEST_STUB = """
class marker(object):
    def __getattr__(self, name):
        return name

mark = marker()
"""

PLACEHOLDER_CLASS_STUB = """
class {name}(object):
    def __init__(self, *args, **kwargs):
        pass
"""

NODE_PLACEHOLDER_CLASS_STUB = """
class {name}(object):
    def __init__(self, node, *args, **kwargs):
        pass
"""


def pytest_transform(module):
    """ Let pylint know the pytest module """
    pytest = ('pytest', 'py.test')
    if module.name not in pytest:
        return

    astroid_mgr = AstroidBuilder(MANAGER)

    fake = astroid_mgr.string_build(PYTEST_STUB)
    for complex_stub in ('mark',):
        module.locals[complex_stub] = fake.locals[complex_stub]

    for stub in ('skip', 'xfail', 'fixture', 'test', 'raises'):
        text = PLACEHOLDER_CLASS_STUB.format(name=stub)
        fake = astroid_mgr.string_build(text)
        module.locals[stub] = fake.locals[stub]


def redbaron_transform(module):
    """ Let pylint know the redbaron module """
    if module.name != 'redbaron':
        return

    astroid_mgr = AstroidBuilder(MANAGER)

    fake = astroid_mgr.string_build(PYTEST_STUB)
    for stub in ('NameNode', 'PassNode'):
        text = NODE_PLACEHOLDER_CLASS_STUB.format(name=stub)
        fake = astroid_mgr.string_build(text)
        module.locals[stub] = fake.locals[stub]


def register(_):
    """ Registers this plugin to pylint

    pylint calls this function when loading
    """
    MANAGER.register_transform(nodes.Module, pytest_transform)
    MANAGER.register_transform(nodes.Module, redbaron_transform)

