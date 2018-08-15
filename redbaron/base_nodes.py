from __future__ import absolute_import

import re
import os
import sys
import ast
import inspect
import itertools

from fnmatch import fnmatch

import baron
import baron.path
from baron.utils import python_version, string_instance
from baron.render import nodes_rendering_order

import redbaron

from redbaron.utils import redbaron_classname_to_baron_type, baron_type_to_redbaron_classname, log, in_a_shell, indent, \
    truncate
from redbaron.private_config import runned_from_ipython
from redbaron.syntax_highlight import help_highlight, python_highlight, python_html_highlight

if python_version == 3:
    from collections import UserList
else:
    from UserList import UserList

# python 3.7 compatibility
RE_PATTERN_FIELD = re.Pattern if hasattr(re, "Pattern") else re._pattern_type


def display_property_atttributeerror_exceptions(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except AttributeError:
            import traceback
            traceback.print_exc()
            raise

    return wrapper


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
                child = getattr(node, key, None)
            else:
                if isinstance(node, ProxyList):
                    node = node.node_list

                if key >= len(node):
                    return None
                child = node[key]
            if child is not None and isinstance(child, (Node, NodeList, ProxyList)):
                node = child

        if isinstance(node, ProxyList):
            node = node.node_list

        return class_(node)

    def to_baron_path(self):
        return self.path

    def __str__(self):
        return 'Path(%s @ %s)' % (
            self.node.__class__.__name__ + ('(' + self.node.type + ')' if isinstance(self.node, Node) else ''),
            str(self.path))

    def __repr__(self):
        return '<' + self.__str__() + ' object at ' + str(id(self)) + '>'

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.to_baron_path() == other.to_baron_path()
        elif isinstance(other, list):
            return self.to_baron_path() == other
        else:
            return False

    @classmethod
    def get_holder(class_, node):
        if node.on_attribute is not None and isinstance(node.parent, Node):
            possible_parent = getattr(node.parent, node.on_attribute)
            if isinstance(possible_parent, ProxyList):
                if possible_parent.node_list is not node:
                    return possible_parent.node_list
            else:
                if possible_parent is not node:
                    return possible_parent
        return node.parent

    @classmethod
    def get_holder_on_attribute(class_, node):
        parent = Path.get_holder(node)
        if parent is None:
            return None

        if isinstance(parent, redbaron.RedBaron):
            parent = parent.node_list

        if isinstance(parent, NodeList):
            if isinstance(node, ProxyList):
                item = node.node_list
            else:
                item = node
            pos = parent.index(item)
            return pos

        if isinstance(node, NodeList):
            return next((key for (_, key, _) in parent._render() if
                         getattr(parent, key, None) is node or getattr(getattr(parent, key, None), "node_list",
                                                                       None) is node), None)

        to_return = next((key for (_, key, _) in parent._render() if key == node.on_attribute), None)
        return to_return


class LiteralyEvaluable(object):
    def to_python(self):
        try:
            return ast.literal_eval(self.dumps().strip())
        except ValueError as e:
            message = 'to_python method only works on numbers, strings, list, tuple, dict, boolean and None. (using ast.literal_eval). The piece of code that you are trying to convert contains an illegale value, for example, a variable.'
            e.message = message
            e.args = (message,)
            raise e


class GenericNodesUtils(object):
    """
    Mixen top class for Node and NodeList that contains generic methods that are used by both.
    """

    def _convert_input_to_node_object(self, value, parent, on_attribute, generic=False):
        if isinstance(value, string_instance):
            if generic:
                return Node.from_fst(baron.parse(value)[0], parent=parent, on_attribute=on_attribute)
            else:
                return self._string_to_node(value, parent=parent, on_attribute=on_attribute)
        elif isinstance(value, dict):
            return Node.from_fst(value, parent=parent, on_attribute=on_attribute)
        elif isinstance(value, Node):
            value.parent = parent
            value.on_attribute = on_attribute
            return value

        raise NotImplementedError

    def _string_to_node(self, string, parent, on_attribute):
        return Node.from_fst(baron.parse(string)[0], parent=parent, on_attribute=on_attribute)

    def _convert_input_to_node_object_list(self, value, parent, on_attribute):
        if isinstance(value, string_instance):
            return self._string_to_node_list(value, parent=parent, on_attribute=on_attribute)

        if isinstance(value, dict):  # assuming that we got some fst
            # also assuming the user do strange things
            return NodeList([Node.from_fst(value, parent=parent, on_attribute=on_attribute)])

        if isinstance(value, Node):
            value.parent = parent
            value.on_attribute = on_attribute
            return NodeList([value])

        if isinstance(value, (NodeList, ProxyList)):
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

        if isinstance(value, ProxyList):
            return value

        raise NotImplementedError

    @property
    @display_property_atttributeerror_exceptions
    def bounding_box(self):
        return baron.path.node_to_bounding_box(self.fst())

    @property
    @display_property_atttributeerror_exceptions
    def absolute_bounding_box(self):
        path = self.path().to_baron_path()
        return baron.path.path_to_bounding_box(self.root.fst(), path)

    def find_by_position(self, position):
        path = Path.from_baron_path(self, baron.path.position_to_path(self.fst(), position))
        return path.node if path else None

    def at(self, line_no):
        if not 0 <= line_no <= self.absolute_bounding_box.bottom_right.line:
            raise IndexError("Line number {0} is outside of the file".format(line_no))

        node = self.find_by_position((line_no, 1))

        if node.absolute_bounding_box.top_left.line == line_no:
            if hasattr(node.parent, 'absolute_bounding_box') and \
                            node.parent.absolute_bounding_box.top_left.line == line_no and \
                    node.parent.parent is not None:
                return node.parent

            return node

        elif node is not None and hasattr(node, 'next_rendered'):
            return list(self._iter_in_rendering_order(node.next_rendered))[0]

        elif node.parent is None:
            node = node.data[0][0]

            while True:
                if node.absolute_bounding_box.top_left.line == line_no:
                    return node
                node = node.next_rendered

        return node

    def _string_to_node_list(self, string, parent, on_attribute):
        return NodeList.from_fst(baron.parse(string), parent=parent, on_attribute=on_attribute)

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
        result = NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)
        if indentation:
            # with re.sub they don't have indentation
            for i in filter(lambda x: x.type == "endl", result[1:-1]):
                i.indent = indentation

        return result

    @property
    @display_property_atttributeerror_exceptions
    def root(self):
        current = self
        while not isinstance(current, redbaron.RedBaron):
            current = current.parent
        return current

    def _iter_in_rendering_order(self, node):
        if not isinstance(node, (Node, NodeList)):
            return
        if not (isinstance(node, Node) and node.type == "endl"):
            yield node
        for kind, key, display in node._render():
            if isinstance(display, string_instance) and not getattr(node, display):
                continue
            if kind == "constant":
                yield node
            elif kind == "string":
                if isinstance(getattr(node, key), string_instance):
                    yield node
            elif kind == "key":
                for i in self._iter_in_rendering_order(getattr(node, key)):
                    yield i
            elif kind in ("list", "formatting"):
                target = getattr(node, key)
                if isinstance(target, ProxyList):
                    target = target.node_list
                for i in target:
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

    @classmethod
    def from_fst(klass, node_list, parent=None, on_attribute=None):
        return klass(map(lambda x: Node.from_fst(x, parent=parent, on_attribute=on_attribute), node_list),
                     parent=parent, on_attribute=on_attribute)

    def find(self, identifier, *args, **kwargs):
        for i in self.data:
            candidate = i.find(identifier, *args, **kwargs)
            if candidate is not None:
                return candidate

    def __getattr__(self, key):
        if key not in redbaron.ALL_IDENTIFIERS:
            raise AttributeError(
                "%s instance has no attribute '%s' and '%s' is not a valid identifier of another node" % (
                    self.__class__.__name__, key, key))

        return self.find(key)

    def __setitem__(self, key, value):
        self.data[key] = self._convert_input_to_node_object(value, parent=self.parent, on_attribute=self.on_attribute)

    def find_iter(self, identifier, *args, **kwargs):
        for node in self.data:
            for matched_node in node.find_iter(identifier, *args, **kwargs):
                yield matched_node

    def find_all(self, identifier, *args, **kwargs):
        return NodeList(list(self.find_iter(identifier, *args, **kwargs)))

    findAll = find_all
    __call__ = find_all

    def find_by_path(self, path):
        path = Path.from_baron_path(self, path)
        return path.node if path else None

    def path(self):
        return Path(self)

    def fst(self):
        return [x.fst() for x in self.data]

    def dumps(self):
        return baron.dumps(self.fst())

    def __repr__(self):
        if in_a_shell():
            return self.__str__()

        return "<%s %s, \"%s\" %s, on %s %s>" % (
            self.__class__.__name__,
            self.path().to_baron_path(),
            truncate(self.dumps().replace("\n", "\\n"), 20),
            id(self),
            self.parent.__class__.__name__,
            id(self.parent)
        )

    def __str__(self):
        to_return = ""
        for number, value in enumerate(self.data):
            to_return += ("%-3s " % number) + "\n    ".join(value.__repr__().split("\n"))
            to_return += "\n"
        return to_return

    def _bytes_repr_html_(self):
        def __repr_html(self):
            # string addition is slow (and makes copies)
            yield b"<table>"
            yield b"<tr><th>Index</th><th>node</th></tr>"
            for num, item in enumerate(self):
                yield b"<tr>"
                yield b"<td>"
                yield str(num).encode("Utf-8")
                yield b"</td>"
                yield b"<td>"
                yield item._bytes_repr_html_() if hasattr(item, "_repr_html_") else str(item).encode("Utf-8")
                yield b"</td>"
                yield b"</tr>"
            yield b"</table>"

        return b''.join(__repr_html(self))

    def _repr_html_(self):
        return self._bytes_repr_html_().decode("Utf-8")

    def help(self, deep=2, with_formatting=False):
        for num, i in enumerate(self.data):
            sys.stdout.write(str(num) + " -----------------------------------------------------\n")
            i.help(deep=deep, with_formatting=with_formatting)

    def __help__(self, deep=2, with_formatting=False):
        return [x.__help__(deep=deep, with_formatting=with_formatting) for x in self.data]

    def copy(self):
        # XXX not very optimised but at least very simple
        return NodeList(map(Node.from_fst, self.fst()))

    def next_generator(self):
        # similary, NodeList will never have next items
        # trick to return an empty generator
        # I wonder if I should not raise instead :/
        return

    def previous_generator(self):
        # similary, NodeList will never have next items
        # trick to return an empty generator
        # I wonder if I should not raise instead :/
        return

    def apply(self, function):
        [function(x) for x in self.data]
        return self

    def map(self, function):
        return NodeList([function(x) for x in self.data])

    def filter(self, function):
        return NodeList([x for x in self.data if function(x)])

    def filtered(self):
        return tuple([x for x in self.data if
                      not isinstance(x, (redbaron.nodes.EndlNode, redbaron.nodes.CommaNode, redbaron.nodes.DotNode))])

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

    def __init__(self, fst, parent=None, on_attribute=None):
        self.init = True
        self.parent = parent
        self.on_attribute = on_attribute
        self._str_keys = ["type"]
        self._list_keys = []
        self._dict_keys = []
        self.type = fst["type"]

        for kind, key, _ in filter(lambda x: x[0] != "constant", self._render()):
            if kind == "key":
                if fst[key]:
                    setattr(self, key, Node.from_fst(fst[key], parent=self, on_attribute=key))
                else:
                    setattr(self, key, None)
                self._dict_keys.append(key)

            elif kind in ("bool", "string"):
                setattr(self, key, fst[key])
                self._str_keys.append(key)

            elif kind in ("list", "formatting"):
                setattr(self, key, NodeList.from_fst(fst[key], parent=self, on_attribute=key))
                self._list_keys.append(key)

            else:
                raise Exception(str((fst["type"], kind, key)))

        self.init = False

    @classmethod
    def from_fst(klass, node, parent=None, on_attribute=None):
        class_name = baron_type_to_redbaron_classname(node["type"])
        return getattr(redbaron.nodes, class_name)(node, parent=parent, on_attribute=on_attribute)

    @property
    @display_property_atttributeerror_exceptions
    def next(self):
        in_list = self._get_list_attribute_is_member_off()

        if in_list is None:
            return None

        next_node = list(itertools.dropwhile(lambda x: x is not self, in_list))[1:]
        return next_node[0] if next_node else None

    @property
    @display_property_atttributeerror_exceptions
    def next_intuitive(self):
        next_ = self.next

        if next_ and next_.type == "ifelseblock":
            return next_.if_

        return next_

    @property
    @display_property_atttributeerror_exceptions
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

    @property
    @display_property_atttributeerror_exceptions
    def next_recursive(self):
        target = self
        while not target.next:
            if not target.parent:
                break
            target = target.parent
        return target.next

    def next_generator(self):
        in_list = self._get_list_attribute_is_member_off()

        if in_list is None:
            return None

        generator = itertools.dropwhile(lambda x: x is not self, in_list)
        next(generator)
        return generator

    @property
    @display_property_atttributeerror_exceptions
    def previous(self):
        in_list = self._get_list_attribute_is_member_off()

        if in_list is None:
            return None

        next_node = list(itertools.dropwhile(lambda x: x is not self, reversed(in_list)))[1:]
        return next_node[0] if next_node else None

    @property
    @display_property_atttributeerror_exceptions
    def previous_intuitive(self):
        previous_ = self.previous

        if previous_ and previous_.type == "ifelseblock":
            return previous_.value[-1]

        elif previous_ and previous_.type == "try":
            if previous_.finally_:
                return previous_.finally_

            if previous_.else_:
                return previous_.else_

            if previous_.excepts:
                return previous_.excepts[-1]

        elif previous_ and previous_.type in ("for", "while"):
            if previous_.else_:
                return previous_.else_

        return previous_

    @property
    @display_property_atttributeerror_exceptions
    def previous_rendered(self):
        previous = None
        target = self.parent
        while target is not None:
            for i in target._generate_nodes_in_rendering_order():
                if i is self:
                    return previous
                previous = i

            target = target.parent

    @property
    @display_property_atttributeerror_exceptions
    def previous_recursive(self):
        target = self
        while not target.previous:
            if not target.parent:
                break
            target = target.parent
        return target.previous

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
    @display_property_atttributeerror_exceptions
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
        elif self.on_attribute is not None:
            if isinstance(self.parent, NodeList):
                in_list = getattr(self.parent.parent, self.on_attribute)
            else:
                in_list = getattr(self.parent, self.on_attribute)
        else:
            return None

        if isinstance(in_list, ProxyList):
            return in_list.node_list

        if not isinstance(in_list, NodeList):
            return None

        return in_list

    def __getattr__(self, key):
        if key.endswith("_") and key[:-1] in self._dict_keys + self._list_keys + self._str_keys:
            return getattr(self, key[:-1])

        if key != "value" and hasattr(self, "value") and isinstance(self.value, ProxyList) and hasattr(self.value, key):
            return getattr(self.value, key)

        if key not in redbaron.ALL_IDENTIFIERS:
            raise AttributeError(
                "%s instance has no attribute '%s' and '%s' is not a valid identifier of another node" % (
                    self.__class__.__name__, key, key))

        return self.find(key)

    def __getitem__(self, key):
        if hasattr(self, "value") and isinstance(self.value, ProxyList):
            return self.value[key]

        raise TypeError("'%s' object does not support indexing" % self.__class__)

    def __getslice__(self, i, j):
        if hasattr(self, "value") and isinstance(self.value, ProxyList):
            return self.value.__getslice__(i, j)

        raise AttributeError("__getslice__")

    def __setitem__(self, key, value):
        if hasattr(self, "value") and isinstance(self.value, ProxyList):
            self.value[key] = value

        else:
            raise TypeError("'%s' object does not support item assignment" % self.__class__)

    def __setslice__(self, i, j, value):
        if hasattr(self, "value") and isinstance(self.value, ProxyList):
            return self.value.__setslice__(i, j, value)

        raise TypeError("'%s' object does not support slice setting" % self.__class__)

    def __len__(self):
        if hasattr(self, "value") and isinstance(self.value, ProxyList):
            return self.value.__len__()

        # XXX bad, because __len__ exists, if will called to check if this object is True
        return True

    def __delitem__(self, key):
        if hasattr(self, "value") and isinstance(self.value, ProxyList):
            del self.value[key]

        else:
            raise AttributeError("__delitem__")

    def __delslice__(self, i, j):
        if hasattr(self, "value") and isinstance(self.value, ProxyList):
            self.value.__delslice__(i, j)

        else:
            raise AttributeError("__delitem__")

    def find_iter(self, identifier, *args, **kwargs):
        if "recursive" in kwargs:
            recursive = kwargs["recursive"]
            kwargs = kwargs.copy()
            del kwargs["recursive"]
        else:
            recursive = True

        if self._node_match_query(self, identifier, *args, **kwargs):
            yield self

        if recursive:
            for (kind, key, _) in self._render():
                if kind == "key":
                    node = getattr(self, key)
                    if not isinstance(node, Node):
                        continue
                    for matched_node in node.find_iter(identifier, *args, **kwargs):
                        yield matched_node
                elif kind in ("list", "formatting"):
                    nodes = getattr(self, key)
                    if isinstance(nodes, ProxyList):
                        nodes = nodes.node_list
                    for node in nodes:
                        for matched_node in node.find_iter(identifier, *args, **kwargs):
                            yield matched_node

    def find(self, identifier, *args, **kwargs):
        return next(self.find_iter(identifier, *args, **kwargs), None)

    def find_all(self, identifier, *args, **kwargs):
        return NodeList(list(self.find_iter(identifier, *args, **kwargs)))

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
        if not self._attribute_match_query(node.generate_identifiers(), identifier.lower() if isinstance(identifier,
                                                                                                         string_instance) and not identifier.startswith(
            "re:") else identifier):
            return False

        all_my_keys = node._str_keys + node._list_keys + node._dict_keys

        if args and isinstance(args[0], (string_instance, RE_PATTERN_FIELD, list, tuple)):
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

            elif isinstance(query, RE_PATTERN_FIELD):
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
        path = Path(self, path).node
        return path.node if path else None

    def path(self):
        return Path(self)

    @classmethod
    def generate_identifiers(klass):
        return sorted(set(map(lambda x: x.lower(), [
            redbaron_classname_to_baron_type(klass.__name__),
            klass.__name__,
            klass.__name__.replace("Node", ""),
            redbaron_classname_to_baron_type(klass.__name__) + "_"
        ] + klass._other_identifiers)))

    def _get_helpers(self):
        not_helpers = set([
            'at',
            'copy',
            'decrease_indentation',
            'dumps',
            'edit',
            'find',
            'find_all',
            'findAll',
            'find_by_path',
            'find_by_position',
            'find_iter',
            'from_fst',
            'fst',
            'fst',
            'generate_identifiers',
            'get_absolute_bounding_box_of_attribute',
            'get_indentation_node',
            'get_indentation_node',
            'has_render_key',
            'help',
            'help',
            'increase_indentation',
            'indentation_node_is_direct',
            'indentation_node_is_direct',
            'index_on_parent',
            'index_on_parent_raw',
            'insert_after',
            'insert_before',
            'next_generator',
            'next_generator',
            'parent_find',
            'parent_find',
            'parse_code_block',
            'parse_decorators',
            'path',
            'path',
            'previous_generator',
            'previous_generator',
            'replace',
            'to_python',
        ])
        return [x for x in dir(self) if
                not x.startswith("_") and x not in not_helpers and inspect.ismethod(getattr(self, x))]

    def fst(self):
        to_return = {}
        for key in self._str_keys:
            to_return[key] = getattr(self, key)
        for key in self._list_keys:
            # Proxy Lists overload __iter__ for a better user interface
            if isinstance(getattr(self, key), ProxyList):
                to_return[key] = [node.fst() for node in getattr(self, key).node_list]
            else:
                to_return[key] = [node.fst() for node in getattr(self, key)]
        for key in self._dict_keys:
            if getattr(self, key) not in (None, "", [], {}):
                to_return[key] = getattr(self, key).fst()
            else:
                to_return[key] = {}
        return to_return

    def dumps(self):
        return baron.dumps(self.fst())

    def help(self, deep=2, with_formatting=False):
        if runned_from_ipython():
            sys.stdout.write(help_highlight(self.__help__(deep=deep, with_formatting=with_formatting) + "\n"))
        else:
            sys.stdout.write(self.__help__(deep=deep, with_formatting=with_formatting) + "\n")

    def __help__(self, deep=2, with_formatting=False):
        new_deep = deep - 1 if not isinstance(deep, bool) else deep

        to_join = ["%s()" % self.__class__.__name__]

        if not deep:
            to_join[-1] += " ..."
        else:
            to_join.append("# identifiers: %s" % ", ".join(self.generate_identifiers()))
            if self._get_helpers():
                to_join.append("# helpers: %s" % ", ".join(self._get_helpers()))
            if self._default_test_value != "value":
                to_join.append("# default test value: %s" % self._default_test_value)
            to_join += ["%s=%s" % (key, repr(getattr(self, key))) for key in self._str_keys if
                        key != "type" and "formatting" not in key]
            to_join += ["%s ->\n    %s" % (key, indent(
                getattr(self, key).__help__(deep=new_deep, with_formatting=with_formatting),
                "    ").lstrip() if getattr(self, key) else getattr(self, key)) for key in self._dict_keys if
                        "formatting" not in key]
            # need to do this otherwise I end up with stacked quoted list
            # example: value=[\'DottedAsNameNode(target=\\\'None\\\', as=\\\'False\\\', value=DottedNameNode(value=["NameNode(value=\\\'pouet\\\')"])]
            for key in filter(lambda x: "formatting" not in x, self._list_keys):
                to_join.append(("%s ->" % key))
                for i in getattr(self, key):
                    to_join.append(
                        "  * " + indent(i.__help__(deep=new_deep, with_formatting=with_formatting), "      ").lstrip())

        if deep and with_formatting:
            to_join += ["%s=%s" % (key, repr(getattr(self, key))) for key in self._str_keys if
                        key != "type" and "formatting" in key]
            to_join += ["%s=%s" % (key, getattr(self, key).__help__(deep=new_deep,
                                                                    with_formatting=with_formatting) if getattr(self,
                                                                                                                key) else getattr(
                self, key)) for key in self._dict_keys if "formatting" in key]

            for key in filter(lambda x: "formatting" in x, self._list_keys):
                to_join.append(("%s ->" % key))
                for i in getattr(self, key):
                    to_join.append(
                        "  * " + indent(i.__help__(deep=new_deep, with_formatting=with_formatting), "      ").lstrip())

        return "\n  ".join(to_join)

    def __repr__(self):
        if in_a_shell():
            return self.__str__()

        return "<%s path=%s, \"%s\" %s, on %s %s>" % (
            self.__class__.__name__,
            self.path().to_baron_path(),
            truncate(self.dumps().replace("\n", "\\n"), 20),
            id(self),
            self.parent.__class__.__name__,
            id(self.parent)
        )

    def __str__(self):
        if runned_from_ipython():
            return python_highlight(self.dumps()).decode("Utf-8")
        else:
            return self.dumps()

    def _bytes_repr_html_(self):
        return python_html_highlight(self.dumps())

    def _repr_html_(self):
        return self._bytes_repr_html_().decode("Utf-8")

    def copy(self):
        # XXX not very optimised but at least very simple
        return Node.from_fst(self.fst())

    def __setattr__(self, name, value):
        if name == "init" or self.init:
            return super(Node, self).__setattr__(name, value)

        # we don't want to mess with "__class__" for example but convert "async_" to "async"
        if name.endswith("_") and not name.endswith("__"):
            name = name[:-1]

        # FIXME I'm pretty sure that Bool should also be put in the isinstance for cases like with_parenthesis/as
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
    @display_property_atttributeerror_exceptions
    def index_on_parent(self):
        if not self.parent:
            return None

        if not isinstance(getattr(self.parent, self.on_attribute), (NodeList, ProxyList)):
            return None

        return getattr(self.parent, self.on_attribute).index(self)

    @property
    @display_property_atttributeerror_exceptions
    def index_on_parent_raw(self):
        if not self.parent:
            return None

        if not isinstance(getattr(self.parent, self.on_attribute), (NodeList, ProxyList)):
            return None

        if isinstance(getattr(self.parent, self.on_attribute), ProxyList):
            return getattr(self.parent, self.on_attribute).node_list.index(self)
        else:
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
        self.get_indentation_node().indent = self.get_indentation_node().indent[:-len(number_of_spaces * " ")]

    def insert_before(self, value, offset=0):
        self.parent.insert(self.index_on_parent - offset, value)

    def insert_after(self, value, offset=0):
        self.parent.insert(self.index_on_parent + 1 + offset, value)


class CodeBlockNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            return self.parse_code_block(string, parent=parent, on_attribute=on_attribute)

        elif on_attribute.endswith("_formatting"):
            return super(CodeBlockNode, self)._string_to_node_list(string, parent, on_attribute)

        else:
            raise Exception("Unhandled case")

    def parse_code_block(self, string, parent, on_attribute):
        # remove heading blanks lines
        clean_string = re.sub("^ *\n", "", string) if "\n" in string else string
        indentation = len(re.search("^ *", clean_string).group())
        target_indentation = len(self.indentation) + 4

        # putting this in the string template will fail, need at least some indent
        if indentation == 0:
            clean_string = "    " + "\n    ".join(clean_string.split("\n"))
            clean_string = clean_string.rstrip()

        fst = baron.parse("def a():\n%s\n" % clean_string)[0]["value"]

        result = NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        # set indentation to the correct level
        indentation = len(result[0].indent)
        if indentation > target_indentation:
            result.decrease_indentation(indentation - target_indentation)
        elif indentation < target_indentation:
            result.increase_indentation(target_indentation - indentation)

        endl_base_node = Node.from_fst({'formatting': [], 'indent': '', 'type': 'endl', 'value': '\n'},
                                       on_attribute=on_attribute, parent=parent)

        if (self.on_attribute == "root" and self.next) or (not self.next and self.parent and self.parent.next):
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

    def __setattr__(self, key, value):
        super(CodeBlockNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, LineProxyList):
            setattr(self, "value", LineProxyList(self.value, on_attribute="value"))

        elif key == "decorators" and not isinstance(self.decorators, LineProxyList):
            setattr(self, "decorators", DecoratorsLineProxyList(self.decorators, on_attribute="decorators"))


