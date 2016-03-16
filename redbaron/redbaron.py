from __future__ import absolute_import

import baron
import baron.path
from baron.utils import string_instance

from redbaron import nodes, base_nodes


# TODO
# LineProxyList: handle comments
#                should a 'pass' be put if the list would be empty?
#                add blank line arround in certain cases? Like arround function/class at first level and second level
#                expected behavior on append when blank lines at the end of the block (-> append before blank lines)
#                more explicit display for blank lines in line proxy .help()
# if node_list is modified, the proxy list won't update itself -> bugs

# CommaProxyList indented
# "change formatting style"
# the "\n" after the "[{(" is hold by the parent node, this parent node should have a method to tell the CommaProxyList where this is

# FIXME: doc others.rst line 244
# FIXME: __setattr__ is broken on formatting

# XXX
# should .next and .previous behavior should be changed to drop formatting
# nodes? I guess so if I consider that with enough abstraction the user will
# never have to play with formatting node unless he wants to


class RedBaron(base_nodes.GenericNodesUtils, base_nodes.LineProxyList):
    def __init__(self, source_code):
        self.first_blank_lines = []  # XXX might need changes

        if isinstance(source_code, string_instance):
            self.node_list = base_nodes.NodeList.from_fst(baron.parse(source_code), parent=self, on_attribute="root")
            self.middle_separator = nodes.DotNode({"type": "endl", "formatting": [], "value": "\n", "indent": ""})

            self.data = []
            previous = None
            for i in self.node_list:
                if i.type != "endl":
                    self.data.append([i, []])
                elif previous and previous.type == "endl":
                    self.data.append([previous, []])
                elif previous is None and i.type == "endl":
                    self.data.append([i, []])
                elif self.data:
                    self.data[-1][1].append(i)

                previous = i
            self.node_list.parent = None
        else:
            # Might be init from same object, or slice
            super(RedBaron, self).__init__(source_code)
        self.on_attribute = None
        self.parent = None

    def _convert_input_to_node_object(self, value, parent, on_attribute):
        return base_nodes.GenericNodesUtils._convert_input_to_node_object(self, value, self, "root")

    def _convert_input_to_node_object_list(self, value, parent, on_attribute):
        return base_nodes.GenericNodesUtils._convert_input_to_node_object_list(self, value, self, "root")
