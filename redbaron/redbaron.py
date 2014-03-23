import baron
from UserList import UserList

import nodes


class RedBaron(UserList):
    def __init__(self, source_code):
        self.data = map(nodes.to_node, baron.parse(source_code))

    def __fst__(self):
        return [x.__fst__() for x in self.data]
