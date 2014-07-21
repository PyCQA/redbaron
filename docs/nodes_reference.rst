.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

    from redbaron import RedBaron


This is the reference page for every node type encountered in RedBaron and
their specificities.

**This page is still a WIP**.

========
TopClass
========

.. _CodeBlockNode:

CodeBlockNode
=============

CodeBlockNode is a type of node that has a body composed of indented code
like the FuncdefNode or the IfNode. Great care has been taken on the SetAttr of
their value so you don't have to take care about reindenting and other
formatting details.

Demonstration:

.. ipython:: python

    red = RedBaron("def function():\n    pass\n")
    red
    red[0].value = "stuff"  # first '\n' will be added, indentation will be set
    red
    red[0].value = "                    bad_indent"
    red
    red[0].value = " some\n stuff"
    red

Some for indented cases:

.. ipython:: python

    red = RedBaron("class A:\n    def __init__():\n        pass\n\n    def plop():\n        pass")
    red.def_.value = "not_indented"
    red
    red.def_.value = "\n                              badly_indented"
    red
    red.def_.value = "some\nstuff\nfoo\nbar\n\npouet"
    red

=====
Nodes
=====

AssignmentNode
==============

A node representing the assign operation in python (:file:`foo = bar`) and the
"augmented" assign (:file:`foo += bar`).

.. ipython:: python

    RedBaron("a = b")[0].help(deep=True, with_formatting=True)
    RedBaron("a += b")[0].help(deep=True, with_formatting=True)

SetAttr
-------

Works as expected:

.. ipython:: python

    red = RedBaron("a = b")
    red[0].first = "caramba"
    red
    red[0].second = "42"
    red

For the operator part, expected input should work:

.. ipython:: python

    red = RedBaron("a = b")
    red[0].operator = "+="
    red
    red[0].operator = "+" # equivalent to '+='
    red
    red[0].operator = "-" # equivalent to '-='
    red
    red[0].operator = "=" # equivalent to '='
    red
    red[0].operator = "/="
    red
    red[0].operator = "" # equivalent to '='
    red


ClassNode
=========

A node representing a class definition.

.. ipython:: python

    RedBaron("class SomeAwesomeName(A, B, C): pass")[0].help(deep=True, with_formatting=True)

SetAttr
-------

ClassNode is a CodeBlockNode which means its value attribute accepts a wide
range of values, see :ref:`CodeBlockNode` for more informations. Most other
attributes work as expected:

.. ipython:: python

    red = RedBaron("class SomeAwesomeName(A, B, C): pass")
    red[0].name = "AnotherAwesomeName"
    red
    red[0].inherit_from = "object"
    red

Helpers
-------

ClassNode comes with one helper to add another item at the end of the value
of the node without having to think about formatting. It is documented here:
:ref:`append_value`.


DictNode
========

A node representing python sugar syntaxic notation for dict.

.. ipython:: python

    RedBaron("{'a': 1, 'b': 2, 'c': 3}")[0].help(deep=True, with_formatting=True)

Helpers
-------

DictNode comes with one helper to add another item at the end of the value of
the node without having to think about formatting. It is documented here:
:ref:`append_value`. **Warning**: :file:`append_value` of DictNode has a
different signature than the append_value of other nodes: it expects 2
arguments: one of the key and one of the value.

.. ipython:: python

    red = RedBaron("{}")
    red[0].append_value(key="'a'", value="42")
    red


.. _ElifNode:

ElifNode
========

A node representing an elif statement.

The ElifNode, like the :ref:`IfNode` or the :ref:`ElseNode` are stored in a :ref:`IfelseblockNode`.

.. ipython:: python

    RedBaron("if a: pass\nelif b: pass")[0].value[1].help(with_formatting=True, deep=True)

SetAttr
-------

ElifNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more informations. Other attributes
work as expected:

.. ipython:: python

    red = RedBaron("if a: pass\nelif b: pass")
    red
    red[0].value[1].test = "1 + 1 == 11"
    red

Helpers
-------

ElifNode comes with one helper to add another item at the end of the value of the
node without having to think about formating. It is documented here:
:ref:`append_value`.

.. _ElseNode:

ElseNode
========

A node representing an else statement.

The ElseNode, like the :ref:`IfNode` or the :ref:`ElifNode` are stored in a :ref:`IfelseblockNode`.

.. ipython:: python

    RedBaron("if a: pass\nelse: pass")[0].value[1].help(with_formatting=True, deep=True)

SetAttr
-------

ElifNode is a CodeBlockNode whichs means its value attribute accept a wide range
of values, see :ref:`CodeBlockNode` for more informations.

Helpers
-------

ElifNode comes with one helper to add another item at the end of the value of the
node without having to think about formating. It is documented here:
:ref:`append_value`.


