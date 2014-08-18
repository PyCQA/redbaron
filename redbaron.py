import re
import os
import sys
import inspect
import itertools

from fnmatch import fnmatch

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

    Note that the second argument "path" is a baron path, i.e. list of
    keys that can be given for example by
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

        parent = node
        path = []
        while parent is not None:
            key = Path.get_holder_on_attribute(parent)
            if key is not None:
                path.insert(0, key)
            parent = Path.get_holder(parent)

        self.path = path

    @classmethod
    def from_baron_path(class_, node, path):
        if path is None:
            return class_(node)

        for key in path:
            if isinstance(key, string_instance):
                child = getattr(node, key)
            else:
                child = node[key]
            if child is not None and isinstance(child, (Node, NodeList)):
                node = child

        return class_(node)

    def to_baron_path(self):
        return self.path

    @classmethod
    def get_holder(class_, node):
        if node.on_attribute is not None and isinstance(node.parent, Node):
            if getattr(node.parent, node.on_attribute) is not node:
                return getattr(node.parent, node.on_attribute)
        return node.parent

    @classmethod
    def get_holder_on_attribute(class_, node):
        parent = Path.get_holder(node)
        if parent is None:
            return None

        if isinstance(parent, NodeList):
            pos = parent.index(node)
            return pos

        if isinstance(node, NodeList):
            return next(key for (_, key, _) in parent._render() if getattr(parent, key) is node)

        return next(key for (_, key, _) in parent._render() if key == node.on_attribute)


class GenericNodesUtils(object):
    # XXX should this be an abstract class?
    def _convert_input_to_node_object(self, value, parent, on_attribute, generic=False):
        if isinstance(value, string_instance):
            if generic:
                return to_node(baron.parse(value)[0], parent=parent, on_attribute=on_attribute)
            else:
                return self._string_to_node(value, parent=parent, on_attribute=on_attribute)
        elif isinstance(value, dict):
            return to_node(value, parent=parent, on_attribute=on_attribute)
        elif isinstance(value, Node):
            value.parent = parent
            value.on_attribute = on_attribute
            return value

        raise NotImplemented

    def _string_to_node(self, string, parent, on_attribute):
        return to_node(baron.parse(string)[0], parent=parent, on_attribute=on_attribute)

    def _convert_input_to_node_object_list(self, value, parent, on_attribute):
        if isinstance(value, string_instance):
            return self._string_to_node_list(value, parent=parent, on_attribute=on_attribute)

        if isinstance(value, dict):  # assuming that we got some fst
                                     # also assuming the user do strange things
            return NodeList([to_node(value, parent=parent, on_attribute=on_attribute)])

        if isinstance(value, Node):
            value.parent = parent
            value.on_attribute = on_attribute
            return [value]

        if isinstance(value, NodeList):
            for i in value:
                i.parent = parent
                i.on_attribute = on_attribute
            return value

        if isinstance(value, list):
            # assume the user can pass a list of random stuff
            new_value = NodeList()
            for i in value:
                new_value.append(self._convert_input_to_node_object(i, parent, on_attribute))

            return new_value

        raise NotImplemented

    @property
    def bounding_box(self):
        return baron.path.node_to_bounding_box(self.fst())

    @property
    def absolute_bounding_box(self):
        path = self.path().to_baron_path()
        return baron.path.path_to_bounding_box(self.root.fst(), path)

    def find_by_position(self, line, column):
        return Path.from_baron_path(self, baron.path.position_to_path(self.fst(), line, column)).node

    def _string_to_node_list(self, string, parent, on_attribute):
        return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), baron.parse(string)))

    def parse_decorators(self, string, parent, on_attribute):
        indentation = self.indentation
        # XXX
        # This regex is bad because it could generate a bug in a very
        # rare case when a '@' with space before is inside an argument
        # of a decorator. This has extremly low chance to happen but
        # will probably drive crazy someone one day. This is a bad.

        # The way to solve this is not very simple. I think that the
        # 'perfect' solution would be use the tokenizer and to have
        # a mini parser that detect if the '@' is effectivly preceeded
        # by a space and remove it (the parser have to handle situation where
        # it is inside a call and outside to detect the good '@' since @ will
        # probably be a new operator in python in the futur)
        string = re.sub(" *@", "@", string)
        fst = baron.parse("%s\ndef a(): pass" % string.strip())[0]["decorators"]
        fst[-1]["indent"] = indentation
        result = NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))
        if indentation:
            # with re.sub they don't have indentation
            for i in filter(lambda x: x.type == "endl", result[1:-1]):
                i.indent = indentation

        return result

    @property
    def root(self):
        current = self
        while not isinstance(current, RedBaron):
            current = current.parent
        return current

    def _iter_in_rendering_order(self, node):
        if not isinstance(node, (Node, NodeList)):
            return
        if not (isinstance(node, Node) and node.type == "endl"):
            yield node
        for kind, key, display in node._render():
            if kind == "constant":
                yield node
            elif kind == "key":
                if isinstance(getattr(node, key), string_instance):
                    yield node
                    continue
                for i in self._iter_in_rendering_order(getattr(node, key)):
                    yield i
            elif kind in ("list", "formatting"):
                for i in getattr(node, key):
                    for j in self._iter_in_rendering_order(i):
                        yield j


