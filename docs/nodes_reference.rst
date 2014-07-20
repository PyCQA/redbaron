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

CodeBlockNode are a type of node that have a body composed of indented code
like the FuncdefNode or the IfNode. Great care has been taken on the SetAttr of
their value so you don't have to take care about reindenting and other
formating details.

Demontration:

.. ipython:: python

    red = RedBaron("def function():\n    pass\n")
    red
    red[0].value = "stuff"  # first '\n' will be hadded, indentation will be set
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

DictNode
========

A node representing python sugar syntaxic notation for dict.

.. ipython:: python

    RedBaron("{'a': 1, 'b': 2, 'c': 3}")[0].help(deep=True, with_formatting=True)

Helpers
-------

DictNode comes with one helper to add another item at the end of the value of
the node without having to think about formating. It is documented here:
:ref:`append_value`. **Warning**: :file:`append_value` of DictNode has a
different signature than the append_value of other nodes: it expects 2
arguments: one of the key and one of the value.

.. ipython:: python

    red = RedBaron("{}")
    red[0].append_value(key="'a'", value="42")
    red


EndlNode
========

A node for the end line ('\n', '\r\n') component.

**This node is responsible for holding the indentation AFTER itself**. This
node also handle formatting around it, CommentNode **before** an EndlNode will
end up in the formatting key of an EndlNode 99% of the time (the exception is
if the CommentNode is the last node of the file).

.. ipython:: python

    RedBaron("suff\n")[1].help(with_formatting=True)
    RedBaron("# first node of the file\n# last node of the file").help(with_formatting=True)


FuncdefNode
===========

A node representing a function definition.

.. ipython:: python

    RedBaron("def stuff():\n    pass\n")[0].help(deep=True, with_formatting=True)

SetAttr
-------

FuncdefNode is a CodeBlockNode whichs means its value attribute accept a wide
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
of the node without having to think about formating. It is documented here:
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
the node without having to think about formating. It is documented here:
:ref:`append_value`.


ReprNode
========

A node representing python sugar syntaxic notation for repr.

.. ipython:: python

    RedBaron("`pouet`")[0].help(deep=True, with_formatting=True)

Helpers
-------

SetNode comes with one helper to add another item at the end of the value of
the node without having to think about formating. It is documented here:
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

**Those nodes will be hidden in formatting keys 99% of the time** (the only exception is if it's the last node fo the file).

.. ipython:: python

    RedBaron("1 + 1")[0].first_formatting[0].help(with_formatting=True)
    RedBaron("1 + 1").help(with_formatting=True)


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
