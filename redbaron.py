import sys
import inspect
import itertools

from pygments import highlight
from pygments.token import Comment, Text, String, Keyword, Name, Operator
from pygments.lexer import RegexLexer, bygroups
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter

import baron
import baron.path
from baron.utils import python_version, string_instance
from baron.render import nodes_rendering_order


if python_version == 3:
    from collections import UserList
else:
    from UserList import UserList


def indent(line, indentation):
    return "\n".join(map(lambda x: indentation + x, line.split("\n")))


def to_node(node, parent=None, on_attribute=None):
    class_name = "".join(map(lambda x: x.capitalize(), node["type"].split("_"))) + "Node"
    if class_name in globals():
        return globals()[class_name](node, parent=parent, on_attribute=on_attribute)
    else:
        return type(class_name, (Node,), {})(node, parent=parent, on_attribute=on_attribute)


class Path(object):
    """Holds the path to a FST node

    Path(node): path coming from the node's root
    Path.from_baron_path(node, path): path going down the node following the given path

    Note that the second argument "path" is a baron path, i.e.
    created by baron.path.make_path() or
    redbaron.Path(node).to_baron_path()

    The second form is useful when converting a path given by baron
    to a redbaron node
    """

    def __init__(self, node):
        self.path = None
        self.node = None
        self.set_node(node)

    def set_node(self, node):
        self.node = node

        parent = Path.get_holder(node)
        if parent is None:
            self.path = baron.path.make_path()
            return

        parent_node_type = parent.type if isinstance(parent, Node) else 'list'
        render_pos, _ = Path.get_position_to_parent(node)

        path = []
        while parent is not None:
            _, key = Path.get_position_to_parent(parent)
            if key is not None:
                path.insert(0, key)
            parent = Path.get_holder(parent)

        self.path = baron.path.make_path(path, parent_node_type, render_pos)

    @classmethod
    def from_baron_path(class_, node, path):
        if baron.path.is_empty(path):
            return class_(node)

        for key in path.path:
            if isinstance(key, string_instance):
                node = getattr(node, key)
            else:
                node = node[key]

        if isinstance(node, NodeList):
            to_return = class_(node[path.position_in_rendering_list])
        else:
            to_return = class_(getattr(node, node._render()[path.position_in_rendering_list][1]))

        to_return.path = path
        return to_return

    def to_baron_path(self):
        return self.path

    @classmethod
    def get_holder(class_, node):
        if node.on_attribute is not None and isinstance(node.parent, Node):
            if getattr(node.parent, node.on_attribute) is not node:
                return getattr(node.parent, node.on_attribute)
        return node.parent

    @classmethod
    def get_position_to_parent(class_, node):
        parent = Path.get_holder(node)
        if parent is None:
            return (None, None)

        if isinstance(parent, NodeList):
            pos = parent.index(node)
            return (pos, pos)

        if isinstance(node, NodeList):
            return next((pos, key) for pos, (_, key, _) in enumerate(parent._render()) if getattr(parent, key) is node)

        return next((pos, key) for pos, (_, key, _) in enumerate(parent._render()) if key == node.on_attribute)


class GenericNodesUtils(object):
    # XXX should this be an abstract class?
    def _convert_input_to_node_object(self, value, parent, on_attribute):
        if isinstance(value, string_instance):
            return to_node(baron.parse(value)[0], parent=parent, on_attribute=on_attribute)
        elif isinstance(value, dict):
            return to_node(value, parent=parent, on_attribute=on_attribute)
        elif isinstance(value, Node):
            value.parent = parent
            value.on_attribute = on_attribute
            return value

        raise NotImplemented

    def _convert_input_to_node_object_list(self, value, parent, on_attribute):
        if isinstance(value, string_instance):
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), baron.parse(value)))

        if isinstance(value, dict):  # assuming that we got some fst
                                     # also assuming the user do strange things
            return NodeList([to_node(value, parent=parent, on_attribute=on_attribute)])

        if isinstance(value, Node):
            value.parent = parent
            value.on_attribute = on_attribute
            return [value]

        if isinstance(value, list) and not isinstance(value, NodeList):
            # assume the user can pass a list of random stuff
            new_value = NodeList()
            for i in value:
                new_value.append(self._convert_input_to_node_object(i, parent, on_attribute))

            return new_value

        raise NotImplemented