class NodeList(UserList, GenericNodesUtils):
    # NodeList doesn't have a previous nor a next
    # avoid common bug in shell by providing None
    next = None
    previous = None

    def __init__(self, initlist=None, parent=None, on_attribute=None):
        super(NodeList, self).__init__(initlist)
        self.parent = parent
        self.on_attribute = on_attribute

    def find(self, identifier, *args, **kwargs):
        for i in self.data:
            candidate = i.find(identifier, *args, **kwargs)
            if candidate is not None:
                return candidate

    def __getattr__(self, key):
        return self.find(key)

    def __setitem__(self, key, value):
        self.data[key] = self._convert_input_to_node_object(value, parent=self.parent, on_attribute=self.on_attribute)

    def find_all(self, identifier, *args, **kwargs):
        to_return = NodeList([])
        for i in self.data:
            to_return += i.find_all(identifier, *args, **kwargs)
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
            i.help(deep=deep, with_formatting=with_formatting)

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

    def _generate_nodes_in_rendering_order(self):
        previous = None
        for i in self:
            for j in self._iter_in_rendering_order(i):
                if j is previous:
                    continue
                previous = j
                yield j

    def get_absolute_bounding_box_of_attribute(self, index):
        if index >= len(self.data) or index < 0:
            raise IndexError()
        path = self.path().to_baron_path() + [index]
        return baron.path.path_to_bounding_box(self.root.fst(), path)

    def increase_indentation(self, number_of_spaces):
        previous = None
        done = set()
        for i in self.data:
            for node in i._generate_nodes_in_rendering_order():
                if node.type != "endl" and previous is not None and previous.type == "endl" and previous not in done:
                    previous.indent += number_of_spaces * " "
                    done.add(previous)
                previous = node

    def decrease_indentation(self, number_of_spaces):
        previous = None
        done = set()
        for i in self.data:
            for node in i._generate_nodes_in_rendering_order():
                if node.type != "endl" and previous is not None and previous.type == "endl" and previous not in done:
                    previous.indent = previous.indent[number_of_spaces:]
                    done.add(previous)
                previous = node


