class Node(object):
    def __init__(self, node):
        self.value = node["value"]


class NameNode(Node):
    pass


class EndlNode(Node):
    pass


class IntNode(Node):
    pass