class IfElseBlockSiblingNode(CodeBlockNode):
    @property
    @display_property_atttributeerror_exceptions
    def next_intuitive(self):
        next_ = super(IfElseBlockSiblingNode, self).next

        if next_ is None and self.parent:
            next_ = self.parent.next

        return next_

    @property
    @display_property_atttributeerror_exceptions
    def previous_intuitive(self):
        previous_ = super(IfElseBlockSiblingNode, self).previous

        if previous_ is None and self.parent:
            previous_ = self.parent.previous

        return previous_


class ElseAttributeNode(CodeBlockNode):
    def _get_last_member_to_clean(self):
        return self

    def _convert_input_to_one_indented_member(self, indented_type, string, parent, on_attribute):
        def remove_trailing_endl(node):
            if isinstance(node.value, ProxyList):
                while node.value.node_list[-1].type == "endl":
                    node.value.node_list.pop()
            else:
                while node.value[-1].type == "endl":
                    node.value.pop()

        if not string:
            last_member = self
            remove_trailing_endl(last_member)
            if isinstance(last_member.value, ProxyList):
                last_member.value.node_list.append(
                    redbaron.nodes.EndlNode({"type": "endl", "indent": "", "formatting": [], "value": "\n"},
                                            parent=last_member, on_attribute="value"))
            else:
                last_member.value.append(
                    redbaron.nodes.EndlNode({"type": "endl", "indent": "", "formatting": [], "value": "\n"},
                                            parent=last_member, on_attribute="value"))
            return ""

        if re.match("^\s*%s" % indented_type, string):

            # we've got indented text, let's deindent it
            if string.startswith((" ", "	")):
                # assuming that the first spaces are the indentation
                indentation = len(re.search("^ +", string).group())
                string = re.sub("(\r?\n)%s" % (" " * indentation), "\\1", string)
                string = string.lstrip()

            node = Node.from_fst(baron.parse("try: pass\nexcept: pass\n%s" % string)[0][indented_type], parent=parent,
                                 on_attribute=on_attribute)
            node.value = self.parse_code_block(node.value.dumps(), parent=node, on_attribute="value")

        else:
            # XXX quite hackish way of doing this
            fst = {'first_formatting': [],
                   'second_formatting': [],
                   'type': indented_type,
                   'value': [{'type': 'pass'},
                             {'formatting': [],
                              'indent': '',
                              'type': 'endl',
                              'value': '\n'}]
                   }

            node = Node.from_fst(fst, parent=parent, on_attribute=on_attribute)
            node.value = self.parse_code_block(string=string, parent=parent, on_attribute=on_attribute)

        # ensure that the node ends with only one endl token, we'll add more later if needed
        remove_trailing_endl(node)
        node.value.node_list.append(
            redbaron.nodes.EndlNode({"type": "endl", "indent": "", "formatting": [], "value": "\n"}, parent=node,
                                    on_attribute="value"))

        last_member = self._get_last_member_to_clean()

        # XXX this risk to remove comments
        if self.next:
            remove_trailing_endl(last_member)
            if isinstance(last_member.value, ProxyList):
                last_member.value.node_list.append(
                    redbaron.nodes.EndlNode({"type": "endl", "indent": "", "formatting": [], "value": "\n"},
                                            parent=last_member, on_attribute="value"))
            else:
                last_member.value.append(
                    redbaron.nodes.EndlNode({"type": "endl", "indent": "", "formatting": [], "value": "\n"},
                                            parent=last_member, on_attribute="value"))

            if self.indentation:
                node.value.node_list.append(redbaron.nodes.EndlNode(
                    {"type": "endl", "indent": self.indentation, "formatting": [], "value": "\n"}, parent=node,
                    on_attribute="value"))
            else:  # we are on root level and followed: we need 2 blanks lines after the node
                node.value.node_list.append(
                    redbaron.nodes.EndlNode({"type": "endl", "indent": "", "formatting": [], "value": "\n"},
                                            parent=node, on_attribute="value"))
                node.value.node_list.append(
                    redbaron.nodes.EndlNode({"type": "endl", "indent": "", "formatting": [], "value": "\n"},
                                            parent=node, on_attribute="value"))

        if isinstance(last_member.value, ProxyList):
            last_member.value.node_list[-1].indent = self.indentation
        else:
            last_member.value[-1].indent = self.indentation

        return node

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute != "else":
            return super(ElseAttributeNode, self)._string_to_node(string, parent=parent, on_attribute=on_attribute)

        return self._convert_input_to_one_indented_member("else", string, parent, on_attribute)

    def __setattr__(self, name, value):
        if name == "else_":
            name = "else"

        return super(ElseAttributeNode, self).__setattr__(name, value)