class NodeList(UserList, GenericNodesUtils):
    # NodeList doesn't have a previous nor a next
    # avoid common bug in shell by providing None
    next = None
    previous = None

    def __init__(self, initlist=None, parent=None, on_attribute=None):
        super(NodeList, self).__init__(initlist)
        self.parent = parent
        self.on_attribute = on_attribute

    def find(self, identifier, recursive=True, **kwargs):
        for i in self.data:
            candidate = i.find(identifier, recursive=recursive, **kwargs)
            if candidate is not None:
                return candidate

    def __getattr__(self, key):
        return self.find(key)

    def find_all(self, identifier, recursive=True, **kwargs):
        to_return = NodeList([])
        for i in self.data:
            to_return += i.find_all(identifier, recursive=recursive, **kwargs)
        return to_return

    findAll = find_all
    __call__ = find_all

    def find_by_path(self, path):
        return Path.from_baron_path(self, path).node

    def path(self):
        return Path(self)

    def fst(self):
        return [x.fst() for x in self.data]

    def dumps(self):
        return baron.dumps(self.fst())

    def __repr__(self):
        to_return = ""
        for number, value in enumerate(self.data):
            to_return += ("%-3s " % number) + "\n    ".join(value.__repr__().split("\n"))
            to_return += "\n"
        return to_return
        return "%s" % [x.__repr__() for x in self.data]

    def help(self, deep=2, with_formatting=False):
        for num, i in enumerate(self.data):
            sys.stdout.write(str(num) + " -----------------------------------------------------\n")
            i.help()

    def __help__(self, deep=2, with_formatting=False):
        return [x.__help__(deep=deep, with_formatting=with_formatting) for x in self.data]

    def copy(self):
        # XXX not very optimised but at least very simple
        return NodeList(map(to_node, self.fst()))

    def next_generator(self):
        # similary, NodeList will never have next items
        # trick to return an empty generator
        # I wonder if I should not raise instead :/
        return
        yield

    def previous_generator(self):
        # similary, NodeList will never have next items
        # trick to return an empty generator
        # I wonder if I should not raise instead :/
        return
        yield

    def apply(self, function):
        [function(x) for x in self.data]
        return self

    def map(self, function):
        return NodeList([function(x) for x in self.data])

    def filter(self, function):
        return NodeList([x for x in self.data if function(x)])

    def filtered(self):
        return tuple([x for x in self.data if not isinstance(x, (EndlNode, CommaNode, DotNode))])

    def append_comma(self, value, parent, on_attribute, trailing):
        "Generic function to append a value in a separated by comma list"
        if self.find("comma", recursive=False) and self.data[-1].type != "comma":
            comma = self.comma.copy()
            comma.parent = parent
            comma.on_attribute = on_attribute
            self.data.append(comma)

        elif self.find("comma", recursive=False) and self.data[-1].type == "comma":
            self.data[-1].second_formatting = {"type": "space", "value": " "}

        elif len(self.data) != 0:
            self.data.append(to_node({"type": "comma", "first_formatting": [], "second_formatting": [{"type": "space", "value": " "}]}, parent=parent, on_attribute=on_attribute))

        self.data.append(self._convert_input_to_node_object(value, parent, on_attribute))

        if trailing:
            self.data.append(to_node({"type": "comma", "first_formatting": [], "second_formatting": []}, parent=parent, on_attribute=on_attribute))

    def append_endl(self, value, parent, on_attribute):
        "Generic function to append a value in a separated by endl list"
        if self.filtered()[-1].indentation_node_is_direct() is False:
            # we are in this kind of case: while a: pass
            self.data.insert(0, to_node({
                "indent": self.filtered()[-1].indentation + "    ",
                "formatting": [],
                "type": "endl",
                "value": "\n",
            }, parent=parent, on_attribute=on_attribute))

        if not (self.data[-2].type == "endl" and self.data[-2].indent == self.filtered()[-1].get_indentation_node().indent):
            new_endl_node = self.filtered()[-1].get_indentation_node().copy()
            new_endl_node.parent = parent
            new_endl_node.on_attribute = on_attribute
            self.data.insert(-1, new_endl_node)

        self.data.insert(-1, self._convert_input_to_node_object(value, parent=parent, on_attribute=on_attribute))


