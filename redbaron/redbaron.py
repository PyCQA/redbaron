import baron
from UserList import UserList

import nodes

class RedBaron(UserList):
    def __init__(self, source_code):
        self.data = map(self._type_to_node, baron.parse(source_code))

    def _type_to_node(self, fst_node):
        return getattr(nodes, fst_node["type"].capitalize() + "Node")(fst_node)