class ProxyList(object):
    def __init__(self, node_list, on_attribute="value"):
        self.node_list = node_list
        self.heading_formatting = []
        self.data = self._build_inner_list(node_list)
        self.middle_separator = redbaron.nodes.CommaNode(
            {"type": "comma", "first_formatting": [], "second_formatting": [{"type": "space", "value": " "}]})
        self.on_attribute = on_attribute

    def _build_inner_list(self, node_list):
        result = []

        for i in node_list:
            if isinstance(i, (redbaron.nodes.EndlNode, redbaron.nodes.CommaNode, redbaron.nodes.DotNode)):
                if result:
                    result[-1][1].append(i)
                else:
                    self.heading_formatting.append(i)
            else:
                result.append([i, []])

        return result

    def __call__(self, identifier, *args, **kwargs):
        return self.node_list.find_all(identifier, *args, **kwargs)

    def _convert_input_to_node_object(self, value, parent, on_attribute):
        lst = self.node_list.parent._convert_input_to_node_object_list(value, parent, on_attribute)
        if all(i.type == 'endl' for i in lst):
            return lst[0]
        else:
            return lst.filtered()[0]

    def _convert_input_to_node_object_list(self, value, parent, on_attribute):
        if isinstance(value, string_instance):
            return self.node_list.parent._convert_input_to_node_object_list(value, parent, on_attribute)
        else:
            return NodeList([self._convert_input_to_node_object(x, parent, on_attribute) for x in value])

    def _generate_expected_list(self):
        expected_list = self.heading_formatting[:]

        for position, i in enumerate(self.data):
            is_last = position == len(self.data) - 1
            expected_list.append(i[0])
            # XXX this will need refactoring...
            if i[1] is not None:
                # here we encounter a middle value that should have formatting
                # to separate between the intems but has not so we add it
                # this happen because a new value has been added after this one
                if not is_last and not i[1]:
                    separator = self.middle_separator.copy()
                    separator.parent = self.node_list
                    separator.on_attribute = self.on_attribute
                    expected_list.append(separator)

                # XXX shoud uniformise the list of formatting nodes
                elif is_last and i[1] and i[1][0].type in ("comma", "dot"):
                    # XXX this will likely break comments if presents at the end of the list
                    pass
                else:
                    expected_list += i[1]
            else:
                # here we generate the new expected formatting
                # None is used as a sentry value for newly inserted values in the proxy list
                if not is_last:
                    separator = self.middle_separator.copy()
                    separator.parent = self.node_list
                    separator.on_attribute = self.on_attribute
                    expected_list.append(separator)

        return expected_list

    def _synchronise(self):
        self.node_list.data = self._generate_expected_list()[:]
        self.data = self._build_inner_list(self.node_list.data)

    def __len__(self):
        return len(self.data)

    def insert(self, index, value):
        value = self._convert_input_to_node_object(value, parent=self.node_list, on_attribute=self.on_attribute)
        self.data.insert(index, [value, None])
        self._synchronise()

    def append(self, value):
        self.insert(len(self), value)

    def extend(self, values):
        self.data.extend(map(lambda x: [x, None], self._convert_input_to_node_object_list(values, parent=self.node_list,
                                                                                          on_attribute=self.on_attribute)))
        self._synchronise()

    def pop(self, index=None):
        if index is not None:
            self.data.pop(index)
        else:
            self.data.pop()
        self._synchronise()

    def remove(self, value):
        self.pop(self.index(value))

    def __delitem__(self, index):
        if isinstance(index, slice):
            self.__delslice__(index.start, index.stop)
        else:
            self.pop(index)

    def index(self, value, *args):
        # XXX would be better if I iterate other the list
        return [x[0] for x in self.data].index(value, *args)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__getslice__(index.start, index.stop)
        else:
            return self.data[index][0]

    def __contains__(self, *args, **kwargs):
        return self.data.__contains__(*args, **kwargs)

    def __iter__(self):
        return map(lambda x: x[0], self.data).__iter__()

    def count(self, value):
        return [x[0] for x in self.data].count(value)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            self.__setslice__(key.start, key.stop, value)
        else:
            self.data[key][0] = self._convert_input_to_node_object(value, parent=self.node_list,
                                                                   on_attribute=self.on_attribute)
        self._synchronise()

    def __setslice__(self, i, j, value):
        self.data[i:j] = map(lambda x: [x, None], self._convert_input_to_node_object_list(value, parent=self.node_list,
                                                                                          on_attribute=self.on_attribute))
        self._synchronise()

    def __delslice__(self, i, j):
        del self.data[i:j]
        self._synchronise()

    def __getslice__(self, i, j):
        to_return = map(lambda x: x[0], self.data[i:j])
        return self.__class__(NodeList(to_return))

    def __repr__(self):
        if in_a_shell():
            return self.__str__()

        return "<%s %s, \"%s\" %s, on %s %s>" % (
            self.__class__.__name__,
            self.path().to_baron_path(),
            truncate(self.dumps().replace("\n", "\\n"), 20),
            id(self),
            self.parent.__class__.__name__,
            id(self.parent)
        )

    def _bytes_repr_html_(self):
        def __repr_html(self):
            # string addition is slow (and makes copies)
            yield b"<table>"
            yield b"<tr><th>Index</th><th>node</th></tr>"
            for num, item in enumerate(self):
                yield b"<tr>"
                yield b"<td>"
                yield str(num).encode("Utf-8")
                yield b"</td>"
                yield b"<td>"
                yield item._bytes_repr_html_()
                yield b"</td>"
                yield b"</tr>"
            yield b"</table>"

        return b''.join(__repr_html(self))

    def _repr_html_(self):
        return self._bytes_repr_html_().decode("Utf-8")

    def __str__(self):
        to_return = ""
        for number, value in enumerate(self.data):
            value = value[0]
            to_return += (("%-3s " % number) + "\n    ".join(value.__repr__().split("\n")))
            to_return += "\n"
        return to_return

    def __getattr__(self, key):
        return getattr(self.node_list, key)


