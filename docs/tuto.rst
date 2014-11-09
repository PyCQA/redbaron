.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

Learn how to use RedBaron
=========================

This tutorial intent to guide you through the big principles of RedBaron and
highlight the most useful helpers and tricks. It is more or less a lighter
version version of the already existing documentation.

A reminder before starting:

* **RedBaron doesn't do static analysis** and will never do (but it's very likely that it will be combined with tools that do it like astroid or rope to bring static analysis into RedBaron or easy source code modification in the others)

The structure of this tutorial is more or less similar to the documentation one:

* basic principles and how to use it into a shell
* how to query the tree
* how to modify the tree
* how to play with list of things
* misc stuff

Basic principles
----------------

Import, input and output:

.. code-block:: python

    from redbaron import RedBaron

    red = RedBaron("code source as a string")
    red.dumps()  # return a string version of the (possibly modified) tree

    # from a file
    with open("code.py", "r") as source_code:
        red = RedBaron(source_code.read())

    with open("code.py", "w") as source_code:
        source_code.py", "w").write(red.dumps())

    red.fst()  # return the Full Syntax Tree in form json serializable python datastructures (dictionary and list of string/bool/ints)

Now that you loaded your coded into RedBaron, let's talk about the principle of RedBaron:

* when you are writing source code (of any classical language), you are actually writing a tree structure in a source file
* for example: in :file:`1 + 2` the top node is :file:`+`, the left one is :file:`1` and the right one is :file:`2`
* in :file:`(1 + 2) + 3` the top node is, again, :file:`+`, but the left one is actually :file:`(1 + 2)` which is again, another :file:`+` node! and so on and so on
* the classical approach for this is the `Abstract Syntax Tree (AST) <https://en.wikipedia.org/wiki/Abstract_syntax_tree>`_ (it is used by compilers and interpreters like cpython)
* RedBaron is using `Baron <https://github.com/psycojoker/baron>`_ which is producing something sightly different: a Full Syntax Tree (FST), it's like an AST except is keeps every informations possible to be lossless. The FST is in JSON. Also: it has been tough to be used by humans
* So, where BeautifulSoup wrap the HTML datastructure into objects, RedBaron do the same thing for the FST datastructure

Example of an AST for some language that looks like Go:

.. image:: ast.png
