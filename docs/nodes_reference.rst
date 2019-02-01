.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

    from redbaron import RedBaron


This is the reference page for every node type encountered in RedBaron and
their specificities.

=====================
Nodes References Page
=====================

========
TopClass
========

.. _CodeBlockNode:

CodeBlockNode
=============

CodeBlockNode is a type of node that has a body composed of indented code
like the DefNode or the IfNode. Great care has been taken on the SetAttr of
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

ArgumentGeneratorComprehensionNode
==================================

A node representing generator passed as an argument during a function call.

.. ipython:: python

    RedBaron("a(x for y in z)")[0].value[1].value[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("a(x for y in z)")
    red
    red[0].value[1].value[0].result = "pouet"
    red
    red[0].value[1].value[0].generators = "for artichaut in courgette"
    red


AssertNode
==========

A node representing the assert statement.

.. ipython:: python

    RedBaron("assert test, message")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("assert some_test")
    red
    red[0].value = "1 == caramba()"
    red
    red[0].message = "'foo bar'"
    red
    red[0].message = ""
    red


AssignmentNode
==============

A node representing the assign operation in python (:file:`foo = bar`) and the
"augmented" assign (:file:`foo += bar`).

.. ipython:: python

    RedBaron("a = b")[0].help(deep=True)
    RedBaron("a += b")[0].help(deep=True)

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

AssociativeParenthesisNode
==========================

This node represents a statement prioritised on another by being surrounded by
parenthesis. For e.g., the first part of this addition: :file:`(1 + 1) * 2`.

.. ipython:: python

    RedBaron("(foo)")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("(foo)")
    red
    red[0].value = "1 + 1"
    red


.. _AtomtrailersNode:

AtomtrailersNode
================

This node represents a combination of :ref:`NameNode`, :ref:`DotNode`,
:ref:`CallNode`, :ref:`GetitemNode` sorted in a list. For e.g.:
:file:`a.b().c[d]`.

.. ipython:: python

    RedBaron("a.b().c[d]")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("a.b()")
    red
    red[0].value = "d.be"
    red


BinaryNode
==========

The node represents a binary number value.

.. ipython:: python

    RedBaron("0b10101")[0].help(deep=True)

BinaryOperatorNode
==================

The node represents a binary operator (an operator (e.g.: :file:`+` :file:`-` :file:`/`..) applied to 2 values) with its operands. For e.g.: :file:`1 + 1`.

.. ipython:: python

    RedBaron("1 + 1")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("1 + 1")
    red
    red[0].value = "*"
    red
    red[0].first = "(1 + 1)"
    red
    red[0].second = "caramba"
    red


BooleanOperatorNode
===================

The node represents a boolean operator (an operator (e.g.: :file:`and` :file:`or`) applied to 2 values) with its operands. For e.g.: :file:`x and y`.

.. ipython:: python

    RedBaron("x and y")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("x and y")
    red
    red[0].value = "or"
    red
    red[0].first = "plop"
    red
    red[0].second = "oupsi"
    red

.. _CallNode:

CallNode
========

A node representing a call (eg: :file:`a()`, here :file:`a` is called with no
arguments). It is always stored in an :ref:`AtomtrailersNode` or a
:ref:`DecoratorNode`.

.. ipython:: python

    RedBaron("a(b, c=d)")[0].value[1].help(deep=True)

SetAttr
-------

SetAttr works as expected:

.. ipython:: python

    red = RedBaron("a()")
    red[0].value[1].value = "b, c=d, *e, **f"
    red

CallArgumentNode
================

A node representing an argument or a named argument of a :ref:`CallNode` (other
nodes that can be in a CallNode are :ref:`ListArgumentNode` and
:ref:`DictArgumentNode`).

.. ipython:: python

    RedBaron("a(b, c=d)")[0].value[1].value[0].help(deep=True)
    RedBaron("a(b, c=d)")[0].value[1].value[1].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("a(b)")
    red
    red[0].value[1].value[0] = "stuff=foo"
    red


ClassNode
=========

A node representing a class definition.

.. ipython:: python

    RedBaron("class SomeAwesomeName(A, B, C): pass")[0].help(deep=True)

SetAttr
-------

ClassNode is a CodeBlockNode which means its value attribute accepts a wide
range of values, see :ref:`CodeBlockNode` for more information. Most other
attributes work as expected:

.. ipython:: python

    red = RedBaron("class SomeAwesomeName(A, B, C): pass")
    red[0].name = "AnotherAwesomeName"
    red
    red[0].inherit_from = "object"
    red

CommaNode
=========

A node representing a comma, this is the kind of formatting node that you might
have to deal with if not enough high level helpers are available. They are
generally present in call, function arguments definition and data structure
sugar syntactic notation.

The comma node is responsible for holding the formatting around it.

.. ipython:: python

    RedBaron("[1, 2, 3]")[0].value.node_list[1].help(deep=True)

ComparisonNode
==============

The node represents a comparison operation, for e.g.: :file:`42 > 30`.

.. ipython:: python

    RedBaron("42 > 30")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("42 > 30")
    red
    red[0].operator = "=="
    red
    red[0].first = "(1 + 1)"
    red
    red[0].second = "caramba"
    red


ComprehensionIfNode
===================

The node represents "if" condition in a comprehension loop. It is always a
member of a :ref:`ComprehensionLoopNode`.

.. ipython:: python

    RedBaron("[x for x in x if condition]")[0].generators[0].ifs[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("[x for x in x if condition]")
    red
    red[0].generators[0].ifs[0].value = "True"
    red


.. _ComprehensionLoopNode:

ComprehensionLoopNode
=====================

The node represents the loop part of a comprehension structure.

.. ipython:: python

    RedBaron("[x for y in z]")[0].generators[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("[x for y in z]")
    red
    red[0].generators[0].target = "plop"
    red
    red[0].generators[0].iterator = "iter"
    red
    red[0].generators[0].ifs = "if a if b"
    red


.. _DecoratorNode:

DecoratorNode
=============

A node representing an individual decorator (of a function or a class).

.. ipython:: python

    RedBaron("@stuff.plop(*a)\ndef b(): pass")[0].decorators[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("@stuff\ndef a(): pass")
    red
    red[0].decorators[0].value = "a.b.c"
    red
    red[0].decorators[0].call = "(*args)"
    red
    red[0].decorators[0].call = ""
    red


DefNode
=======

A node representing a function definition.

.. ipython:: python

    RedBaron("def stuff():\n    pass\n")[0].help(deep=True)

SetAttr
-------

DefNode is a CodeBlockNode which means its value attribute accepts a wide
range of values, see :ref:`CodeBlockNode` for more information. Most other
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


*New in 0.7*.

Async is a boolean attribute that determine if a function is async:

.. ipython:: python

    red =  RedBaron("def stuff():\n    body\n")
    red[0].async_
    red[0].async_ = True
    red
    red[0].async_ = False
    red

.. WARNING::
   As of python 3.7 `async` and `await` are now reserved keywords so don't uses
   `red.async`, it works as expected but won't make your code forward
   compatible.

*New in 0.9*

Return annotation management:

.. ipython:: python

    red =  RedBaron("def stuff():\n    return 42\n")
    red
    red[0].return_annotation = "Int"
    red
    red[0].return_annotation = ""
    red


DefArgumentNode
===============

A node representing an argument in a function definition.

.. ipython:: python

    RedBaron("def a(b, c=d): pass")[0].arguments.help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("def a(b): pass")
    red
    red[0].arguments[0].name = "plop"
    red
    red[0].arguments[0].value = "1 + 1"
    red

*New in 0.9*

Annotations:

.. ipython:: python

    red = RedBaron("def a(b): pass")
    red
    red[0].arguments[0].annotation = "Int"
    red
    red[0].arguments[0].annotation
    red

DelNode
=======

A node representing a :file:`del` statement.

.. ipython:: python

    RedBaron("del stuff")[0].help(deep=True)


SetAttr
-------

.. ipython:: python

    red = RedBaron("del stuff")
    red
    red[0].value = "some, other, stuff"
    red


.. _DictArgumentNode:

DictArgumentNode
================

A node representing a 'kwargs' defined in a function definition argument or
used in a :ref:`CallNode`.

.. ipython:: python

    RedBaron("a(**b)")[0].value[1].value[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("a(**b)")
    red
    red[0].value[1].value[0].value = "plop"
    red

*New in 0.9*

Annotations:

.. ipython:: python

    red = RedBaron("def a(**b): pass")
    red
    red[0].arguments[0].annotation = "Int"
    red
    red[0].arguments[0].annotation
    red


DictNode
========

A node representing python sugar syntactic notation for dict.

.. ipython:: python

    RedBaron("{'a': 1, 'b': 2, 'c': 3}")[0].help(deep=True)

DictComprehensionNode
=====================

A node representing dictionary comprehension node.

.. ipython:: python

    RedBaron("{a: b for c in d}")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("{a: b for c in d}")
    red
    red[0].result = "plop: poulpe"
    red
    red[0].generators = "for zomg in wtf"
    red


DottedAsNameNode
================

A node representing an argument to the import node.

.. ipython:: python

    RedBaron("import a.b.c as d")[0].value[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("import a.b.c as d")
    red
    red[0].value[0].value = "some.random.module"
    red
    red[0].value[0].target = "stuff"
    red


.. _DotNode:

DotNode
=======

A node representing a dot '.', generally found in atom trailers (this kind of structure: 'variable.another_variable(call)[getitem]').
This is the kind of formatting node that you might have to deal with if not enough high level helpers are available.

The dot node is responsible for holding the formatting around it.

.. ipython:: python

    RedBaron("a.b")[0].value[1].help(deep=True)

.. _ElifNode:

ElifNode
========

A node representing an elif statement.

The ElifNode, like the :ref:`IfNode` or the :ref:`ElseNode` are stored in a :ref:`IfelseblockNode`.

.. ipython:: python

    RedBaron("if a: pass\nelif b: pass")[0].value[1].help(deep=True)

SetAttr
-------

ElifNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more information. Other attributes
work as expected:

.. ipython:: python

    red = RedBaron("if a: pass\nelif b: pass")
    red
    red[0].value[1].test = "1 + 1 == 11"
    red

.. _ElseNode:

ElseNode
========

A node representing an else statement.

The ElseNode, like the :ref:`IfNode` or the :ref:`ElifNode`, is stored in a :ref:`IfelseblockNode`.

.. ipython:: python

    RedBaron("if a: pass\nelse: pass")[0].value[1].help(deep=True)

SetAttr
-------

ElifNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more information.

EllipsisNode
============

A node representing "...".

.. ipython:: python

    RedBaron("def a(): ...").ellipsis.help(deep=True)

EndlNode
========

A node for the end line ('\n', '\r\n') component.

**This node is responsible for holding the indentation AFTER itself**. This
node also handles formatting around it, CommentNode **before** an EndlNode will
end up in the formatting key of an EndlNode 99% of the time (the exception is
if the CommentNode is the last node of the file).

.. ipython:: python

    RedBaron("\n")[0].help()
    RedBaron("# first node of the file\n# last node of the file").node_list.help()

.. _ExceptNode:

ExceptNode
==========

A node representing an except statement (member of a :ref:`TryNode`).

.. ipython:: python

    RedBaron("try: pass\nexcept FooBar: pass\nexcept Exception: pass\nelse: pass\nfinally: pass\n")[0].excepts[0].help(deep=True)

SetAttr
-------

ExceptNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more information. Other attributes
work as expected:

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

ExecNode
========

A node representing an exec statement.

.. ipython:: python

    RedBaron("exec '1 + 1' in a, b")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("exec 'stuff'")
    red
    red[0].value = 'some_code'
    red
    red[0].globals = 'x'
    red
    red[0].locals = 'y'
    red


.. _FinallyNode:

FinallyNode
===========

A node representing a finally statement (member of a :ref:`TryNode`).

.. ipython:: python

    RedBaron("try: pass\nexcept FooBar: pass\nexcept Exception: pass\nelse: pass\nfinally: pass\n").finally_.help(deep=True)

SetAttr
-------

FinallyNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more information.

ForNode
=======

A node representing a for loop.

.. ipython:: python

    RedBaron("for i in b:\n    pass")[0].help(deep=True)

SetAttr
-------

ForNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more information. The else attributes
accept a great ranges of inputs, since :file:`else` is a reserved python
keyword, you need to access it using the :file:`else_` attribute. Other
attributes work as expected:

.. ipython:: python

    red = RedBaron("for i in b: pass")
    red
    red[0].iterator = "i, j, k"
    red
    red[0].target = "[x for x in stuff if condition]"
    red
    red[0].else_ = "do_stuff"
    red
    red[0].else_ = "else: foobar"
    red
    red[0].else_ = "    else:\n        badly_indented_and_trailing\n\n\n\n"
    red

*New in 0.8*.

Async is a boolean attribute that determine if a function is async:

.. ipython:: python

    red =  RedBaron("for a in b: pass")
    red[0].async_
    red[0].async_ = True
    red
    red[0].async_ = False
    red

.. WARNING::
   As of python 3.7 `async` and `await` are now reserved keywords so don't uses
   `red.async`, it works as expected but won't make your code forward
   compatible.



FromImportNode
==============

A node representing a "from import" statement.

.. ipython:: python

    RedBaron("from a import b")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("from a import b")
    red
    red[0].value = "some.module"
    red
    red[0].targets = "a as b, c as d, e"
    red

Helpers
-------

To reduce the complexity, 2 helpers method are provided:

.. ipython:: python

    red = RedBaron("from foo.bar import baz as stuff, plop")
    red[0].names()  # names added to the context
    red[0].modules()  # modules imported
    red[0].full_path_names()  # names added to the context with full path
    red[0].full_path_modules()  # modules imported with full path

GeneratorComprehensionNode
==========================

A node representing a generator comprehension node.

.. ipython:: python

    RedBaron("(x for y in z)")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("(x for y in z)")
    red
    red[0].result = "pouet"
    red
    red[0].generators = "for artichaut in courgette"
    red

.. _GetitemNode:

GetitemNode
===========

A node representing a 'get item' access on a python object, in other words the
'[stuff]' in 'some_object[stuff]'.

.. ipython:: python

    RedBaron("a[b]")[0].value[1].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("a[b]")
    red
    red[0].value[1].value = "1 + 1"
    red

GlobalNode
==========

A node representing a global statement.

.. ipython:: python

    RedBaron("global a")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("global a")
    red
    red[0].value = "stuff, plop"
    red

.. _IfNode:

IfNode
======

A node representing an if statement.

The IfNode, like the :ref:`ElifNode` or the :ref:`ElseNode`, is stored in an :ref:`IfelseblockNode`.

.. ipython:: python

    RedBaron("if a: pass")[0].value[0].help(deep=True)

SetAttr
-------

IfNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more information. Other attributes
work as expected:

.. ipython:: python

    red = RedBaron("if a: pass")
    red
    red[0].value[0].test = "1 + 1 == 11"
    red

.. _IfelseblockNode:

IfelseblockNode
===============

A node representing the conditional block composed of at least one if statement,
zero or more elif statements and, at the end, an optional else statement. All
those statements are stored in a list.

.. ipython:: python

    RedBaron("if a: pass\nelif b: pass\nelse: pass\n")[0].help(deep=True)

SetAttr
-------

Works as expected and is very flexible on its input:

* the input is automatically put at the correct indentation
* the input is automatically right strip
* if the statement is followed, the correct number of blanks lines are added: 2 when at the root of the file, 1 when indented

.. ipython:: python

    red = RedBaron("if a: pass\n")
    red
    red[0].value = "if a:\n    pass\nelif b:\n    pass\n\n\n"
    red
    red[0].value = "    if a:\n        pass"
    red

.. ipython:: python

    red = RedBaron("if a:\n    pass\n\n\nplop")
    red
    red[0].value = "    if a:\n        pass"
    red

.. ipython:: python

    red = RedBaron("while True:\n    if plop:\n        break\n\n    stuff")
    red
    red[0].value[1].value = "if a:\n    pass\nelif b:\n    pass\n\n\n"
    red


ImportNode
==========

A node representing the import statement of the python language.

*Be careful, this node and its subnodes are way more complex than what you can
expect*.

.. ipython:: python

    RedBaron("import foo")[0].help(deep=True)
    RedBaron("import foo.bar.baz as stuff, another_thing.plop")[0].help(deep=True)

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

    RedBaron("42")[0].help()


KwargsOnlyMarkerNode
====================

*New in 0.7*.

A node representing the "*" in arguments declaration to force keywords only
arguments after itself.

.. ipython:: python

    RedBaron("def a(*): pass")[0].arguments[0].help(deep=True)


LambdaNode
==========

A node representing a lambda statement.

.. ipython:: python

    RedBaron("lambda x: y")[0].help(deep=True)

SetAttr
-------

Works as expected:

.. ipython:: python

    red = RedBaron("lambda x: y")
    red
    red[0].arguments = "a, b=c, *d, **f"
    red
    red[0].value = "plop"
    red


.. _ListArgumentNode:

ListArgumentNode
================

A node representing a "star argument" in a function call **or** definition.

.. ipython:: python

    RedBaron("def a(*b): pass")[0].arguments[0].help(deep=True)

SetAttr
-------

Works as expected:

.. ipython:: python

    red = RedBaron("def a(*b): pass")
    red
    red[0].arguments[0].value = "plop"
    red

*New in 0.9*

Annotations:

.. ipython:: python

    red = RedBaron("def a(*b): pass")
    red
    red[0].arguments[0].annotation = "Int"
    red
    red[0].arguments[0].annotation
    red


ListComprehensionNode
=====================

A node representing a list comprehension node.

.. ipython:: python

    RedBaron("[x for y in z]")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("[x for y in z]")
    red
    red[0].result = "pouet"
    red
    red[0].generators = "for artichaut in courgette"
    red

ListNode
========

A node representing python sugar syntactic notation for list.

.. ipython:: python

    RedBaron("[1, 2, 3]")[0].help(deep=True)

NameAsNameNode
==============

A node representing an argument to the from import statement.

.. ipython:: python

    RedBaron("from x import a as d")[0].targets[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("from x import a as d")
    red
    red[0].targets[0].value = "some_random_module"
    red
    red[0].targets[0].target = "stuff"
    red


NonlocalNode
============

*New in 0.7*.

A node representing a nonlocal statement.

.. ipython:: python

    RedBaron("nonlocal a")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("nonlocal a")
    red
    red[0].value = "stuff, plop"
    red

.. _IfNode:

PrintNode
=========

A node representing a print statement.

.. ipython:: python

    RedBaron("print(stuff)")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("print(stuff)")
    red
    red[0].destination = "some_file"
    red
    red[0].value = "a, b, c"
    red
    red[0].destination = ""
    red
    red[0].value = ""
    red


RaiseNode
=========

A node representing a raise statement.

.. ipython:: python

    RedBaron("raise Exception(), foo, bar")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("raise stuff")
    red
    red[0].value = "foo"
    red
    red[0].instance = "bar"
    red
    red[0].traceback = "baz"
    red


*New in 0.9*

How to deal with the "raise from" notation: (by default a comma is inserted to
avoid breaking backward compatibility)

.. ipython:: python

    red = RedBaron("raise stuff")
    red
    red[0].instance = "foo"
    red
    red[0].comma_or_from = "from"
    red
    red[0].comma_or_from = ","
    red
    red[0].instance = ""
    red

ReprNode
========

A node representing python sugar syntactic notation for repr.

.. ipython:: python

    RedBaron("`pouet`")[0].help(deep=True)

ReturnNode
==========

A node representing a return statement.

.. ipython:: python

    RedBaron("return stuff")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("return stuff")
    red
    red[0].value = "1 + 1"
    red
    red[0].value = ""
    red


SetNode
=======

A node representing python sugar syntactic notation for set.

.. ipython:: python

    RedBaron("{1, 2, 3}")[0].help(deep=True)

SetComprehensionNode
====================

A node representing a set comprehension node.

.. ipython:: python

    RedBaron("{x for y in z}")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("{x for y in z}")
    red
    red[0].result = "pouet"
    red
    red[0].generators = "for artichaut in courgette"
    red

SliceNode
=========

A node representing a slice, the "1:2:3" that can be found in a
:ref:`GetitemNode`.

.. ipython:: python

    RedBaron("a[1:-1:2]")[0].value[1].value.help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("a[1:-1:2]")
    red
    red[0].value[1].value.lower = "a"
    red
    red[0].value[1].value.upper = "b"
    red
    red[0].value[1].value.step = "stuff"
    red
    red[0].value[1].value.step = ""
    red

SpaceNode
=========

A formatting node representing a space. You'll probably never have to deal with
it except if you play with the way the file is rendered.

**Those nodes will be hidden in formatting keys 99% of the time** (the only exception is if it's the last node of the file).

.. ipython:: python

    RedBaron("1 + 1")[0].first_formatting[0].help()
    RedBaron("1 + 1").help()


StarExpressionNode
==================

*New in 0.9*

A node representing the result of a deconstruction in an assignment.

.. ipython:: python

   red = RedBaron("a, *b = c")
   red
   red[0].target[1].help()

StringChainNode
===============

This is a special node that handle a particular way of writing a single string in
python by putting several strings one after the other while only separated by
spaces or endls.

.. ipython:: python

    RedBaron("'a' r'b' b'c'")[0].help(deep=True)


SetAttr
-------

.. ipython:: python

    red = RedBaron("'a' r'b' b'c'")
    red
    red[0].value = "'plip' 'plop'"
    red

TernaryOperatorNode
===================

A node representing the ternary operator expression.

.. ipython:: python

    RedBaron("a if b else c")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("a if b else c")
    red
    red[0].value = "some_test"
    red
    red[0].first = "a_value"
    red
    red[0].second = "another_value"
    red

.. _TryNode:

TryNode
=======

A node representing a try statement. This node is responsible for holding the
:ref:`ExceptNode`, :ref:`FinallyNode` and :ref:`ElseNode`.

.. ipython:: python

    RedBaron("try: pass\nexcept FooBar: pass\nexcept Exception: pass\nelse: pass\nfinally: pass\n")[0].help(deep=True)

SetAttr
-------

TryNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more information. For the :file:`else`
and the :file:`finally` and the :file:`excepts` attributes, TryNode is very
flexible on the range of inputs it can get, like for a CodeBlockNode value's
attribute.

**Important**: Since :file:`else` and :file:`finally` are reserved keywords in python, you
need to append a :file:`_` to those attributes name to access/modify them:
:file:`node.else_` and :file:`node.finally_`.

.. ipython:: python

    red = RedBaron("try:\n    pass\nexcept:\n    pass\n")
    red
    red[0].else_ = "do_stuff"
    red
    red[0].else_ = "else: foobar"
    red
    red[0].else_ = "    else:\n        badly_indented_and_trailing\n\n\n\n"
    red
    # input management of finally_ works the same way than for else_
    red[0].finally_ = "close_some_stuff"
    red
    red[0].else_ = ""
    red
    red[0].finally_ = ""
    red
    red[0].excepts = "except A as b:\n    pass"
    red
    red[0].excepts = "except X:\n    pass\nexcept Y:\n    pass"
    red
    # You **CAN'T** do this red[0].excepts = "foobar"

TupleNode
=========

A node representing python sugar syntactic notation for tuple.

.. ipython:: python

    RedBaron("(1, 2, 3)")[0].help(deep=True)

UnitaryOperatorNode
===================

A node representing a number sign modification operator like :file:`-2` or :file:`+42`.

.. ipython:: python

    RedBaron("-1")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("-1")
    red
    red[0].target = "42"
    red
    red[0].value = "+"
    red


YieldNode
=========

A node representing a yield statement.

.. ipython:: python

    RedBaron("yield 42")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("yield 42")
    red
    red[0].value = "stuff"
    red
    red[0].value = ""
    red


YieldAtomNode
=============

A node representing a yield statement surrounded by parenthesis.

.. ipython:: python

    RedBaron("(yield 42)")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("(yield 42)")
    red
    red[0].value = "stuff"
    red
    red[0].value = ""
    red

YieldFromNode
=============

*New in 0.7*.

A node representing a "yield from" statement.

.. ipython:: python

    RedBaron("yield from 42")[0].help(deep=True)

SetAttr
-------

.. ipython:: python

    red = RedBaron("yield from 42")
    red
    red[0].value = "stuff"
    red


WhileNode
=========

A node representing a while loop.

.. ipython:: python

    RedBaron("while condition:\n    pass")[0].help(deep=True)

SetAttr
-------

WhileNode is a CodeBlockNode which means its value attribute accepts a wide
range of values, see :ref:`CodeBlockNode` for more information. The else
attributes accept a great ranges of inputs, since :file:`else` is a reserved
python keyword, you need to access it using the :file:`else_` attribute. Other
attributes work as expected:

.. ipython:: python

    red = RedBaron("while condition: pass")
    red
    red[0].test = "a is not None"
    red
    red[0].else_ = "do_stuff"
    red
    red[0].else_ = "else: foobar"
    red
    red[0].else_ = "    else:\n        badly_indented_and_trailing\n\n\n\n"
    red

WithContext
===========

A node representing a with statement.

.. ipython:: python

    RedBaron("with a: pass")[0].help(deep=True)

WithContextItemNode
===================

A node representing one of the context manager items in a with statement.

.. ipython:: python

    RedBaron("with a as b: pass")[0].contexts[0].help(deep=True)

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

WithNode
========

A node representing a with statement.

.. ipython:: python

    RedBaron("with a as b, c: pass")[0].help(deep=True)

SetAttr
-------

WithNode is a CodeBlockNode which means its value attribute accepts a wide range
of values, see :ref:`CodeBlockNode` for more information. Other attributes
work as expected:

.. ipython:: python

    red = RedBaron("with a: pass")
    red
    red[0].contexts = "b as plop, stuff()"
    red

*New in 0.8*.

Async is a boolean attribute that determine if a function is async:

.. ipython:: python

    red =  RedBaron("with a as b: pass")
    red[0].async_
    red[0].async_ = True
    red
    red[0].async_ = False
    red

.. WARNING::
   As of python 3.7 `async` and `await` are now reserved keywords so don't uses
   `red.async`, it works as expected but won't make your code forward
   compatible.
