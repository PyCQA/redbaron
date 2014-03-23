class Node(object):
    def __init__(self, node):
        self.value = node["value"]


class NameNode(Node):
    pass


class EndlNode(Node):
    pass


class IntNode(Node):
    def __init__(self, node):
        super(IntNode, self).__init__(node)
        self.value = int(self.value)
