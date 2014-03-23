import baron

from . import nodes


class RedBaron(nodes.NodeList):
    def __init__(self, source_code):
        self.data = map(nodes.to_node, baron.parse(source_code))