class Node(GenericNodesUtils):
    _other_identifiers = []
    _default_test_value = "value"

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
                setattr(self, key, NodeList(map(lambda x: to_node(x, parent=self, on_attribute=key), node[key]), parent=self, on_attribute=key))
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

    @property
    def next_rendered(self):
        previous = None
        target = self.parent
        while target is not None:
            for i in reversed(list(target._generate_nodes_in_rendering_order())):
                if i is self and previous is not None:
                    return previous
                previous = i

            previous = None
            target = target.parent

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

    @property
    def previous_rendered(self):
        previous = None
        target = self.parent
        while target is not None:
            for i in target._generate_nodes_in_rendering_order():
                if i is self:
                    return previous
                previous = i

            target = target.parent

    def previous_generator(self):
        in_list = self._get_list_attribute_is_member_off()

        if in_list is None:
            return None

        generator = itertools.dropwhile(lambda x: x is not self, reversed(in_list))
        next(generator)
        return generator

    def get_indentation_node(self):
        if self.type == "endl":
            # by convention, an endl node will always have this indentation
            return None

        if self.previous_rendered is None:
            return None

        if self.previous_rendered.type == "endl":
            return self.previous_rendered

        return self.previous_rendered.get_indentation_node()

    @property
    def indentation(self):
        endl_node = self.get_indentation_node()
        return endl_node.indent if endl_node is not None else ""

    def indentation_node_is_direct(self):
        if self.previous_rendered and self.previous_rendered.type == "endl":
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


    def find(self, identifier, *args, **kwargs):
        if "recursive" in kwargs:
            recursive = kwargs["recursive"]
            kwargs = kwargs.copy()
            del kwargs["recursive"]
        else:
            recursive = True

        if self._node_match_query(self, identifier, *args, **kwargs):
            return self

        if not recursive:
            return None

        for kind, key, _ in filter(lambda x: x[0] == "list" or (x[0] == "key" and isinstance(getattr(self, x[1]), Node)), self._render()):
            if kind == "key":
                i = getattr(self, key)
                if not i:
                    continue

                found = i.find(identifier, *args, **kwargs)
                if found:
                    return found

            elif kind == "list":
                for i in getattr(self, key):
                    found = i.find(identifier, *args, **kwargs)
                    if found:
                        return found

            else:
                raise Exception()

    def __getattr__(self, key):
        return self.find(key)

    def find_all(self, identifier, *args, **kwargs):
        to_return = NodeList([])
        if "recursive" in kwargs:
            recursive = kwargs["recursive"]
            kwargs = kwargs.copy()
            del kwargs["recursive"]
        else:
            recursive = True

        if self._node_match_query(self, identifier, *args, **kwargs):
            to_return.append(self)

        if not recursive:
            return to_return

        for kind, key, _ in filter(lambda x: x[0] in ("list", "formatting") or (x[0] == "key" and isinstance(getattr(self, x[1]), Node)), self._render()):
            if kind == "key":
                i = getattr(self, key)
                if not i:
                    continue

                to_return += i.find_all(identifier, *args, **kwargs)

            elif kind in ("list", "formatting"):
                for i in getattr(self, key):
                    to_return += i.find_all(identifier, *args, **kwargs)

            else:
                raise Exception()

        return to_return

    findAll = find_all
    __call__ = find_all

    def parent_find(self, identifier, *args, **kwargs):
        current = self
        while current.parent and current.on_attribute != 'root':
            if self._node_match_query(current.parent, identifier, *args, **kwargs):
                return current.parent

            current = current.parent
        return None

    def _node_match_query(self, node, identifier, *args, **kwargs):
        if not self._attribute_match_query(node._generate_identifiers(), identifier.lower() if isinstance(identifier, string_instance) and not identifier.startswith("re:") else identifier):
            return False

        all_my_keys = node._str_keys + node._list_keys + node._dict_keys

        if args and isinstance(args[0], (string_instance, re._pattern_type, list, tuple)):
            if not self._attribute_match_query([getattr(node, node._default_test_value)], args[0]):
                return False
            args = args[1:]

        for arg in args:
            if not arg(node):
                return False

        for key, value in kwargs.items():
            if key not in all_my_keys:
                return False

            if not self._attribute_match_query([getattr(node, key)], value):
                return False

        return True

    def _attribute_match_query(self, attribute_names, query):
        """
        Take a list/tuple of attributes that can match and a query, return True
        if any of the attributes match the query.
        """
        assert isinstance(attribute_names, (list, tuple))

        if isinstance(query, string_instance) and query.startswith("re:"):
            query = re.compile(query[3:])

        for attribute in attribute_names:
            if callable(query):
                if query(attribute):
                    return True

            elif isinstance(query, string_instance) and query.startswith("g:"):
                if fnmatch(attribute, query[2:]):
                    return True

            elif isinstance(query, re._pattern_type):
                if query.match(attribute):
                    return True

            elif isinstance(query, (list, tuple)):
                if attribute in query:
                    return True
            else:
                if attribute == query:
                    return True

        return False


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
            'find_by_path',
            'replace',
            'edit',
            'increase_indentation',
            'decrease_indentation',
            'has_render_key',
            'get_absolute_bounding_box_of_attribute',
            'find_by_position',
            'parse_code_block',
            'parse_decorators',
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
            if self._default_test_value != "value":
                to_join.append("# default test value: %s" % self._default_test_value)
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

    def replace(self, new_node):
        new_node = self._convert_input_to_node_object(new_node, parent=None, on_attribute=None, generic=True)
        self.__class__ = new_node.__class__  # YOLO
        self.__init__(new_node.fst(), parent=self.parent, on_attribute=self.on_attribute)

    def edit(self, editor=None):
        if editor is None:
            editor = os.environ.get("EDITOR", "nano")

        base_path = os.path.join("/tmp", "baron_%s" % os.getpid())
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        temp_file_path = os.path.join(base_path, str(id(self)))

        self_in_string = self.dumps()
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(self_in_string)

        os.system("%s %s" % (editor, temp_file_path))

        with open(temp_file_path, "r") as temp_file:
            result = temp_file.read()

        if result != self_in_string:
            self.replace(result)

    @property
    def index(self):
        if not self.parent:
            return None

        if not isinstance(getattr(self.parent, self.on_attribute), NodeList):
            return None

        return getattr(self.parent, self.on_attribute).index(self)

    def _generate_nodes_in_rendering_order(self):
        previous = None
        for j in self._iter_in_rendering_order(self):
            if j is previous:
                continue
            previous = j
            yield j

    def has_render_key(self, target_key):
        for _, _, key in baron.render.render(self.fst()):
            if key == target_key:
                return True
        return False

    def get_absolute_bounding_box_of_attribute(self, attribute):
        if not self.has_render_key(attribute):
            raise KeyError()
        path = self.path().to_baron_path() + [attribute]
        return baron.path.path_to_bounding_box(self.root.fst(), path)

    def increase_indentation(self, number_of_spaces):
        self.get_indentation_node().indent += number_of_spaces * " "

    def decrease_indentation(self, number_of_spaces):
        self.get_indentation_node().indent -= number_of_spaces * " "


class CodeBlockNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            return self.parse_code_block(string, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def parse_code_block(self, string, parent, on_attribute):
        clean_string = re.sub("^ *\n", "", string) if "\n" in string else string
        indentation = len(re.search("^ *", clean_string).group())
        target_indentation = len(self.indentation) + 4

        # putting this in the string template will fail, need at least some indent
        if indentation == 0:
            clean_string = "    " + "\n    ".join(clean_string.split("\n"))
            clean_string = clean_string.rstrip()

        fst = baron.parse("def a():\n%s\n" % clean_string)[0]["value"]

        result = NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        # set indentation to the correct level
        indentation = len(result[0].indent)
        if indentation > target_indentation:
            result.decrease_indentation(indentation - target_indentation)
        elif indentation < target_indentation:
            result.increase_indentation(target_indentation - indentation)

        endl_base_node = to_node({'formatting': [], 'indent': '', 'type': 'endl', 'value': '\n'}, on_attribute=on_attribute, parent=parent)

        if (self.on_attribute == "root" and self.next) or (not self.next and self.parent.next):
            # I need to finish with 3 endl nodes
            if not all(map(lambda x: x.type == "endl", result[-1:])):
                result.append(endl_base_node.copy())
            elif not all(map(lambda x: x.type == "endl", result[-2:])):
                result.append(endl_base_node.copy())
                result.append(endl_base_node.copy())
            elif not all(map(lambda x: x.type == "endl", result[-3:])):
                result.append(endl_base_node.copy())
                result.append(endl_base_node.copy())
                result.append(endl_base_node.copy())
        elif self.next:
            # I need to finish with 2 endl nodes
            if not all(map(lambda x: x.type == "endl", result[-2:])):
                result.append(endl_base_node.copy())
            elif not all(map(lambda x: x.type == "endl", result[-3:])):
                result.append(endl_base_node.copy())
                result.append(endl_base_node.copy())

            result[-1].indent = self.indentation

        return result


class ElseAttributeNode(CodeBlockNode):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "else":
            if string.startswith("else"):
                return to_node(baron.parse("while s: pass\n%s" % string)[0]["else"], parent=parent, on_attribute=on_attribute)

            # XXX quite hackish way of doing this
            fst = {'first_formatting': [],
                   'second_formatting': [],
                   'type': 'else',
                   'value': [{'type': 'pass'},
                             {'formatting': [],
                              'indent': '',
                              'type': 'endl',
                              'value': '\n'}]
                  }

            else_node = to_node(fst, parent=parent, on_attribute=on_attribute)
            else_node.value = self.parse_code_block(string=string, parent=parent, on_attribute=on_attribute)

            return else_node

        else:
            raise Exception("Unhandled case")

    def __setattr__(self, name, value):
        if name == "else_":
            name = "else"

        return super(ElseAttributeNode, self).__setattr__(name, value)


class ArgumentGeneratorComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("(x %s)" % string)[0]["generators"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return to_node(baron.parse("(%s for x in x)" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class AssertNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("assert %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "message":
            if string:
                self.third_formatting = [to_node({"type": "space", "value": " "}, on_attribute=on_attribute, parent=parent)]
                return to_node(baron.parse("assert plop, %s" % string)[0]["message"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class AssignmentNode(Node):
    _other_identifiers = ["assign"]

    def __setattr__(self, key, value):
        if key == "operator":
            if len(value) == 2 and value[1] == "=":
                value = value[0]
            elif len(value) == 1 and value == "=":
                value = ""
            elif value is None:
                value = ""
            elif len(value) not in (0, 1, 2):
                raise Exception("The value of the operator can only be a string of one or two char, for eg: '+', '+=', '=', ''")

        return super(AssignmentNode, self).__setattr__(key, value)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "target":
            return to_node(baron.parse("%s = a" % string)[0]["target"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "value":
            return to_node(baron.parse("a = %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class AssociativeParenthesisNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("(%s)" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class AtomtrailersNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), baron.parse("(%s)" % string)[0]["value"]["value"]))

        else:
            raise Exception("Unhandled case")


class BinaryNode(Node):
    def __setattr__(self, key, value):
        if key == "value" and isinstance(value, string_instance):
            assert baron.parse(value)[0]["type"] == "binary"

        return super(BinaryNode, self).__setattr__(key, value)


class BinaryOperatorNode(Node):
    def __setattr__(self, key, value):
        if key == "value" and isinstance(value, string_instance):
            assert baron.parse("a %s b" % value)[0]["type"] == "binary_operator"

        return super(BinaryOperatorNode, self).__setattr__(key, value)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "first":
            return to_node(baron.parse("%s + b" % string)[0]["first"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "second":
            return to_node(baron.parse("bb + %s" % string)[0]["second"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class BooleanOperatorNode(Node):
    def __setattr__(self, key, value):
        if key == "value" and isinstance(value, string_instance):
            assert baron.parse("a %s b" % value)[0]["type"] == "boolean_operator"

        return super(BooleanOperatorNode, self).__setattr__(key, value)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "first":
            return to_node(baron.parse("%s and b" % string)[0]["first"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "second":
            return to_node(baron.parse("bb and %s" % string)[0]["second"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class CallNode(Node):
    def _convert_input_to_node_object_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), baron.parse("a(%s)" % string)[0]["value"][1]["value"]))

        else:
            raise Exception("Unhandled case")

    def append_value(self, value, trailing=False):
        if isinstance(value, string_instance):
            value = baron.parse("a(%s)" % value)[0]["value"][1]["value"][0]
        self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)


class CallArgumentNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("a(%s)" % string)[0]["value"][1]["value"][0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ClassNode(CodeBlockNode):
    _default_test_value = "name"

    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "decorators":
            return self.parse_decorators(string, parent=parent, on_attribute=on_attribute)

        elif on_attribute == "inherit_from":
            if string:
                self.parenthesis = True
            else:
                self.parenthesis = False

            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), baron.parse("class a(%s): pass" % string)[0]["inherit_from"]))

        else:
            return super(ClassNode, self)._string_to_node_list(string, parent, on_attribute)

    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.sixth_formatting) == 1 and self.sixth_formatting[0].type == "space":
            self.sixth_formatting = []


class CommaNode(Node):
    pass


class ComparisonNode(Node):
    def __setattr__(self, key, value):
        if key == "value" and isinstance(value, string_instance):
            assert baron.parse("a %s b" % value)[0]["type"] == "comparison"

        return super(ComparisonNode, self).__setattr__(key, value)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "first":
            return to_node(baron.parse("%s > b" % string)[0]["first"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "second":
            return to_node(baron.parse("bb > %s" % string)[0]["second"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ComprehensionIfNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("[x for x in x if %s]" % string)[0]["generators"][0]["ifs"][0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ComprehensionLoopNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "ifs":
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), baron.parse("[x for x in x %s]" % string)[0]["generators"][0]["ifs"]))

        else:
            return super(ClassNode, self)._string_to_node_list(string, parent, on_attribute)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "iterator":
            return to_node(baron.parse("[x for %s in x]" % string)[0]["generators"][0]["iterator"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "target":
            return to_node(baron.parse("[x for s in %s]" % string)[0]["generators"][0]["target"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DecoratorNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("@%s()\ndef a(): pass" % string)[0]["decorators"][0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "call":
            if string:
                return to_node(baron.parse("@a%s\ndef a(): pass" % string)[0]["decorators"][0]["call"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DefArgumentNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("def a(b=%s): pass" % string)[0]["arguments"][0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DelNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("del %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DictArgumentNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("a(**%s)" % string)[0]["value"][1]["value"][0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DictitemNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("{a: %s}" % string)[0]["value"][0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "key":
            return to_node(baron.parse("{%s: a}" % string)[0]["value"][0]["key"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DictNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("{%s}" % string)[0]["value"]
        return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

    def append_value(self, key, value, trailing=False):
        # XXX sucks, only accept key/value, not fst/rebaron instance
        value = baron.parse("{%s: %s}" % (key, value))[0]["value"][0]
        self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)


class DictComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("{x %s}" % string)[0]["generators"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return to_node(baron.parse("{%s for x in x}" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DotNode(Node):
    pass


class DottedAsNameNode(Node):
    def __setattr__(self, key, value):
        if key == "target":
            if not (re.match(r'^[a-zA-Z_]\w*$', value) or value in ("", None)):
                raise Exception("The target of a dotted as name node can only be a 'name' or an empty string or None")

            if value:
                self.first_formatting = [to_node({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
                self.second_formatting = [to_node({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]

        return super(DottedAsNameNode, self).__setattr__(key, value)

    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            fst = baron.parse("import %s" % string)[0]["value"][0]["value"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            raise Exception("Unhandled case")



class ElifNode(CodeBlockNode):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "test":
            return to_node(baron.parse("if %s: pass" % string)[0]["value"][0]["test"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.third_formatting) == 1 and self.third_formatting[0].type == "space":
            self.third_formatting = []


class ElseNode(CodeBlockNode):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.second_formatting) == 1 and self.second_formatting[0].type == "space":
            self.second_formatting = []


class EndlNode(Node):
    def __repr__(self):
        return repr(baron.dumps([self.fst()]))


class ExceptNode(CodeBlockNode):
    def __setattr__(self, key, value):
        if key == "delimiter":
            if value == ",":
                self.second_formatting = []
                self.third_formatting = [to_node({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
            elif value == "as":
                self.second_formatting = [to_node({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
                self.third_formatting = [to_node({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
            elif value:
                raise Exception("Delimiters of an except node can only be 'as' or ',' (without spaces around it).")

        return super(ExceptNode, self).__setattr__(key, value)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "exception":
            if string:
                self.first_formatting = [to_node({"type": "space", "value": " "}, on_attribute=on_attribute, parent=parent)]
                return to_node(baron.parse("try: pass\nexcept %s: pass" % string)[0]["excepts"][0]["exception"], parent=parent, on_attribute=on_attribute)
            else:
                self.first_formatting = []
                self.delimiter = ""
                self.target = ""
                return ""

        elif on_attribute == "target":
            if not self.exception:
                raise Exception("Can't set a target to an exception node that doesn't have an exception set")

            if string:
                self.delimiter = "as"
                self.second_formatting = [to_node({"type": "space", "value": " "}, on_attribute=on_attribute, parent=parent)]
                self.third_formatting = [to_node({"type": "space", "value": " "}, on_attribute=on_attribute, parent=parent)]
                return to_node(baron.parse("try: pass\nexcept a as %s: pass" % string)[0]["excepts"][0]["target"], parent=parent, on_attribute=on_attribute)

            else:
                self.delimiter = ""
                self.second_formatting = []
                self.third_formatting = []
                return ""

        else:
            raise Exception("Unhandled case")

    def append_value(self, value):
        self.help(with_formatting=True)
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.fifth_formatting) == 1 and self.fifth_formatting[0].type == "space":
            self.fifth_formatting = []


class ExecNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("exec %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "globals":
            if string:
                self.second_formatting = [{"type": "space", "value": " "}]
                self.third_formatting = [{"type": "space", "value": " "}]
                return to_node(baron.parse("exec a in %s" % string)[0]["globals"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "locals":
            if not self.globals:
                raise Exception("I can't set locals when globals aren't set.")

            if string:
                self.fifth_formatting = [{"type": "space", "value": " "}]
                return to_node(baron.parse("exec a in b, %s" % string)[0]["locals"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")



class FinallyNode(CodeBlockNode):
    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.second_formatting) == 1 and self.second_formatting[0].type == "space":
            self.second_formatting = []


class ForNode(CodeBlockNode):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "target":
            return to_node(baron.parse("for i in %s: pass" % string)[0]["target"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "iterator":
            return to_node(baron.parse("for %s in i: pass" % string)[0]["iterator"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.fifth_formatting) == 1 and self.fifth_formatting[0].type == "space":
            self.fifth_formatting = []


class FromImportNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "targets":
            fst = baron.parse("from a import %s" % string)[0]["targets"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        if on_attribute == "value":
            fst = baron.parse("from %s import s" % string)[0]["value"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            raise Exception("Unhandled case")


class FuncdefNode(CodeBlockNode):
    _other_identifiers = ["def", "def_"]
    _default_test_value = "name"

    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "arguments":
            fst = baron.parse("def a(%s): pass" % string)[0]["arguments"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        elif on_attribute == "decorators":
            return self.parse_decorators(string, parent=parent, on_attribute=on_attribute)

        else:
            return super(FuncdefNode, self)._string_to_node_list(string, parent, on_attribute)

    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.sixth_formatting) == 1 and self.sixth_formatting[0].type == "space":
            self.sixth_formatting = []


class GeneratorComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("(x %s)" % string)[0]["generators"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return to_node(baron.parse("(%s for x in x)" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class GetitemNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("a[%s]" % string)[0]["value"][1]["value"], parent=parent, on_attribute=on_attribute)


class GlobalNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            fst = baron.parse("global %s" % string)[0]["value"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            raise Exception("Unhandled case")


class IfNode(CodeBlockNode):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "test":
            return to_node(baron.parse("if %s: pass" % string)[0]["value"][0]["test"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.third_formatting) == 1 and self.third_formatting[0].type == "space":
            self.third_formatting = []


class ImportNode(Node):
    def modules(self):
        "return a list of string of modules imported"
        return [x.value.dumps()for x in self('dotted_as_name')]

    def names(self):
        "return a list of string of new names inserted in the python context"
        return [x.target if x.target else x.value.dumps() for x in self('dotted_as_name')]

    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("import %s" % string)[0]["value"]
        return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))


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


class LambdaNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "arguments":
            self.first_formatting = [{"type": "space", "value": " "}] if string else []
            fst = baron.parse("lambda %s: x" % string)[0]["arguments"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            return super(FuncdefNode, self)._string_to_node_list(string, parent, on_attribute)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("lambda: %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ListArgumentNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("lambda *%s: x" % string)[0]["arguments"][0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ListComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("[x %s]" % string)[0]["generators"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return to_node(baron.parse("[%s for x in x]" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ListNode(Node):
    append_value = lambda self, value, trailing=False: self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)

    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("[%s]" % string)[0]["value"]
        return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))


class NameAsNameNode(Node):
    def __setattr__(self, key, value):
        if key == "target":
            if not (re.match(r'^[a-zA-Z_]\w*$', value) or value in ("", None)):
                raise Exception("The target of a name as name node can only be a 'name' or an empty string or None")

            if value:
                self.first_formatting = [to_node({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
                self.second_formatting = [to_node({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]

        elif key == "value":
            if not (re.match(r'^[a-zA-Z_]\w*$', value) or value in ("", None)):
                raise Exception("The value of a name as name node can only be a 'name' or an empty string or None")

        return super(NameAsNameNode, self).__setattr__(key, value)


class PrintNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "destination":
            if string and not self.value:
                self.formatting = [{"type": "space", "value": " "}]
                return to_node(baron.parse("print >>%s" % string)[0]["destination"], parent=parent, on_attribute=on_attribute)

            elif string and self.value:
                self.formatting = [{"type": "space", "value": " "}]
                result = to_node(baron.parse("print >>%s" % string)[0]["destination"], parent=parent, on_attribute=on_attribute)
                if not self.value[0].type == "comma":
                    self.value = NodeList([to_node({"type": "comma", "second_formatting": [{"type": "space", "value": " "}], "first_formatting": []}, parent=parent, on_attribute=on_attribute)]) + self.value
                return result

            elif self.value and self.value[0].type == "comma":
                self.formatting = [{"type": "space", "value": " "}]
                self.value = self.value[1:]

            else:
                self.formatting = []

        else:
            raise Exception("Unhandled case")


    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            if string:
                self.formatting = [{"type": "space", "value": " "}]

                fst = baron.parse(("print %s" if not self.destination else "print >>a, %s") % string)[0]["value"]
                return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))
            else:
                self.formatting = [] if not string and not self.destination else [{"type": "space", "value": " "}]
                return NodeList()

        else:
            raise Exception("Unhandled case")


class RaiseNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            self.first_formatting = [{"type": "space", "value": " "}] if string else []
            if string:
                return to_node(baron.parse("raise %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "instance":
            if not self.value:
                raise Exception("Can't set instance if there is not value")

            if string:
                self.third_formatting = [{"type": "space", "value": " "}]
                return to_node(baron.parse("raise a, %s" % string)[0]["instance"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "traceback":
            if not self.instance:
                raise Exception("Can't set traceback if there is not instance")

            if string:
                self.fifth_formatting = [{"type": "space", "value": " "}]
                return to_node(baron.parse("raise a, b, %s" % string)[0]["traceback"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ReprNode(Node):
    append_value = lambda self, value, trailing=False: self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)

    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("`%s`" % string)[0]["value"]
        return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))


class ReturnNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            self.formatting = [{"type": "space", "value": " "}] if string else []
            if string:
                return to_node(baron.parse("return %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class SetNode(Node):
    append_value = lambda self, value, trailing=False: self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)

    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("{%s}" % string)[0]["value"]
        return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))


class SetComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("{x %s}" % string)[0]["generators"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return to_node(baron.parse("{%s for x in x}" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class SliceNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "lower":
            if string:
                return to_node(baron.parse("a[%s:]" % string)[0]["value"][1]["value"]["lower"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "upper":
            if string:
                return to_node(baron.parse("a[:%s]" % string)[0]["value"][1]["value"]["upper"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "step":
            self.has_two_colons = bool(string)
            if string:
                return to_node(baron.parse("a[::%s]" % string)[0]["value"][1]["value"]["step"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class SpaceNode(Node):
    def __repr__(self):
        return repr(baron.dumps([self.fst()]))


class StringChainNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            fst = baron.parse("a = %s" % string)[0]["value"]["value"]
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

        else:
            raise Exception("Unhandled case")


class TernaryOperatorNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "first":
            return to_node(baron.parse("%s if b else c" % string)[0]["first"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "second":
            return to_node(baron.parse("a if b else %s" % string)[0]["second"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "value":
            return to_node(baron.parse("a if %s else s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class TryNode(CodeBlockNode):
    def __getattr__(self, name):
        if name == "finally_":
            return getattr(self, "finally")

        return super(TryNode, self).__getattr__(name)

    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.second_formatting) == 1 and self.second_formatting[0].type == "space":
            self.second_formatting = []


class TupleNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("(%s)" % string)[0]["value"]
        return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), fst))

    def append_value(self, value, trailing=False):
        if len(self.value) == 0:
            # a tuple of one item must have a trailing comma
            self.value.append_comma(value, parent=self, on_attribute="value", trailing=True)
            return
        self.value.append_comma(value, parent=self, on_attribute="value", trailing=trailing)


class UnitaryOperatorNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "target":
            return to_node(baron.parse("-%s" % string)[0]["target"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class YieldNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            self.formatting = [{"type": "space", "value": " "}] if string else []
            if string:
                return to_node(baron.parse("yield %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class YieldAtomNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            self.second_formatting = [{"type": "space", "value": " "}] if string else []
            if string:
                return to_node(baron.parse("yield %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class WhileNode(ElseAttributeNode):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "test":
            return to_node(baron.parse("while %s: pass" % string)[0]["test"], parent=parent, on_attribute=on_attribute)

        else:
            return super(WhileNode, self)._string_to_node(string, parent, on_attribute)

    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.third_formatting) == 1 and self.third_formatting[0].type == "space":
            self.third_formatting = []


class WithContextItemNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return to_node(baron.parse("with %s: pass" % string)[0]["contexts"][0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "as":
            if string:
                self.first_formatting = [{"type": "space", "value": " "}]
                self.second_formatting = [{"type": "space", "value": " "}]
                return to_node(baron.parse("with a as %s: pass" % string)[0]["contexts"][0]["as"], parent=parent, on_attribute=on_attribute)
            else:
                self.first_formatting = []
                self.second_formatting = []
                return ""

        else:
            raise Exception("Unhandled case")

    def __getattr__(self, name):
        if name == "as_":
            return getattr(self, "as")

        return super(WithContextItemNode, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name == "as_":
            name = "as"

        return super(WithContextItemNode, self).__setattr__(name, value)


class WithNode(CodeBlockNode):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "contexts":
            return NodeList(map(lambda x: to_node(x, parent=parent, on_attribute=on_attribute), baron.parse("with %s: pass" % string)[0]["contexts"]))

        else:
            return super(WithNode, self)._string_to_node_list(string, parent, on_attribute)

    def append_value(self, value):
        self.value.append_endl(value, parent=self, on_attribute="value")
        if len(self.third_formatting) == 1 and self.third_formatting[0].type == "space":
            self.third_formatting = []


class RedBaron(NodeList):
    def __init__(self, source_code):
        if isinstance(source_code, string_instance):
            self.data = [to_node(x, parent=self, on_attribute="root") for x in baron.parse(source_code)]
        else:
            # Might be init from same object, or slice
            super(RedBaron, self).__init__(source_code)


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
            (r"('([^\\']|\\.)*'|\"([^\\\"]|\\.)*\")", String),
            (r"(None|False|True)", String),
            (r'(\*)( \w+Node)', bygroups(Operator, Keyword)),
            (r'\w+Node', Name.Function),
            (r'(\*|=|->|\(|\)|\.\.\.)', Operator),
            (r'\w+', Text),
            (r'\s+', Text),
        ]
    }
