# -*- coding:Utf-8 -*-

from __future__ import absolute_import

from redbaron.base_nodes import Node, NodeList, ProxyList


class NodeVisitor(Node):
    """
    A node base class that walks the full syntax tree and calls a
    visitor function for every node found.
    """

    # TODO: Improve for visitor
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

        for kind, key, _ in filter(
                lambda x: x[0] in ("list", "formatting") or (x[0] == "key" and isinstance(getattr(self, x[1]), Node)),
                self._render()):
            if kind == "key":
                i = getattr(self, key)
                if not i:
                    continue

                to_return += i.find_all(identifier, *args, **kwargs)

            elif kind in ("list", "formatting"):
                if isinstance(getattr(self, key), ProxyList):
                    for i in getattr(self, key).node_list:
                        to_return += i.find_all(identifier, *args, **kwargs)
                else:
                    for i in getattr(self, key):
                        to_return += i.find_all(identifier, *args, **kwargs)

            else:
                raise Exception()

        return to_return

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit())
        return visitor

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for data, value in self.find_all(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, (Node, NodeList)):
                        self.visit(item)
            elif isinstance(value, (Node, NodeList)):
                self.visit(value)


class NodeTransformer(NodeVisitor):
    """
    A :class:`NodeVisitor` subclass that walks the abstract syntax tree and
    allows modification of nodes.
    """

    def generic_visit(self, node):
        for field, old_value in self.find_all(node):
            old_value = getattr(node, field, None)
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, (Node, NodeList)):
                        value = self.visit(value)
                        if value is None:
                            continue
                        elif not isinstance(value, (Node, NodeList)):
                            new_values.extend(value)
                            continue
                    new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, (Node, NodeList)):
                new_node = self.visit(old_value)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node
