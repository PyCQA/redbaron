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

    red.fst()  # return the full syntax tree in form a json serialisable python datastructure (dictionnary and list of string/bool/ints)