class Node(GenericNodesUtils):
    _other_identifiers = []

    def __init__(self, node, parent=None, on_attribute=None):
        self.init = True
        self.parent = parent
        self.on_attribute = on_attribute
        self._str_keys = ["type"]
        self._list_keys = []
        self._dict_keys = []
        self.type = node["type"]
        for kind, key, _ in filter(lambda x: x[0] != "constant", self._render()):
            if kind == "key" and isinstance(node[key], (dict, type(None))):
                if node[key]:
                    setattr(self, key, to_node(node[key], parent=self, on_attribute=key))
                else:
                    setattr(self, key, None)
                self._dict_keys.append(key)

            elif kind == "bool" or (kind == "key" and isinstance(node[key], string_instance)):
                setattr(self, key, node[key])
                self._str_keys.append(key)

            elif kind in ("list", "formatting"):
                setattr(self, key, NodeList(map(lambda x: to_node(x, parent=self, on_attribute=key), node[key]), parent=self))
                self._list_keys.append(key)

            else:
                raise Exception(str((node["type"], kind, key)))

        self.init = False

    @property
    def next(self):
        in_list = self._get_list_attribute_is_member_off()

        if in_list is None:
            return None

        next_node = list(itertools.dropwhile(lambda x: x is not self, in_list))[1:]
        return next_node[0] if next_node else None

    def next_generator(self):
        in_list = self._get_list_attribute_is_member_off()

        if in_list is None:
            return None

        generator = itertools.dropwhile(lambda x: x is not self, in_list)
        next(generator)
        return generator

    @property
    def previous(self):
        in_list = self._get_list_attribute_is_member_off()

        if in_list is None:
            return None

        next_node = list(itertools.dropwhile(lambda x: x is not self, reversed(in_list)))[1:]
        return next_node[0] if next_node else None

    def previous_generator(self):
        in_list = self._get_list_attribute_is_member_off()

        if in_list is None:
            return None

        generator = itertools.dropwhile(lambda x: x is not self, reversed(in_list))
        next(generator)
        return generator

    def get_indentation_node(self):
        if self.on_attribute == "root":
            return None

        if self.type == "endl":
            # by convention, an endl node will always have this indentation
            return None

        if self.parent is None:
            # we have been copied and not parent is set yet
            return None

        if isinstance(getattr(self.parent, self.on_attribute), Node):
            return self.parent.get_indentation_node()

        # I'm 'pass' in this kind of situation:
        # if a: pass
        # (so I don't have a previous 'endl')
        if self.previous is None:
            return self.parent.get_indentation_node()

        if self.previous.type == "endl":
            return self.previous

        return self.previous.get_indentation_node()

    @property
    def indentation(self):
        endl_node = self.get_indentation_node()
        return endl_node.indent if endl_node is not None else ""

    def indentation_node_is_direct(self):
        if self.previous and self.previous.type == "endl":
            return True

        return False

    def _get_list_attribute_is_member_off(self):
        """
        Return the list attribute of the parent from which this node is a
        member.

        If this node isn't in a list attribute, return None.
        """
        if self.parent is None:
            return None

        if self.on_attribute is "root":
            in_list = self.parent
        else:
            in_list = getattr(self.parent, self.on_attribute)

        if not isinstance(in_list, NodeList):
            return None

        return in_list


    def find(self, identifier, recursive=True, **kwargs):
        if self._node_match_query(self, identifier, **kwargs):
            return self

        if not recursive:
            return None

        for kind, key, _ in filter(lambda x: x[0] == "list" or (x[0] == "key" and isinstance(getattr(self, x[1]), Node)), self._render()):
            if kind == "key":
                i = getattr(self, key)
                if not i:
                    continue

                found = i.find(identifier, recursive, **kwargs)
                if found:
                    return found

            elif kind == "list":
                for i in getattr(self, key):
                    found = i.find(identifier, recursive, **kwargs)
                    if found:
                        return found

            else:
                raise Exception()

    def __getattr__(self, key):
        return self.find(key)

    def find_all(self, identifier, recursive=True, **kwargs):
        to_return = NodeList([])
        if self._node_match_query(self, identifier, **kwargs):
            to_return.append(self)

        if not recursive:
            return to_return

        for kind, key, _ in filter(lambda x: x[0] == "list" or (x[0] == "key" and isinstance(getattr(self, x[1]), Node)), self._render()):
            if kind == "key":
                i = getattr(self, key)
                if not i:
                    continue

                to_return += i.find_all(identifier, recursive, **kwargs)

            elif kind == "list":
                for i in getattr(self, key):
                    to_return += i.find_all(identifier, recursive, **kwargs)

            else:
                raise Exception()

        return to_return

    findAll = find_all
    __call__ = find_all

    def parent_find(self, identifier, **kwargs):
        current = self
        while current.parent and current.on_attribute != 'root':
            if self._node_match_query(current.parent, identifier, **kwargs):
                return current.parent

            current = current.parent
        return None

    def _node_match_query(self, node, identifier, **kwargs):
        if identifier.lower() not in node._generate_identifiers():
            return False

        all_my_keys = node._str_keys + node._list_keys + node._dict_keys

        for key in kwargs:
            if key not in all_my_keys:
                return False

            if getattr(node, key) != kwargs[key]:
                return False

        return True

    def find_by_path(self, path):
        return Path(self, path).node()

    def path(self):
        return Path(self)

    def _generate_identifiers(self):
        return sorted(set(map(lambda x: x.lower(), [
            self.type,
            self.__class__.__name__,
            self.__class__.__name__.replace("Node", ""),
            self.type + "_"
        ] + self._other_identifiers)))

    def _get_helpers(self):
        not_helpers = set([
            'copy',
            'dumps',
            'find',
            'findAll',
            'find_all',
            'fst',
            'help',
            'next_generator',
            'previous_generator',
            'get_indentation_node',
            'indentation_node_is_direct',
            'parent_find',
            'path',
            'find_by_path'
        ])
        return [x for x in dir(self) if not x.startswith("_") and x not in not_helpers and inspect.ismethod(getattr(self, x))]

    def fst(self):
        to_return = {}
        for key in self._str_keys:
            to_return[key] = getattr(self, key)
        for key in self._list_keys:
            to_return[key] = [node.fst() for node in getattr(self, key)]
        for key in self._dict_keys:
            if getattr(self, key):
                to_return[key] = getattr(self, key).fst()
            else:
                to_return[key] = {}
        return to_return

    def dumps(self):
        return baron.dumps(self.fst())

    def help(self, deep=2, with_formatting=False):
        if runned_from_ipython():
            sys.stdout.write(highlight(self.__help__(deep=deep, with_formatting=with_formatting) + "\n", HelpLexer(), Terminal256Formatter(style='monokai')))
        else:
            sys.stdout.write(self.__help__(deep=deep, with_formatting=with_formatting) + "\n")

    def __help__(self, deep=2, with_formatting=False):
        new_deep = deep - 1 if not isinstance(deep, bool) else deep

        to_join = ["%s()" % self.__class__.__name__]

        if not deep:
            to_join[-1] += " ..."
        else:
            to_join.append("# identifiers: %s" % ", ".join(self._generate_identifiers()))
            if self._get_helpers():
                to_join.append("# helpers: %s" % ", ".join(self._get_helpers()))
            to_join += ["%s=%s" % (key, repr(getattr(self, key))) for key in self._str_keys if key != "type" and "formatting" not in key]
            to_join += ["%s ->\n    %s" % (key, indent(getattr(self, key).__help__(deep=new_deep, with_formatting=with_formatting), "    ").lstrip() if getattr(self, key) else getattr(self, key)) for key in self._dict_keys if "formatting" not in key]
            # need to do this otherwise I end up with stacked quoted list
            # example: value=[\'DottedAsNameNode(target=\\\'None\\\', as=\\\'False\\\', value=DottedNameNode(value=["NameNode(value=\\\'pouet\\\')"])]
            for key in filter(lambda x: "formatting" not in x, self._list_keys):
                to_join.append(("%s ->" % key))
                for i in getattr(self, key):
                    to_join.append("  * " + indent(i.__help__(deep=new_deep, with_formatting=with_formatting), "      ").lstrip())

        if deep and with_formatting:
            to_join += ["%s=%s" % (key, repr(getattr(self, key))) for key in self._str_keys if key != "type" and "formatting" in key]
            to_join += ["%s=%s" % (key, getattr(self, key).__help__(deep=new_deep, with_formatting=with_formatting) if getattr(self, key) else getattr(self, key)) for key in self._dict_keys if "formatting" in key]

            for key in filter(lambda x: "formatting" in x, self._list_keys):
                to_join.append(("%s ->" % key))
                for i in getattr(self, key):
                    to_join.append("  * " + indent(i.__help__(deep=new_deep, with_formatting=with_formatting), "      ").lstrip())

        return "\n  ".join(to_join)

    def __repr__(self):
        if runned_from_ipython():
            return highlight(self.dumps(), PythonLexer(encoding="Utf-8"),
                             Terminal256Formatter(style='monokai',
                                                  encoding="Utf-8"))
        else:
            return self.dumps()

    def copy(self):
        # XXX not very optimised but at least very simple
        return to_node(self.fst())

    def __setattr__(self, name, value):
        if name == "init" or self.init:
            return super(Node, self).__setattr__(name, value)

        # FIXME I'm pretty sure that Bool should also be put in the isinstance for cases like with_parenthesis/as
        # also, the int stuff won't scale to all number notations
        if name in self._str_keys and not isinstance(value, (string_instance, int)):
            value = str(value)

        elif name in self._dict_keys:
            value = self._convert_input_to_node_object(value, self, name)

        elif name in self._list_keys:
            value = self._convert_input_to_node_object_list(value, self, name)

        return super(Node, self).__setattr__(name, value)


    def _render(self):
        return nodes_rendering_order[self.type]


