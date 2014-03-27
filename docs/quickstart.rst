Tutorial
========

Before starting, just a remind of what RedBaron is and is not:

* Baron produces a FST in the form of a big JSON out of a valid python source file. Working directly with a JSON of that size would be boring.
* RedBaron is a tool built to interact with this JSON in a more easy way by providing an interface heavily inspired by BeautifulSoup, allowing to query and modify it.
* **It is not a refactoring library**. But it allows you to write one way more easily that anything else I'm aware of.
* Remember that despite all my efforts to make this a more realistic task, refactoring is still a **hard** problem.

This tutorial will teach you first the basics, then how to query the Baron FST
using RedBaron and finally how to modify it.

Basics
------

RedBaron is very simple to use, you just need to import it and feed him with a string:

.. code-block:: python

    from redbaron import RedBaron

    red = RedBaron("print 'hello world!'")

But what you should be really doing is using RedBaron directly into a shell (I
recommend `IPython <http://ipython.org/>`_ but
`bpython <http://bpython-interpreter.org/>`_ is cool too), it has been thought
for it, like BeautifulSoup.

.. code-block:: python

    In [1]: from redbaron import SemicolonNode

    In [2]: red = RedBaron("hello = 'Hello World!'\nprint hello")

    In [3]: red
    Out[3]:
    0   hello = 'Hello World!'
    1   '\n'
    2   print hello

As you can see, when displayed, a RedBaron instance renders to the actual
content so you easily see what you are doing when playing interactively with it
(just like a BeautifulSoup instance).

There are 2 families of Node in RedBaron: NodeList and standalone Node. Since a
Python program is a list of operations, RedBaron will always be a NodeList.
This is why when displayed you see integers on the left, those are the index in
the list of the nodes of the right, so as expected:

.. code-block:: python

    In [4]: red[2]
    Out[4]: print hello

You get the `print` Node that was located at 2. As you can see, here we are on a
standalone Node, so we don't get the list of indexes of the left.

.help()
~~~~~~~

Another useful function is :file:`.help()`. It displays the RedBaron nodes tree
helping you understand how is it composed and how you can use it:

.. code-block:: python

    In [5]: red[0]
    Out[5]: hello = 'Hello World!'

    In [6]: red[0].help()
    AssignmentNode()
      target ->
        NameNode()
          value='hello'
      value ->
        StringNode()
          value="'Hello World!'"


Here, as you can see, :file:`hello = 'Hello World!'` is an
:file:`AssignmentNode` and it has 2 attributes: :file:`target` and
:file:`value`. Those 2 attributes are 2 other nodes, a :file:`NameNode` for the
variable :file:`hello` and a :file:`StringNode` for the string. Those 2 nodes
each have one attribute :file:`value` that is their content.

One rule with Baron: **every node has a value attribute** that contains its
value (in case of a node with multiple data, :file:`value` points to the most
obvious one, for example, in a function definition it's the body of the
function). The **only exceptions** are nodes where it doesn't make any sense,
for example a :file:`PassNode` (representing the keyword :file:`pass`) simply
doesn't contains anything.

Like the :file:`repr`, :file:`.help()` have also a display showing index number
when called on a :file:`NodeList`:

.. code-block:: python

    In [14]: red.help()
    0 -----------------------------------------------------
    AssignmentNode()
      target ->
        NameNode()
          value='hello'
      value ->
        StringNode()
          value="'Hello World!'"
    1 -----------------------------------------------------
    EndlNode()
      indent=''
      value='\n'
    2 -----------------------------------------------------
    PrintNode()
      destination=None
      value ->
        * NameNode()
            value='hello'
