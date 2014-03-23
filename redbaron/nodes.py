def to_node(node):
    return globals()["".join(map(lambda x: x.capitalize(), node["type"].split("_"))) + "Node"](node)


class Node(object):
    def __init__(self, node):
        for key, value in node.items():
            if isinstance(value, dict):
                pass
                setattr(self, key, to_node(value))
            else:
                setattr(self, key, value)


class NameNode(Node):
    pass


class EndlNode(Node):
    pass


class IntNode(Node):
    def __init__(self, node):
        super(IntNode, self).__init__(node)
        self.value = int(self.value)


class AssignmentNode(Node):
    pass


class BinaryOperatorNode(Node):
    pass


class PassNode(Node):
    pass