class CommaProxyList(ProxyList):
    def __init__(self, node_list, on_attribute="value"):
        super(CommaProxyList, self).__init__(node_list, on_attribute=on_attribute)
        self.style = "indented" if any(self.node_list('comma', recursive=False).map(lambda x: x('endl'))) else "flat"

        # XXX will likely break if the user modify the formatting of the list,
        # I don't like that
        self.has_trailing = self.node_list and self.node_list[-1].type == "comma"

    def _get_middle_separator(self):
        if self.style == "indented":
            return redbaron.nodes.CommaNode({"type": "comma", "first_formatting": [], "second_formatting": [
                {"type": "endl", "indent": self.parent.indentation + "    ", "formatting": [], "value": "\n"}]})

        return redbaron.nodes.CommaNode(
            {"type": "comma", "first_formatting": [], "second_formatting": [{"type": "space", "value": " "}]})

    def _generate_expected_list(self):
        def generate_separator():
            separator = self._get_middle_separator()
            separator.parent = self.node_list
            separator.on_attribute = self.on_attribute
            return separator

        # XXX will break comments
        if not self.data:
            self.parent.first_formatting = []
            self.parent.second_formatting = []
            return []

        expected_list = []

        for position, i in enumerate(self.data):
            is_last = position == len(self.data) - 1
            expected_list.append(i[0])
            # XXX this will need refactoring...
            if i[1] is not None:
                # here we encounter a middle value that should have formatting
                # to separate between the intems but has not so we add it
                # this happen because a new value has been added after this one
                if not is_last and not i[1]:
                    expected_list.append(generate_separator())

                # comma list doesn't have trailing but has a comma at its end, remove it
                elif is_last and not self.has_trailing and i[1] and i[1][0].type == "comma":
                    # XXX this will likely break comments if presents at the end of the list
                    pass
                else:
                    expected_list += i[1]

                    # XXX will break comments
                    if self.style == "indented":
                        if not expected_list[-1].second_formatting.endl:
                            raise Exception(
                                "It appears that you have indentation in your CommaList, for now RedBaron doesn't know how to handle this situation (which requires a lot of work), sorry about that. You can find more information here https://github.com/PyCQA/redbaron/issues/100")
                        elif expected_list[-1].second_formatting.endl.indent != self.parent.indentation + " " * 4:
                            expected_list[-1].second_formatting.endl.indent = self.parent.indentation + " " * 4
            else:
                # here we generate the new expected formatting
                # None is used as a sentry value for newly inserted values in the proxy list
                if not is_last:
                    expected_list.append(generate_separator())
                elif self.has_trailing:
                    expected_list.append(generate_separator())
                    expected_list[-1].second_formatting[0].indent = ""

        if expected_list and self.has_trailing and self.style == "indented":
            if not expected_list[-1].second_formatting.endl:
                raise Exception(
                    "It appears that you have indentation in your CommaList, for now RedBaron doesn't know how to handle this situation (which requires a lot of work), sorry about that. You can find more information here https://github.com/PyCQA/redbaron/issues/100")
            elif expected_list[-1].second_formatting.endl.indent != self.parent.indentation:
                expected_list[-1].second_formatting.endl.indent = self.parent.indentation

        return expected_list