EndlNode
========

A node for the end line ('\n', '\r\n') component.

**This node is responsible for holding the indentation AFTER itself**. This
node also handles formatting around it, CommentNode **before** an EndlNode will
end up in the formatting key of an EndlNode 99% of the time (the exception is
if the CommentNode is the last node of the file).

.. ipython:: python

    RedBaron("suff\n")[1].help(with_formatting=True)
    RedBaron("# first node of the file\n# last node of the file").help(with_formatting=True)

.. _ExceptNode:

ExceptNode
==========

A node representing a except statement (member of a :ref:`TryNode`).

.. ipython:: python

    RedBaron("try: pass\nexcept FooBar: pass\nexcept Exception: pass\nelse: pass\nfinally: pass\n")[0].excepts[0].help(deep=True, with_formatting=True)

SetAttr
-------

ExceptNode is a CodeBlockNode whichs means its value attribute accept a wide range
of values, see :ref:`CodeBlockNode` for more informations. Other attributes
works as expected:

.. ipython:: python

    red = RedBaron("try: pass\nexcept: pass")
    red
    red[0].excepts[0].exception = "plop"
    red
    red[0].excepts[0].target = "stuff"
    red
    red[0].excepts[0].exception = ""
    red
    # red[0].excepts[0].target = "stuff" <- would raise without a target

Helpers
-------

ExceptNode comes with one helper to add another item at the end of the value
of the node without having to think about formating. It is documented here:
:ref:`append_value`.

.. _FinallyNode:

FinallyNode
===========

A node representing a finally statement (member of a :ref:`TryNode`).

.. ipython:: python

    RedBaron("try: pass\nexcept FooBar: pass\nexcept Exception: pass\nelse: pass\nfinally: pass\n").finally_.help(deep=True, with_formatting=True)

SetAttr
-------

FinallyNode is a CodeBlockNode whichs means its value attribute accept a wide range
of values, see :ref:`CodeBlockNode` for more informations.

Helpers
-------

FinallyNode comes with one helper to add another item at the end of the value
of the node without having to think about formating. It is documented here:
:ref:`append_value`.


ForNode
=======

A node representing a for loop.

.. ipython:: python

    RedBaron("for i in b:\n    pass")[0].help(deep=True, with_formatting=True)

SetAttr
-------

ForNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more informations. Other attributes
work as expected:

.. ipython:: python

    red = RedBaron("for i in b: pass")
    red
    red[0].iterator = "i, j, k"
    red
    red[0].target = "[x for x in stuff if condition]"
    red

Helpers
-------

ForNode comes with one helper to add another item at the end of the value
of the node without having to think about formatting. It is documented here:
:ref:`append_value`.


FuncdefNode
===========

A node representing a function definition.

.. ipython:: python

    RedBaron("def stuff():\n    pass\n")[0].help(deep=True, with_formatting=True)

SetAttr
-------

FuncdefNode is a CodeBlockNode which means its value attribute accepts a wide
range of values, see :ref:`CodeBlockNode` for more informations. Most other
attributes works as expected:

.. ipython:: python

    red = RedBaron("def stuff():\n    body\n")
    red[0]
    red[0].name = "awesome_function"
    red[0].arguments = "a, b=None, *c, **d"
    red

Decorators might be a bit less intuitive:

.. ipython:: python

    red =  RedBaron("def stuff():\n    body\n")
    red[0].decorators = "@foo(*plop)"
    red
    red[0].decorators = "@foo\n@bar.baz()"
    red
    red[0].decorators = "    @pouet"  # SetAttr will take care of reindenting everything as expected
    red

Helpers
-------

FuncdefNode comes with one helper to add another item at the end of the value
of the node without having to think about formatting. It is documented here:
:ref:`append_value`.

.. _IfNode:

IfNode
======

A node representing an if statement.

The IfNode, like the :ref:`ElifNode` or the :ref:`ElseNode`, is stored in an :ref:`IfelseblockNode`.

.. ipython:: python

    RedBaron("if a: pass")[0].value[0].help(with_formatting=True, deep=True)

SetAttr
-------

IfNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more informations. Other attributes
work as expected:

.. ipython:: python

    red = RedBaron("if a: pass")
    red
    red[0].value[0].test = "1 + 1 == 11"
    red

Helpers
-------

IfNode comes with one helper to add another item at the end of the value of the
node without having to think about formatting. It is documented here:
:ref:`append_value`.


ImportNode
==========

A node representing the import statement of the python language.

*Be careful, this node and its subnodes are way more complex than what you can
expect*.

.. ipython:: python

    RedBaron("import foo")[0].help(with_formatting=True, deep=True)
    RedBaron("import foo.bar.baz as stuff, another_thing.plop")[0].help(with_formatting=True, deep=True)

