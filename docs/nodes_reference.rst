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

IntNode
=======

A python integer.

.. ipython:: python

    RedBaron("42")[0].help(with_formatting=True)

SpaceNode
=========

A formatting node representing a space. You'll probably never have to deal with
it except if you play with the way the file is rendered.

**Those nodes will be hidden in formatting keys 99% of the time** (the only exception is if it's the last node fo the file).

.. ipython:: python

    RedBaron("1 + 1")[0].first_formatting[0].help(with_formatting=True)
    RedBaron("1 + 1").help(with_formatting=True)
