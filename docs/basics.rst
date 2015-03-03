.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

    from redbaron import RedBaron


Basics
======

RedBaron is very simple to use, you just need to import it and feed him with a string:

.. code-block:: python

    from redbaron import RedBaron

    red = RedBaron("print('hello world!')")

But what you should be really doing is using RedBaron directly into a shell (I
recommend `IPython <http://ipython.org/>`_ but
`bpython <http://bpython-interpreter.org/>`_ is cool too), it has been thought
for it, like BeautifulSoup.

.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

.. ipython:: python

    from redbaron import RedBaron
    red = RedBaron("hello = 'Hello World!'\nprint(hello)")
    red

As you can see, when displayed in a shell, a RedBaron instance renders to the actual
content so you easily see what you are doing when playing interactively with it
(just like a BeautifulSoup instance).

There are 2 families of Node in RedBaron: NodeList and standalone Node. Since a
Python program is a list of operations, RedBaron will always be a list.
This is why when displayed you see integers on the left, those are the index in
the list of the nodes of the right, so as expected:

.. ipython::

    In [4]: red[1]

You get the `print` Node that was located at 2. As you can see, here we are on a
standalone Node, so we don't get the list of indexes of the left.

.. _help():

.help()
-------

Another useful function is :file:`.help()`. It displays the RedBaron nodes tree
helping you understand how is it composed and how you can use it:

.. ipython::

    In [5]: red[0]

    In [6]: red[0].help()

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
doesn't contain anything.

Like the :file:`repr`, :file:`.help()` has also a display showing index number
when called on a :file:`NodeList`:

.. ipython::

    In [14]: red.help()

The best way to understand how :file:`.help()` works is to remember that
RedBaron is mapping from Baron FST which is JSON. This means that RedBaron node
can be composed of either: string, bool, numbers, list or other nodes and the
key are always string.

helpers
~~~~~~~

Some nodes come with helpers method, :file:`.help()` displays them when they
are present:

.. ipython:: python

    red = RedBaron("import a, b, c as d")
    red.help(deep=1)

You can read their documentation using the :file:`?` magic of ipython:

.. ipython:: python

    print(red[0].names.__doc__)  # you can do "red[0].names?" in IPython shell
    red[0].names()

    print(red[0].modules.__doc__)
    red[0].modules()

If you come with cool helpers, don't hesitate to propose them in a `pull
request <https://github.com/Psycojoker/redbaron>`_!

deep
~~~~

:file:`.help()` accept a deep argument on how far in the tree it should show
the :file:`.help()` of subnode. By default its value is :file:`2`. You can pass
the value :file:`True` if you want to display the whole tree.

.. ipython:: python

    red = RedBaron("a = b if c else d")
    red.help()
    red.help(0)
    red.help(deep=1)  # you can name the argument too
    red.help(True)

with_formatting
~~~~~~~~~~~~~~~

:file:`.help()` accepts the option :file:`with_formatting` that is set at
:file:`False` by default. If set at :file:`True` it will also display the
attributes responsible for holding the formatting of the node (they are always
node list):

.. ipython::

    In [12]: red.help(with_formatting=True)

Those attributes are always surrounding syntax element of Python like
:file:`[](),.{}` or keywords. You should, normally, not have a lot of reasons
to play with them. You can find a detailed version of each nodes here:
:doc:`nodes_reference`.

nodes structure
---------------

Nodes can have 3 kind of attributes (which can be accessed like normal object
attributes):

* data attributes, which are nearly always strings. They are shown with a :file:`=` in
  :file:`.help()`. :file:`.value` here for example.

.. ipython::

    In [1]: red = RedBaron("variable")

    In [2]: red[0].help()

    In [3]: red[0].value

* node attributes, which are other nodes. They are shown with a :file:`->` followed by the name of the other node
  at the next line in :file:`.help()`. :file:`.target` and :file:`.value` here for example.

.. ipython::

    In [19]: red = RedBaron("a = 1")

    In [20]: red[0].help()

    In [21]: red[0].target.help()

* nodelist attributes, which are lists of other nodes. They are shown with a :file:`->` followed by a series of names
  of the other nodes starting with a :file:`*` for every item of the list. :file:`.value` here for example:

.. ipython::

    In [17]: red = RedBaron("[1, 2, 3]")

    In [18]: red[0].help()

    In [19]: red[0].value[0].help()

.dumps(), transform the tree into source code
---------------------------------------------

To transform a RedBaron tree back into source code, use the
:file:`.dumps()` method. This will transform the **current selection** back
into code.

.. ipython::

    In [26]: red = RedBaron("a = 1")

    In [27]: red.dumps()

    In [28]: red[0].target.dumps()

.fst(), transform the RedBaron tree into Baron FST
--------------------------------------------------

To transform a RedBaron tree into Baron Full Syntax Tree, just use the
:file:`.fst()` method. This will transform the **current selection** into FST.

.. ipython::

    In [28]: red = RedBaron("a = 1")

    In [29]: red.fst()

    In [30]: red[0].target.fst()

While I don't see a lot of occasions where you might need this, this will
allow you to better understand how Baron and RedBaron are working.

.copy()
-------

If you want to copy a RedBaron node you can use the :file:`.copy()` method this
way:

.. ipython::

    In [45]: red = RedBaron("a = b")

    In [52]: red[0].target.copy()


Next
~~~~

To learn how to find things in RedBaron read :doc:`querying`.