class IntNode(Node):
    def __init__(self, node, *args, **kwargs):
        super(IntNode, self).__init__(node, *args, **kwargs)
        self.value = int(self.value)

    def fst(self):
        return {
            "type": "int",
            "value": str(self.value),
            "section": "number",
        }


class EndlNode(Node):
    def __repr__(self):
        return repr(baron.dumps([self.fst()]))

class SpaceNode(Node):
    def __repr__(self):
        return repr(baron.dumps([self.fst()]))


class ImportNode(Node):
    def modules(self):
        "return a list of string of modules imported"
        return [x.value.dumps()for x in self('dotted_as_name')]

    def names(self):
        "return a list of string of new names inserted in the python context"
        return [x.target if x.target else x.value.dumps() for x in self('dotted_as_name')]


class ListNode(Node):
    append_value = lambda self, value, trailing=False: self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)


class SetNode(Node):
    append_value = lambda self, value, trailing=False: self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)


class ReprNode(Node):
    append_value = lambda self, value, trailing=False: self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)


class TupleNode(Node):
    def append_value(self, value, trailing=False):
        if len(self.value) == 0:
            # a tuple of one item must have a trailing comma
            self.value.append_comma(value, parent=self, on_attribute="value", trailing=True)
            return
        self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)


class DictNode(Node):
    def append_value(self, key, value, trailing=False):
        value = baron.parse("{%s: %s}" % (key, value))[0]["value"][0]
        self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)


