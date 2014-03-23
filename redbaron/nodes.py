import sys
import baron
from types import ModuleType


def to_node(node):
    class_name = "".join(map(lambda x: x.capitalize(), node["type"].split("_"))) + "Node"
    if class_name in globals():
        return globals()[class_name](node)
    else:
        return type(class_name, (Node,), {})(node)


class Node(object):
    def __init__(self, node):
        self._str_keys = []
        self._list_keys = []
        self._dict_keys = []
        for key, value in node.items():
            if isinstance(value, dict):
                if value:
                    setattr(self, key, to_node(value))
                else:
                    setattr(self, key, None)
                self._dict_keys.append(key)
            elif isinstance(value, list):
                setattr(self, key, map(to_node, value))
                self._list_keys.append(key)
            else:
                setattr(self, key, value)
                self._str_keys.append(key)

    def __fst__(self):
        to_return = {}
        for key in self._str_keys:
            to_return[key] = getattr(self, key)
        for key in self._list_keys:
            to_return[key] = [node.__fst__() for node in getattr(self, key)]
        for key in self._dict_keys:
            if getattr(self, key):
                to_return[key] = getattr(self, key).__fst__()
            else:
                to_return[key] = {}
        return to_return

    def __repr__(self):
        return baron.dumps([self.__fst__()])


class IntNode(Node):
    def __init__(self, node):
        super(IntNode, self).__init__(node)
        self.value = int(self.value)


# enter the black magic realm, beware of what you might find
# (in fact that's pretty simple appart from the strange stuff needed)
# this basically allows to write code like:
# from redbaron.nodes import WatheverNode
# and a new class with Node has the parent will be created on the fly
# if this class doesn't already exist (like IntNode for example)
# while this is horribly black magic, this allows quite some cool stuff
class MissingNodesBuilder(dict):
    def __init__(self, globals, baked_args={}):
        self.globals = globals
        self.baked_args = baked_args

    def __getitem__(self, key):
        if key in self.globals:
            return self.globals[key]

        if key.endswith("Node"):
            new_node_class = type(key, (Node,), {})
            self.globals[key] = new_node_class
            return new_node_class


class BlackMagicImportHook(ModuleType):
    def __init__(self, self_module, baked_args={}):
        # this code is directly inspired by amoffat/sh
        # see https://github.com/amoffat/sh/blob/80af5726d8aa42017ced548abbd39b489068922a/sh.py#L1695
        for attr in ["__builtins__", "__doc__", "__name__", "__package__"]:
            setattr(self, attr, getattr(self_module, attr))

        # python 3.2 (2.7 and 3.3 work fine) breaks on osx (not ubuntu)
        # if we set this to None. and 3.3 needs a value for __path__
        self.__path__ = []
        self.self_module = self_module
        self._env = MissingNodesBuilder(globals(), baked_args)

    def __getattr__(self, name):
        return self._env[name]

    def __setattr__(self, name, value):
        if hasattr(self, "_env"):
            self._env[name] = value
        ModuleType.__setattr__(self, name, value)


self = sys.modules[__name__]
sys.modules[__name__] = BlackMagicImportHook(self)