SetAttr
-------

Works as expected:

.. ipython:: python

    red = RedBaron("import foo")
    red[0].value = "foo.bar.baz as plop, stuff, plop.dot"
    red
    red.help(deep=True)

Helpers
-------

To reduce the complexity, 2 helpers method are provided:

.. ipython:: python

    red = RedBaron("import foo.bar.baz as stuff, another_thing.plop")
    red[0].modules()  # modules imported
    red[0].names()  # names added to the context


IntNode
=======

A python integer.

.. ipython:: python

    RedBaron("42")[0].help(with_formatting=True)


ListNode
========

A node representing python sugar syntaxic notation for list.

.. ipython:: python

    RedBaron("[1, 2, 3]")[0].help(deep=True, with_formatting=True)

Helpers
-------

ListNode comes with one helper to add another item at the end of the value of
the node without having to think about formatting. It is documented here:
:ref:`append_value`.


ReprNode
========

A node representing python sugar syntaxic notation for repr.

.. ipython:: python

    RedBaron("`pouet`")[0].help(deep=True, with_formatting=True)

Helpers
-------

SetNode comes with one helper to add another item at the end of the value of
the node without having to think about formatting. It is documented here:
:ref:`append_value`.


SetNode
========

A node representing python sugar syntaxic notation for set.

.. ipython:: python

    RedBaron("{1, 2, 3}")[0].help(deep=True, with_formatting=True)

Helpers
-------

SetNode comes with one helper to add another item at the end of the value of
the node without having to think about formating. It is documented here:
:ref:`append_value`.


SpaceNode
=========

A formatting node representing a space. You'll probably never have to deal with
it except if you play with the way the file is rendered.

**Those nodes will be hidden in formatting keys 99% of the time** (the only exception is if it's the last node of the file).

.. ipython:: python

    RedBaron("1 + 1")[0].first_formatting[0].help(with_formatting=True)
    RedBaron("1 + 1").help(with_formatting=True)


.. _TryNode:

TryNode
=======

A node representing a try statement. This node is responsible for holding the
:ref:`ExceptNode`, :ref:`FinallyNode` and :ref:`ElseNode`.

.. ipython:: python

    RedBaron("try: pass\nexcept FooBar: pass\nexcept Exception: pass\nelse: pass\nfinally: pass\n")[0].help(deep=True, with_formatting=True)

SetAttr
-------

TryNode is a CodeBlockNode whichs means its value attribute accept a wide range
of values, see :ref:`CodeBlockNode` for more informations.

**The other attributes (excepts, finally, else) cannot be setted easily for
now**. It is planned to fix this in a near future.

Helpers
-------

TryNode comes with one helper to add another item at the end of the value
of the node without having to think about formating. It is documented here:
:ref:`append_value`.


TupleNode
=========

A node representing python sugar syntaxic notation for tuple.

.. ipython:: python

    RedBaron("(1, 2, 3)")[0].help(deep=True, with_formatting=True)

Helpers
-------

TupleNode comes with one helper to add another item at the end of the value of
the node without having to think about formating. It is documented here:
:ref:`append_value`.


WhileNode
=========

A node representing a while loop.

.. ipython:: python

    RedBaron("while condition:\n    pass")[0].help(deep=True, with_formatting=True)

SetAttr
-------

WhileNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more informations. Other attributes
work as expected:

.. ipython:: python

    red = RedBaron("while condition: pass")
    red
    red[0].test = "a is not None"
    red

Helpers
-------

WhileNode comes with one helper to add another item at the end of the value
of the node without having to think about formatting. It is documented here:
:ref:`append_value`.

WithContextItemNode
===================

A node representing a while loop.

.. ipython:: python

    RedBaron("with a as b: pass")[0].contexts[0].help(deep=True, with_formatting=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("with a: pass")
    red
    red[0].contexts[0].value = "plop"
    red
    red[0].contexts[0].as_ = "stuff"
    red
    red[0].contexts[0].as_ = ""
    red

Helpers
-------

WithContextItemNode comes with one helper to add another item at the end of the
value of the node without having to think about formatting. It is documented
here: :ref:`append_value`.


WithNode
========

A node representing a with statement.

.. ipython:: python

    RedBaron("with a as b, c: pass")[0].help(deep=True, with_formatting=True)

SetAttr
-------

WithNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more informations. Other attributes
work as expected:

.. ipython:: python

    red = RedBaron("with a: pass")
    red
    red[0].contexts = "b as plop, stuff()"
    red

Helpers
-------

WithNode comes with one helper to add another item at the end of the value
of the node without having to think about formatting. It is documented here:
:ref:`append_value`.