class FuncdefNode(Node):
    _other_identifiers = ["def", "def_"]
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.sixth_formatting) == 1 and self.sixth_formatting[0].type == "space":
            self.sixth_formatting = []


class ForNode(Node):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.fifth_formatting) == 1 and self.fifth_formatting[0].type == "space":
            self.fifth_formatting = []


class WhileNode(Node):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.third_formatting) == 1 and self.third_formatting[0].type == "space":
            self.third_formatting = []


class ClassNode(Node):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.sixth_formatting) == 1 and self.sixth_formatting[0].type == "space":
            self.sixth_formatting = []


class WithNode(Node):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.third_formatting) == 1 and self.third_formatting[0].type == "space":
            self.third_formatting = []


class IfNode(Node):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.third_formatting) == 1 and self.third_formatting[0].type == "space":
            self.third_formatting = []


class ElifNode(Node):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.third_formatting) == 1 and self.third_formatting[0].type == "space":
            self.third_formatting = []


class ElseNode(Node):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.second_formatting) == 1 and self.second_formatting[0].type == "space":
            self.second_formatting = []


class TryNode(Node):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.second_formatting) == 1 and self.second_formatting[0].type == "space":
            self.second_formatting = []


class FinallyNode(Node):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.second_formatting) == 1 and self.second_formatting[0].type == "space":
            self.second_formatting = []


class ExceptNode(Node):
    def append_value(self, value):
        self.help(with_formatting=True)
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.fifth_formatting) == 1 and self.fifth_formatting[0].type == "space":
            self.fifth_formatting = []


class CommaNode(Node):
    pass


class DotNode(Node):
    pass


class CallNode(Node):
    def append_value(self, value, trailing=False):
        if isinstance(value, string_instance):
            value = baron.parse("a(%s)" % value)[0]["value"][1]["value"][0]
        self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)


class RedBaron(NodeList):
    def __init__(self, source_code):
        self.data = [to_node(x, parent=self, on_attribute="root") for x in baron.parse(source_code)]


# to avoid to have to declare EVERY node class, dynamically create the missings
# ones using nodes_rendering_order as a reference
for node_type in nodes_rendering_order:
    class_name = node_type.capitalize() + "Node"
    if class_name not in globals():
        globals()[class_name] = type(class_name, (Node,), {})


ipython_behavior = True
def runned_from_ipython():
    if not ipython_behavior:
        return False
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


class HelpLexer(RegexLexer):
    name = 'Lexer for RedBaron .help() method output'

    tokens = {
        'root': [
            (r"#.*$", Comment),
            (r"'[^']*'", String),
            (r"(None|False|True)", String),
            (r'(\*)( \w+Node)', bygroups(Operator, Keyword)),
            (r'\w+Node', Name.Function),
            (r'(\*|=|->|\(|\)|\.\.\.)', Operator),
            (r'\w+', Text),
            (r'\s+', Text),
        ]
    }
