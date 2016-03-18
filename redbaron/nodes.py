from __future__ import absolute_import

import re

import baron
from baron.utils import string_instance

from redbaron.base_nodes import Node, NodeList, LiteralyEvaluable, CodeBlockNode, DotProxyList, CommaProxyList, LineProxyList, IfElseBlockSiblingNode, ElseAttributeNode
from redbaron.syntax_highlight import python_html_highlight


class ArgumentGeneratorComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("(x %s)" % string)[0]["generators"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return Node.from_fst(baron.parse("(%s for x in x)" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class AssertNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("assert %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "message":
            if string:
                self.third_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute=on_attribute, parent=parent)]
                return Node.from_fst(baron.parse("assert plop, %s" % string)[0]["message"], parent=parent, on_attribute=on_attribute)

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
            return Node.from_fst(baron.parse("%s = a" % string)[0]["target"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "value":
            return Node.from_fst(baron.parse("a = %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class AssociativeParenthesisNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("(%s)" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class AtomtrailersNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            return NodeList.from_fst(baron.parse("(%s)" % string)[0]["value"]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def __setattr__(self, key, value):
        super(AtomtrailersNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, DotProxyList):
            setattr(self, "value", DotProxyList(self.value))


class BinaryNode(Node, LiteralyEvaluable):
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
            return Node.from_fst(baron.parse("%s + b" % string)[0]["first"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "second":
            return Node.from_fst(baron.parse("bb + %s" % string)[0]["second"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class BinaryStringNode(Node, LiteralyEvaluable):
    pass


class BinaryRawStringNode(Node, LiteralyEvaluable):
    pass


class BooleanOperatorNode(Node):
    def __setattr__(self, key, value):
        if key == "value" and isinstance(value, string_instance):
            assert baron.parse("a %s b" % value)[0]["type"] == "boolean_operator"

        return super(BooleanOperatorNode, self).__setattr__(key, value)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "first":
            return Node.from_fst(baron.parse("%s and b" % string)[0]["first"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "second":
            return Node.from_fst(baron.parse("bb and %s" % string)[0]["second"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class BreakNode(Node):
    pass


class CallNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            return NodeList.from_fst(baron.parse("a(%s)" % string)[0]["value"][1]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def __setattr__(self, key, value):
        super(CallNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, CommaProxyList):
            setattr(self, "value", CommaProxyList(self.value))


class CallArgumentNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("a(%s)" % string)[0]["value"][1]["value"][0]["value"], parent=parent, on_attribute=on_attribute) if string else ""

        elif on_attribute == "target":
            return Node.from_fst(baron.parse("a(%s=b)" % string)[0]["value"][1]["value"][0]["target"], parent=parent, on_attribute=on_attribute) if string else ""

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

            return NodeList.from_fst(baron.parse("class a(%s): pass" % string)[0]["inherit_from"], parent=parent, on_attribute=on_attribute)

        else:
            return super(ClassNode, self)._string_to_node_list(string, parent, on_attribute)

    def __setattr__(self, key, value):
        super(ClassNode, self).__setattr__(key, value)

        if key == "inherit_from" and not isinstance(self.inherit_from, CommaProxyList):
            setattr(self, "inherit_from", CommaProxyList(self.inherit_from, on_attribute="inherit_from"))

class CommaNode(Node):
    pass


class CommentNode(Node):
    pass


class ComparisonNode(Node):
    def __setattr__(self, key, value):
        if key == "value" and isinstance(value, string_instance):
            assert baron.parse("a %s b" % value)[0]["type"] == "comparison"

        return super(ComparisonNode, self).__setattr__(key, value)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "first":
            return Node.from_fst(baron.parse("%s > b" % string)[0]["first"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "value":
            return Node.from_fst(baron.parse("a %s b" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "second":
            return Node.from_fst(baron.parse("bb > %s" % string)[0]["second"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ComparisonOperatorNode(Node):
    pass


class ComplexNode(Node):
    pass


class ComprehensionIfNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("[x for x in x if %s]" % string)[0]["generators"][0]["ifs"][0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ComprehensionLoopNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "ifs":
            return NodeList.from_fst(baron.parse("[x for x in x %s]" % string)[0]["generators"][0]["ifs"], parent=parent, on_attribute=on_attribute)

        else:
            return super(ClassNode, self)._string_to_node_list(string, parent, on_attribute)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "iterator":
            return Node.from_fst(baron.parse("[x for %s in x]" % string)[0]["generators"][0]["iterator"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "target":
            return Node.from_fst(baron.parse("[x for s in %s]" % string)[0]["generators"][0]["target"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ContinueNode(Node):
    pass


class DecoratorNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("@%s()\ndef a(): pass" % string)[0]["decorators"][0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "call":
            if string:
                return Node.from_fst(baron.parse("@a%s\ndef a(): pass" % string)[0]["decorators"][0]["call"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DefArgumentNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("def a(b=%s): pass" % string)[0]["arguments"][0]["value"], parent=parent, on_attribute=on_attribute) if string else ""

        elif on_attribute == "target":
            return Node.from_fst(baron.parse("def a(%s=b): pass" % string)[0]["arguments"][0]["target"], parent=parent, on_attribute=on_attribute) if string else ""

        else:
            raise Exception("Unhandled case")


class DelNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("del %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DictArgumentNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("a(**%s)" % string)[0]["value"][1]["value"][0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DictitemNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("{a: %s}" % string)[0]["value"][0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "key":
            return Node.from_fst(baron.parse("{%s: a}" % string)[0]["value"][0]["key"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DictNode(Node, LiteralyEvaluable):
    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("{%s}" % string)[0]["value"]
        return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

    def __setattr__(self, key, value):
        super(DictNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, CommaProxyList):
            setattr(self, "value", CommaProxyList(self.value))


class DictComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("{x %s}" % string)[0]["generators"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return Node.from_fst(baron.parse("{%s for x in x}" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

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
                self.first_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
                self.second_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]

        super(DottedAsNameNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, DotProxyList):
            setattr(self, "value", DotProxyList(self.value))

    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            fst = baron.parse("import %s" % string)[0]["value"][0]["value"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class DottedNameNode(Node):
    pass


class ElifNode(IfElseBlockSiblingNode):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "test":
            return Node.from_fst(baron.parse("if %s: pass" % string)[0]["value"][0]["test"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class EllipsisNode(Node):
    pass


class ElseNode(IfElseBlockSiblingNode):
    @property
    def next_intuitive(self):
        if self.parent.type == "ifelseblock":
            return super(ElseNode, self).next_intuitive

        elif self.parent.type == "try":
            if self.parent.finally_:
                return self.parent.finally_

            else:
                return self.parent.next

        elif self.parent.type in ("for", "while"):
            return self.parent.next

    @property
    def previous_intuitive(self):
        if self.parent.type == "ifelseblock":
            return super(ElseNode, self).previous_intuitive

        elif self.parent.type == "try":
            return self.parent.excepts[-1]

        elif self.parent.type in ("for", "while"):
            return self.parent


class EndlNode(Node):
    def __repr__(self):
        return repr(baron.dumps([self.fst()]))

    def _bytes_repr_html_(self):
        return python_html_highlight(self.__repr__())


class ExceptNode(CodeBlockNode):
    @property
    def next_intuitive(self):
        next_ = self.next

        if next_:
            return next_

        if self.parent.else_:
            return self.parent.else_

        if self.parent.finally_:
            return self.parent.finally_

        if self.parent.next:
            return self.parent.next

    @property
    def previous_intuitive(self):
        previous_ = self.previous

        if previous_:
            return previous_

        return self.parent

    def __setattr__(self, key, value):
        if key == "delimiter":
            if value == ",":
                self.second_formatting = []
                self.third_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
            elif value == "as":
                self.second_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
                self.third_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
            elif value:
                raise Exception("Delimiters of an except node can only be 'as' or ',' (without spaces around it).")

        super(ExceptNode, self).__setattr__(key, value)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "exception":
            if string:
                self.first_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute=on_attribute, parent=parent)]
                return Node.from_fst(baron.parse("try: pass\nexcept %s: pass" % string)[0]["excepts"][0]["exception"], parent=parent, on_attribute=on_attribute)
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
                self.second_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute=on_attribute, parent=parent)]
                self.third_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute=on_attribute, parent=parent)]
                return Node.from_fst(baron.parse("try: pass\nexcept a as %s: pass" % string)[0]["excepts"][0]["target"], parent=parent, on_attribute=on_attribute)

            else:
                self.delimiter = ""
                self.second_formatting = []
                self.third_formatting = []
                return ""

        else:
            raise Exception("Unhandled case")



class ExecNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("exec %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "globals":
            if string:
                self.second_formatting = [{"type": "space", "value": " "}]
                self.third_formatting = [{"type": "space", "value": " "}]
                return Node.from_fst(baron.parse("exec a in %s" % string)[0]["globals"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "locals":
            if not self.globals:
                raise Exception("I can't set locals when globals aren't set.")

            if string:
                self.fifth_formatting = [{"type": "space", "value": " "}]
                return Node.from_fst(baron.parse("exec a in b, %s" % string)[0]["locals"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class FinallyNode(CodeBlockNode):
    @property
    def next_intuitive(self):
        return self.parent.next

    @property
    def previous_intuitive(self):
        if self.parent.else_:
            return self.parent.else_

        if self.parent.excepts:
            return self.parent.excepts[-1]

        return self.parent

    def __setattr__(self, key, value):
        super(FinallyNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, LineProxyList):
            setattr(self, "value", LineProxyList(self.value, on_attribute="value"))


class ForNode(ElseAttributeNode):
    @property
    def next_intuitive(self):
        if self.else_:
            return self.else_

        return self.next

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "target":
            return Node.from_fst(baron.parse("for i in %s: pass" % string)[0]["target"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "iterator":
            return Node.from_fst(baron.parse("for %s in i: pass" % string)[0]["iterator"], parent=parent, on_attribute=on_attribute)

        else:
            return super(ForNode, self)._string_to_node(string, parent, on_attribute)


class FloatNode(Node, LiteralyEvaluable):
    pass


class FloatExponantNode(Node, LiteralyEvaluable):
    pass


class FloatExponantComplexNode(Node, LiteralyEvaluable):
    pass


class FromImportNode(Node):
    def names(self):
        """Return the list of new names imported

        For example:
            RedBaron("from qsd import a, c, e as f").names() == ['a', 'c', 'f']
        """
        return [x.target if x.target else x.value for x in self.targets]

    def modules(self):
        """Return the list of the targets imported

        For example (notice 'e' instead of 'f'):
            RedBaron("from qsd import a, c, e as f").names() == ['a', 'c', 'e']
        """
        return [x.value for x in self.targets]

    def full_path_names(self):
        """Return the list of new names imported with the full module path

        For example (notice 'e' instead of 'f'):
            RedBaron("from qsd import a, c, e as f").names() == ['qsd.a', 'qsd.c', 'qsd.f']
        """
        return [self.value.dumps() + "." + (x.target if x.target else x.value) for x in self.targets]

    def full_path_modules(self):
        """Return the list of the targets imported with the full module path

        For example (notice 'e' instead of 'f'):
            RedBaron("from qsd import a, c, e as f").names() == ['qsd.a', 'qsd.c', 'qsd.e']
        """
        return [self.value.dumps() + "." + x.value for x in self.targets]

    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "targets":
            fst = baron.parse("from a import %s" % string)[0]["targets"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        if on_attribute == "value":
            fst = baron.parse("from %s import s" % string)[0]["value"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def __setattr__(self, key, value):
        super(FromImportNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, DotProxyList):
            setattr(self, "value", DotProxyList(self.value, on_attribute="value"))

        if key == "targets" and not isinstance(self.targets, CommaProxyList):
            setattr(self, "targets", CommaProxyList(self.targets, on_attribute="targets"))


class DefNode(CodeBlockNode):
    _other_identifiers = ["funcdef", "funcdef_"]
    _default_test_value = "name"

    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "arguments":
            fst = baron.parse("def a(%s): pass" % string)[0]["arguments"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        elif on_attribute == "decorators":
            return self.parse_decorators(string, parent=parent, on_attribute=on_attribute)

        else:
            return super(DefNode, self)._string_to_node_list(string, parent, on_attribute)

    def __setattr__(self, key, value):
        super(DefNode, self).__setattr__(key, value)

        if key == "arguments" and not isinstance(self.arguments, CommaProxyList):
            setattr(self, "arguments", CommaProxyList(self.arguments, on_attribute="arguments"))


class GeneratorComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("(x %s)" % string)[0]["generators"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return Node.from_fst(baron.parse("(%s for x in x)" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class GetitemNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("a[%s]" % string)[0]["value"][1]["value"], parent=parent, on_attribute=on_attribute)


class GlobalNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            fst = baron.parse("global %s" % string)[0]["value"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def __setattr__(self, key, value):
        super(GlobalNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, CommaProxyList):
            setattr(self, "value", CommaProxyList(self.value, on_attribute="value"))


class HexaNode(Node, LiteralyEvaluable):
    pass


class IfNode(IfElseBlockSiblingNode):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "test":
            return Node.from_fst(baron.parse("if %s: pass" % string)[0]["value"][0]["test"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class IfelseblockNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute != "value":
            return super(IfelseblockNode, self)._string_to_node_list(string, parent=parent, on_attribute=on_attribute)

        string = string.rstrip()
        string += "\n"

        if self.next and self.on_attribute == "root":
            string += "\n\n"
        elif self.next:
            string += "\n"

        clean_string = re.sub("^ *\n", "", string) if "\n" in string else string
        indentation = len(re.search("^ *", clean_string).group())

        if indentation:
            string = "\n".join(map(lambda x: x[indentation:], string.split("\n")))

        result = NodeList.from_fst(baron.parse(string)[0]["value"], parent=parent, on_attribute=on_attribute)

        if self.indentation:
            result.increase_indentation(len(self.indentation))
            if self.next:
                result[-1].value.node_list[-1].indent = self.indentation

        return result


class ImportNode(Node):
    def modules(self):
        "return a list of string of modules imported"
        return [x.value.dumps()for x in self('dotted_as_name')]

    def names(self):
        "return a list of string of new names inserted in the python context"
        return [x.target if x.target else x.value.dumps() for x in self('dotted_as_name')]

    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("import %s" % string)[0]["value"]
        return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

    def __setattr__(self, key, value):
        super(ImportNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, CommaProxyList):
            setattr(self, "value", CommaProxyList(self.value, on_attribute="value"))


class IntNode(Node, LiteralyEvaluable):
    def fst(self):
        return {
            "type": "int",
            "value": self.value,
            "section": "number",
        }


class LambdaNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "arguments":
            self.first_formatting = [{"type": "space", "value": " "}] if string else []
            fst = baron.parse("lambda %s: x" % string)[0]["arguments"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            return super(DefNode, self)._string_to_node_list(string, parent, on_attribute)

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("lambda: %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def __setattr__(self, key, value):
        super(LambdaNode, self).__setattr__(key, value)

        if key == "arguments" and not isinstance(self.arguments, CommaProxyList):
            setattr(self, "arguments", CommaProxyList(self.arguments, on_attribute="arguments"))


class LeftParenthesisNode(Node):
    pass


class ListArgumentNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("lambda *%s: x" % string)[0]["arguments"][0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ListComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("[x %s]" % string)[0]["generators"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return Node.from_fst(baron.parse("[%s for x in x]" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class ListNode(Node, LiteralyEvaluable):
    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("[%s]" % string)[0]["value"]
        return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

    def __setattr__(self, key, value):
        super(ListNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, CommaProxyList):
            setattr(self, "value", CommaProxyList(self.value))


class LongNode(Node, LiteralyEvaluable):
    pass


class NameNode(Node, LiteralyEvaluable):
    pass


class NameAsNameNode(Node):
    def __setattr__(self, key, value):
        if key == "target":
            if not (re.match(r'^[a-zA-Z_]\w*$', value) or value in ("", None)):
                raise Exception("The target of a name as name node can only be a 'name' or an empty string or None")

            if value:
                self.first_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]
                self.second_formatting = [Node.from_fst({"type": "space", "value": " "}, on_attribute="delimiter", parent=self)]

        elif key == "value":
            if not (re.match(r'^[a-zA-Z_]\w*$', value) or value in ("", None)):
                raise Exception("The value of a name as name node can only be a 'name' or an empty string or None")

        return super(NameAsNameNode, self).__setattr__(key, value)


class OctaNode(Node, LiteralyEvaluable):
    pass


class PassNode(Node):
    pass


class PrintNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "destination":
            if string and not self.value:
                self.formatting = [{"type": "space", "value": " "}]
                return Node.from_fst(baron.parse("print >>%s" % string)[0]["destination"], parent=parent, on_attribute=on_attribute)

            elif string and self.value:
                self.formatting = [{"type": "space", "value": " "}]
                result = Node.from_fst(baron.parse("print >>%s" % string)[0]["destination"], parent=parent, on_attribute=on_attribute)
                if len(self.value.node_list) and not self.value.node_list[0].type == "comma":
                    self.value = NodeList([Node.from_fst({"type": "comma", "second_formatting": [{"type": "space", "value": " "}], "first_formatting": []}, parent=parent, on_attribute=on_attribute)]) + self.value
                return result

            elif self.value.node_list and self.value.node_list[0].type == "comma":
                self.formatting = [{"type": "space", "value": " "}]
                self.value = self.value.node_list[1:]

            else:
                self.formatting = []

        else:
            raise Exception("Unhandled case")


    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            if string:
                self.formatting = [{"type": "space", "value": " "}]

                fst = baron.parse(("print %s" if not self.destination else "print >>a, %s") % string)[0]["value"]
                return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)
            else:
                self.formatting = [] if not string and not self.destination else [{"type": "space", "value": " "}]
                return NodeList()

        else:
            raise Exception("Unhandled case")

    def __setattr__(self, key, value):
        super(PrintNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, CommaProxyList):
            setattr(self, "value", CommaProxyList(self.value))


class RaiseNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            self.first_formatting = [{"type": "space", "value": " "}] if string else []
            if string:
                return Node.from_fst(baron.parse("raise %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "instance":
            if not self.value:
                raise Exception("Can't set instance if there is not value")

            if string:
                self.third_formatting = [{"type": "space", "value": " "}]
                return Node.from_fst(baron.parse("raise a, %s" % string)[0]["instance"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "traceback":
            if not self.instance:
                raise Exception("Can't set traceback if there is not instance")

            if string:
                self.fifth_formatting = [{"type": "space", "value": " "}]
                return Node.from_fst(baron.parse("raise a, b, %s" % string)[0]["traceback"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class RawStringNode(Node, LiteralyEvaluable):
    pass


class RightParenthesisNode(Node):
    pass


class ReprNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("`%s`" % string)[0]["value"]
        return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

    def __setattr__(self, key, value):
        super(ReprNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, CommaProxyList):
            setattr(self, "value", CommaProxyList(self.value))


class ReturnNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            self.formatting = [{"type": "space", "value": " "}] if string else []
            if string:
                return Node.from_fst(baron.parse("return %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class SemicolonNode(Node):
    pass


class SetNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("{%s}" % string)[0]["value"]
        return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

    def __setattr__(self, key, value):
        super(SetNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, CommaProxyList):
            setattr(self, "value", CommaProxyList(self.value))


class SetComprehensionNode(Node):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "generators":
            fst = baron.parse("{x %s}" % string)[0]["generators"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "result":
            return Node.from_fst(baron.parse("{%s for x in x}" % string)[0]["result"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class SliceNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "lower":
            if string:
                return Node.from_fst(baron.parse("a[%s:]" % string)[0]["value"][1]["value"]["lower"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "upper":
            if string:
                return Node.from_fst(baron.parse("a[:%s]" % string)[0]["value"][1]["value"]["upper"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "step":
            self.has_two_colons = bool(string)
            if string:
                return Node.from_fst(baron.parse("a[::%s]" % string)[0]["value"][1]["value"]["step"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class SpaceNode(Node):
    def __repr__(self):
        return repr(baron.dumps([self.fst()]))


class StarNode(Node):
    pass


class StringNode(Node, LiteralyEvaluable):
    pass


class StringChainNode(Node, LiteralyEvaluable):
    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute == "value":
            fst = baron.parse("a = %s" % string)[0]["value"]["value"]
            return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class TernaryOperatorNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "first":
            return Node.from_fst(baron.parse("%s if b else c" % string)[0]["first"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "second":
            return Node.from_fst(baron.parse("a if b else %s" % string)[0]["second"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "value":
            return Node.from_fst(baron.parse("a if %s else s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class TryNode(ElseAttributeNode):
    @property
    def next_intuitive(self):
        if self.excepts:
            return self.excepts[0]

        if self.finally_:
            return self.finally_

        raise Exception("incoherent state of TryNode, try should be followed either by except or finally")

    def _string_to_node_list(self, string, parent, on_attribute):
        if on_attribute != "excepts":
            return super(TryNode, self)._string_to_node_list(string, parent=parent, on_attribute=on_attribute)

        clean_string = re.sub("^ *\n", "", string) if "\n" in string else string
        indentation = len(re.search("^ *", clean_string).group())

        if indentation:
            string = "\n".join(map(lambda x: x[indentation:], string.split("\n")))

        string = string.rstrip()
        string += "\n"

        if self.next and self.on_attribute == "root":
            string += "\n\n"
        elif self.next:
            string += "\n"

        result = NodeList.from_fst(baron.parse("try:\n pass\n%sfinally:\n pass" % string)[0]["excepts"], parent=parent, on_attribute=on_attribute)

        if self.indentation:
            result.increase_indentation(len(self.indentation))
            if self._get_last_member_to_clean().type != "except":
                # assume that this is an endl node, this might break
                result[-1].value.node_list[-1].indent = self.indentation
            elif self.next:
                result[-1].value.node_list[-1].indent = self.indentation

        return result

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "finally":
            return self._convert_input_to_one_indented_member("finally", string, parent, on_attribute)

        else:
            return super(TryNode, self)._string_to_node(string, parent=parent, on_attribute=on_attribute)

    def __setattr__(self, name, value):
        if name == "finally_":
            name = "finally"

        return super(TryNode, self).__setattr__(name, value)

    def _get_last_member_to_clean(self):
        if self.finally_:
            return self.finally_
        if self.else_:
            return self.else_
        return self.excepts[-1]

    def __getattr__(self, name):
        if name == "finally_":
            return getattr(self, "finally")

        return super(TryNode, self).__getattr__(name)


class TupleNode(Node, LiteralyEvaluable):
    def _string_to_node_list(self, string, parent, on_attribute):
        fst = baron.parse("(%s)" % string)[0]["value"]

        # I assume that I've got an AssociativeParenthesisNode here instead of a tuple
        # because string is only one single element
        if not isinstance(fst, list):
            fst = baron.parse("(%s,)" % string)[0]["value"]

        return NodeList.from_fst(fst, parent=parent, on_attribute=on_attribute)

    def __setattr__(self, key, value):
        super(TupleNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, CommaProxyList):
            setattr(self, "value", CommaProxyList(self.value))


class UnicodeStringNode(Node, LiteralyEvaluable):
    pass


class UnicodeRawStringNode(Node, LiteralyEvaluable):
    pass


class UnitaryOperatorNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "target":
            return Node.from_fst(baron.parse("-%s" % string)[0]["target"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class YieldNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            self.formatting = [{"type": "space", "value": " "}] if string else []
            if string:
                return Node.from_fst(baron.parse("yield %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class YieldAtomNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            self.second_formatting = [{"type": "space", "value": " "}] if string else []
            if string:
                return Node.from_fst(baron.parse("yield %s" % string)[0]["value"], parent=parent, on_attribute=on_attribute)

        else:
            raise Exception("Unhandled case")


class WhileNode(ElseAttributeNode):
    @property
    def next_intuitive(self):
        if self.else_:
            return self.else_

        return self.next

    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "test":
            return Node.from_fst(baron.parse("while %s: pass" % string)[0]["test"], parent=parent, on_attribute=on_attribute)

        else:
            return super(WhileNode, self)._string_to_node(string, parent, on_attribute)


    def __setattr__(self, key, value):
        super(WhileNode, self).__setattr__(key, value)

        if key == "value" and not isinstance(self.value, LineProxyList):
            setattr(self, "value", LineProxyList(self.value, on_attribute="value"))


class WithContextItemNode(Node):
    def _string_to_node(self, string, parent, on_attribute):
        if on_attribute == "value":
            return Node.from_fst(baron.parse("with %s: pass" % string)[0]["contexts"][0]["value"], parent=parent, on_attribute=on_attribute)

        elif on_attribute == "as":
            if string:
                self.first_formatting = [{"type": "space", "value": " "}]
                self.second_formatting = [{"type": "space", "value": " "}]
                return Node.from_fst(baron.parse("with a as %s: pass" % string)[0]["contexts"][0]["as"], parent=parent, on_attribute=on_attribute)
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
            return NodeList.from_fst(baron.parse("with %s: pass" % string)[0]["contexts"], parent=parent, on_attribute=on_attribute)

        else:
            return super(WithNode, self)._string_to_node_list(string, parent, on_attribute)

    def __setattr__(self, key, value):
        super(WithNode, self).__setattr__(key, value)

        if key == "contexts" and not isinstance(self.contexts, CommaProxyList):
            setattr(self, "contexts", CommaProxyList(self.contexts, on_attribute="contexts"))