class DotProxyList(ProxyList):
    def __init__(self, node_list, on_attribute="value"):
        # XXX this will have its limitations, users will probably wants to be
        # able to modify those, DotProxyList should be reconsidered for that
        super(DotProxyList, self).__init__(node_list, on_attribute=on_attribute)
        self.middle_separator = redbaron.nodes.DotNode({"type": "dot", "first_formatting": [], "second_formatting": []})

    def _build_inner_list(self, node_list):
        # XXX to merge with parent, behavior is the same only formatting nodes changes
        result = []

        for i in node_list:
            if isinstance(i, redbaron.nodes.DotNode):
                if not result:
                    self.heading_formatting.append(i)
                else:
                    result[-1][1].append(i)
            else:
                result.append([i, []])

        return result

    def _generate_expected_list(self):
        expected_list = self.heading_formatting[:]

        for position, i in enumerate(self.data):
            if expected_list and i[0].type in ("call", "getitem"):
                expected_list.pop()

            is_last = position == len(self.data) - 1
            expected_list.append(i[0])
            # XXX this will need refactoring...
            if i[1] is not None:
                # here we encounter a middle value that should have formatting
                # to separate between the items but has not so we add it
                # this happen because a new value has been added after this one
                if not is_last and not i[1]:
                    separator = self.middle_separator.copy()
                    separator.parent = self.node_list
                    separator.on_attribute = self.on_attribute
                    expected_list.append(separator)

                # XXX shoud uniformise the list of formatting nodes
                elif is_last and i[1] and i[1][0].type in ("comma", "dot"):
                    # XXX this will likely break comments if presents at the end of the list
                    pass
                else:
                    expected_list += i[1]
            else:
                # here we generate the new expected formatting
                # None is used as a sentry value for newly inserted values in the proxy list
                if not is_last:
                    separator = self.middle_separator.copy()
                    separator.parent = self.node_list
                    separator.on_attribute = self.on_attribute
                    expected_list.append(separator)

        return expected_list

    def _convert_input_to_node_object(self, value, parent, on_attribute):
        if value.startswith(("(", "[")):
            value = "a%s" % value
        else:
            value = "a.%s" % value

        return self.node_list.parent._convert_input_to_node_object_list(value, parent, on_attribute).filtered()[-1]


