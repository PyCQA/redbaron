.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False
    from redbaron import RedBaron

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

While you don't have to do that, it might helps your understanding of RedBaron
to see the procude FST (every key that has "_formatting" in its name is ...
formatting related, you can ignore it):

.. ipython:: python

    import json

    red = RedBaron("1+2")
    print json.dumps(red.fst(), indent=4)

Use it in a shell
-----------------

Now that you should have understand the concept of the source code as a tree,
let's explore it.

First, like BeautifulSoup, when used in a shell RedBaron display the currently
selected source code, so you'll have a direct idea of what you are working on:

.. ipython:: python

    red = RedBaron("stuff = 1 + 2\nprint 'Hello', stuff")
    red

You might notice the :file:`0` and the :file:`1` on the left: those are the
indexes of the 2 nodes in the root of the source code (because a source code is
a list of statements). See by yourself:

.. ipython:: python

    red[0]
    red[1]

But now, how to access the attributes? Since reading the doc for every node is
boring, RedBaron comes with a helper method that shows you the underlying
structure of the currently selected nodes:

.. ipython:: python

    red[0]
    red[0].help()

The output might be a bit scary at first, but what is shows you is simply the
underlying structure that is map to the one of the JSON or Baron. Here: we are
on an AssignmentNode (something like :file:`a = b`) that has 3 attributes:
operator, target and value. The operator is an empty string (it could has been
a python operator like :file:`+` in a case like :file:`a += b`) and target and
value which point to other nodes (notice the :file:`->` instead of a :file:`=`
in the output).

Let's try it:

.. ipython:: python

    red[0]
    red[0].operator
    red[0].target
    red[0].value

The last kind of attributes that you might are list like here for the print
statement:

.. ipython:: python

    red[1].help()

Notice the :file:`*` before :file:`StringNode` and :file:`NameNode`? That
indicates that their are items of a list (on the attribute value). Look:

.. ipython:: python

    red[1]
    red[1].value
    red[1].value[0]
    red[1].value[1]

And *voilà*, you now know how to navigate the tree by attributes without having
to read any documentation.

And one last thing: by default :file:`.help()` stops at a certain deep and
displays :file:`...` instead of going further. To avoid that, simply pass an
integer that indicate the deep or :file:`True` if you want to display the whole tree.

::

    red.help(4)
    red.help(True)

You can read the whole documentation of :file:`.help` here: :ref:`help()`

Querying
--------

Again, querying is very inspired by BeautifulSoup. You have 2 methods:
:file:`.find` and :file:`.find_all`. Those 2 methods accept the same arguments.
The first one returns the first matched node and the second one, a list of all
the matched nodes.

The first argument is a string that represent the kind of the node you want to
match on. This is the "identifiers" displayed by :file:`.help()`. Example:

.. ipython:: python

    red
    red.help()
    red.find("assignment")
    red.find("print")
    red.find_all("int")

Then, you can pass as many keyword arguments as you want, those keywords
arguments will test the attributes of the node and select it if all attributes
match:

.. ipython:: python

    red.find("int", value=2)

The only special argument you can pass is :file:`recursive` that determine if
the query is done recursively. By default it is set at :file:`True`, just pass
:file:`recursive=False` to :file:`.find` or :file:`.find_all` to avoid that.

Queries are very powerful: you can pass lambda, regex, a short hand syntax for
regex and globs, a tuple of string instead of a string for the type of nodes, a
global regex that receives the node (instead of a regex per attribute) etc...
You can read all of that here: :doc:`querying`.

:file:`.find` and :file:`.find_all` also have a shortcut syntax (exactly like
in BeautifulSoup), just have a look:

.. ipython:: python

    red.int  # is the equivalent of red.find("int")
    red("int", value=2)  # is the equivalent of red.find_all("int", value=2)

Modification
------------

Nodes modification is extremely simple in RedBaron: you just have to set the
attribute of the node you want to modify with a string containing python source
code. Just look by yourself:

.. ipython:: python

    red
    red[0].target = "something_else"
    red[0].value = "42 * 34"
    red
    red[1].value = "'Hello World!'"
    red

And *voilà*, you can't get easier than that. You can also pass RedBaron node
objects (or FST) that you have obtain is some way or another, for example by
using :file:`.copy()`:

.. ipython:: python

    red
    i = red[0].value.copy()
    red[1].value = i
    red

You can also replace a node *in place* using the :file:`.replace()` method.
**Warning**: the :file:`.replace()` expect that the string you pass it
represent a whole valid python program (so for example: :file:`.replace("*args,
**kwargs")` won't work). This limitation should be raised in the future.

.. ipython:: python

    red
    red[0].value.replace("1234")
    red

This is generally very useful when working on queries. For example (a real life
example), here is the code to replace every :file:`print stuff` (prints
statement of **one** argument, the one with multiple arguments is left to the
reader as exercice) with :file:`logger.debug(stuff)`:

::

    red("print", value=lambda x: len(x) == 1).map(lambda x: x.replace("logger.debug(%s)" % x.value.dumps()))

(:file:`.map()` will be covered at the end of the tutorial but should speak for itself.)

You can read everything about modifications in RedBaron here: :doc:`modifying`

Playing with list of nodes
--------------------------

Last big concept of RedBaron: how to handle list of nodes. The problem for
short is that, for a python developer the list :file:`[1, 2, 3]` has 3 items,
while in the FST world, it has 5 items because you need to take into account
the commas. This is a pattern that you find in every list of nodes, the
separator being either commas, dot (eg: :file:`a.b(c)[d]`) or end of line
character (for line of code).

Having to deal with those separator is extremely annoying and error prone, so,
RedBaron offers you an abstraction that hides all of this for you! You just
have to deal with those list of nodes like if they were regular python list and
everything will fine. See by yourself:

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red.help()
    red[0].value  # see: no explicit commas to deal with
    red[0].value.append("4")
    red  # comma has been added for us

This abstraction is called a proxy list. Those proxy list can even detect
indentation style for comma separated lists:

.. ipython:: python

    red = RedBaron("[\n    1,\n    2,\n    3\n]")
    red
    red[0].value.append("caramba")
    red

This also work with nodes separated by dots:

.. ipython:: python

    red = RedBaron("a.b(c)[d]")
    red
    red[0].value.extend(["e", "(f)", "[g:h]"])
    red

And lines of code (notice that the blank line is explicitly shown):

.. ipython:: python

    red = RedBaron("a = 1\n\nprint a")
    red
    red.insert(1, "if a:\n    print 'a == 1'")
    red

* every methods and protocols of python lists (expect :file:`sort` and :file:`reversed`) works on proxy list.
* every list of nodes in python is wrapped by a proxy list.

The raw list is stored on the :file:`.node_list` attribute of the proxy list:

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red[0].node_list

**Warning**: the proxyfied list and the proxy list are only sync from the proxy
list to the proxyfied list. If you start to modify the proxyfied list, don't
use the proxy list anymore or you'll have strange bugs! This might changes in
the future.

One last thing: if the proxy list is stored on the :file:`.value` attribute,
you can omit to access this attribute and directly called on the holder node.
This is done because it is more intuitive, see by yourself:

::

    red = RedBaron("[1, 2, 3]")

    red[0].append("4")  # is exactly the same than the next line
    red[0].value.append("4")

Misc things
-----------

A short list of useful features of RedBaron:

* :file:`.map`, a method of RedBaron lists that takes a callable (like a lambda or a function), apply it to every one of its members and returns a RedBaron list containing the result of the call
* :file:`.apply` same than :file:`.map` except it returns a RedBaron list of the nodes on which the callable has been applied (instead of the result of the call)

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red("int").map(lambda x: x.value + 42)
    red("int").apply(lambda x: x.value + 42)

* :file:`.filter`, another method of RedBaron list, it takes a callable and return a RedBaron list containing the nodes for which the callable has return True (or something that is tested has True in python)

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red("int").filter(lambda x: x.value % 2 == 1)  # nombre impairs

* :file:`.next` gives the node just after the current one if the node is in a list
* :file:`.previous` dot the inverse
* :file:`.parent` gives the holder of this node

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red.int_
    red.int_.next
    red.int_.previous  # None because nothing is behind it
    red.int_.parent

And you can find all the others various RedBaron features here: :doc:`other`
