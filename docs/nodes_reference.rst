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