class LineProxyList(ProxyList):
    def __init__(self, node_list, on_attribute="value"):
        self.first_blank_lines = []
        super(LineProxyList, self).__init__(node_list, on_attribute=on_attribute)
        self.middle_separator = redbaron.nodes.DotNode(
            {"type": "endl", "formatting": [], "value": "\n", "indent": "    "})

    def _synchronise(self):
        log("Before synchronise, self.data = '%s' + '%s'", self.first_blank_lines, self.node_list)
        super(LineProxyList, self)._synchronise()
        log("After synchronise, self.data = '%s' + '%s'", self.first_blank_lines, self.node_list)

    def _build_inner_list(self, node_list):
        result = []
        self.first_blank_lines = []

        previous = None
        still_at_beginning = False
        for i in node_list:
            if i.type != "endl":
                result.append([i, []])
                still_at_beginning = False
            elif previous and previous.type == "endl":
                result.append([i, []])
                still_at_beginning = False
            elif still_at_beginning and self.first_blank_lines:
                result.append([i, []])
                still_at_beginning = False
            else:
                if result:
                    result[-1][1].append(i)
                    still_at_beginning = False
                else:
                    self.first_blank_lines.append(i)
                    still_at_beginning = True

            if still_at_beginning:
                previous = None
            else:
                previous = i

        return result

    def _get_separator_indentation(self):
        return self.node_list.filtered()[
            0].indentation if self.node_list.filtered() else self.parent.indentation + "    "

    def _generate_expected_list(self):
        log("Start _generate_expected_list for LineProxyList")
        log(">>> current list '%s'", self.data)
        indentation = self._get_separator_indentation()

        log("Detect indentation has %s", indentation.__repr__())

        def generate_separator():
            separator = self.middle_separator.copy()
            separator.parent = self.node_list
            separator.on_attribute = self.on_attribute
            separator.indent = indentation
            return separator

        def get_real_last(node):
            try:
                return node.node_list[-1]
            except:
                return node[-1]

        def modify_last_indentation(node, indentation):
            try:
                current_last = get_real_last(node)
                while current_last.type in ('def', 'class', 'ifelseblock'):
                    current_last = get_real_last(current_last)
                current_last.indent = indentation
            except (AttributeError, IndexError, TypeError):
                node.indent = indentation

        expected_list = self.first_blank_lines[:]
        if expected_list:
            log(">> adding first blank lines to expected_list: '%s'", expected_list)
        previous = expected_list[-1] if expected_list else None

        might_need_separator = False
        has_added_separator = False

        if expected_list and self.data and self.data[0][0].type == "endl" and not expected_list[-1].formatting.comment:
            log("first_blank_lines doesn't has comments, reset indentation")
            expected_list[-1].indent = ""

        for position, i in enumerate(self.data):
            log("[%s] %s", position, i)

            if might_need_separator and i[0].type != "endl" and (
                        not previous or previous.type != "endl") and not isinstance(previous, (
                    CodeBlockNode, redbaron.nodes.IfelseblockNode)):
                log(">> Previous line has content and current needs to be indented, append separator to indent it")
                expected_list.append(generate_separator())
                log("-- current result: %s", ["".join(map(lambda x: x.dumps(), expected_list))])
                previous = expected_list[-1]
                might_need_separator = False

            if has_added_separator and i[0].type == "endl":
                # XXX this will break comments if present
                log("Previous is endl (from a added separator) and current is endl, remove indentation of previous")
                expected_list[-1].indent = ""

            if previous and previous.type == "endl" and i[0].type == "endl":
                # XXX this will break comments
                log("Previous is endl and current is endl, remove indentation of previous")
                previous.indent = ""

            has_added_separator = False

            is_last = position == len(self.data) - 1
            log(">> Append node to expected_list: '%s'", [i[0]])
            expected_list.append(i[0])
            log("-- current result: %s", ["".join(map(lambda x: x.dumps(), expected_list))])

            if previous and previous.type == "endl" and i[0].type != "endl" and previous.indentation != indentation:
                log("Previous is endl and current isn't endl and identation isn't correct, fix it")
                previous.indent = indentation

            if i[0].type != "endl" and previous and isinstance(previous, CodeBlockNode):
                log("Previous is CodeBlockNode and current isn't endl, ensure previous has the current identation")
                modify_last_indentation(get_real_last(previous.value), indentation)

            # XXX this will need refactoring...
            if i[1] is not None:
                log("current doesn't have None for formatting")
                # here we encounter a middle value that should have formatting
                # to separate between the intems but has not so we add it
                # this happen because a new value has been added after this one
                if not is_last and not i[1] and not isinstance(i[0], CodeBlockNode):
                    log(
                        "If current isn't a CodeBlockNode and doesn't have a separator and isn't the last, mark it has might needing a separator")
                    might_need_separator = True

                # XXX shoud uniformise the list of formatting nodes
                elif is_last and i[1] and i[1][0].type in ("comma", "dot"):
                    # XXX this will likely break comments if presents at the end of the list
                    log("Current is last and a CodeBlockNode, don't do anything")
                    pass
                else:
                    log(">> Append formatting to expected_list: %s", i[1])
                    expected_list += i[1]
                    log("-- current result: %s", ["".join(map(lambda x: x.dumps(), expected_list))])
            else:
                log("current HAS None for formatting")
                # here we generate the new expected formatting
                # None is used as a sentry value for newly inserted values in the proxy list
                # CodeBlockNode are responsible for the last indentation
                if isinstance(i[0], CodeBlockNode):
                    log("Current is CodeBlockNode, don't do anything")
                    pass
                elif not is_last and not i[0].type == "endl":
                    log(">> Current is not last and not endl, append a separator")
                    has_added_separator = True
                    expected_list.append(generate_separator())
                    log("-- current result: %s", ["".join(map(lambda x: x.dumps(), expected_list))])
                elif i[0].type == "endl":
                    log(">> Current is endl, don't do anything")
                elif is_last:
                    log(">> Current is last, don't do anything")

            previous = expected_list[-1]

        log("End of loop")

        log("-- result before end list procedure: %s", map(lambda x: x.dumps(), expected_list))

        if self.parent and self.parent.next_intuitive:
            log("self.parent is followed by another node, last_indentation is indentation of self.parent")
            last_indentation = self.parent.indentation
        else:
            log("self.parent is NOT followed by another node, last indentation is empty string")
            last_indentation = ""

        if not expected_list or not isinstance(expected_list[-1], (CodeBlockNode, redbaron.nodes.EndlNode)):
            log(
                ">> List is empty or last node is not a CodeBlockNode or EndlNode, append a separator to it and set identation to it")
            expected_list.append(generate_separator())
            expected_list[-1].indent = last_indentation
            log("-- current result: %s", ["".join(map(lambda x: x.dumps(), expected_list))])
        else:
            if isinstance(expected_list[-1], CodeBlockNode):
                # In this case, the last \n is owned by the node
                log("Last node is a CodeBlockNode, ensure that I still have the same last_indentation")
                modify_last_indentation(get_real_last(expected_list[-1].value), last_indentation)
            else:
                log("Last node is NOT CodeBlockNode, ensure that I still have the same last_indentation")
                expected_list[-1].indent = last_indentation

        log("-- final result: %s", map(lambda x: x.dumps(), expected_list))
        log("End")
        return expected_list

    def get_absolute_bounding_box_of_attribute(self, index):
        if index >= len(self.data) or index < 0:
            raise IndexError()
        index = self[index].index_on_parent_raw
        path = self.path().to_baron_path() + [index]
        return baron.path.path_to_bounding_box(self.root.fst(), path)


class DecoratorsLineProxyList(LineProxyList):
    def _convert_input_to_node_object_list(self, value, parent, on_attribute):
        return map(lambda x: self._convert_input_to_node_object(x, parent, on_attribute), value)

    def _generate_expected_list(self):
        expected_list = super(DecoratorsLineProxyList, self)._generate_expected_list()
        expected_list[-1].indent = self.parent.indentation
        return expected_list

    def _get_separator_indentation(self):
        return self.parent.indentation
