========
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
======

RedBaron is very simple to use, you just need to import it and feed him with a string:

.. code-block:: python

    from redbaron import RedBaron

    red = RedBaron("print 'hello world!'")

But what you should be really doing is using RedBaron directly into a shell (I
recommend `IPython <http://ipython.org/>`_ but
`bpython <http://bpython-interpreter.org/>`_ is cool too), it has been thought
for it, like BeautifulSoup.

.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

.. ipython:: python

    from redbaron import RedBaron
    red = RedBaron("hello = 'Hello World!'\nprint hello")
    red

As you can see, when displayed, a RedBaron instance renders to the actual
content so you easily see what you are doing when playing interactively with it
(just like a BeautifulSoup instance).

There are 2 families of Node in RedBaron: NodeList and standalone Node. Since a
Python program is a list of operations, RedBaron will always be a NodeList.
This is why when displayed you see integers on the left, those are the index in
the list of the nodes of the right, so as expected:

.. ipython::

    In [4]: red[2]

You get the `print` Node that was located at 2. As you can see, here we are on a
standalone Node, so we don't get the list of indexes of the left.

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
doesn't contains anything.

Like the :file:`repr`, :file:`.help()` have also a display showing index number
when called on a :file:`NodeList`:

.. ipython::

    In [14]: red.help()

nodes structure
---------------

Nodes can have 3 kind of attributes (which can be accessed like normal object
attributes):

* data attributes which are nearly always strings, they are shown with a :file:`=` in
  :file:`.help()`. :file:`.value` here for example.

.. ipython::

    In [1]: red = RedBaron("variable")

    In [2]: red[0].help()

    In [3]: red[0].value

* node attributes which are other nodes, they are shown with a :file:`->` followed by the name of the other node at the next line in :file:`.help()`. :file:`.target` and :file:`.value` here for example.

.. ipython::

    In [19]: red = RedBaron("a = 1")

    In [20]: red[0].help()

    In [21]: red[0].target.help()

* nodelist attributes which are a list of other nodes, they are shown with a :file:`->` followed by a series of names of the other nodes starting with a \* for every item of the list. :file:`.value` here for example:

.. ipython::

    In [17]: red = RedBaron("[1, 2, 3]")

    In [18]: red[0].help()

    In [19]: red[0].value[0].help()

.dumps(), transform the tree into source code
---------------------------------------------

To transform a RedBaron tree back into source code, just use the
:file:`.dumps()` method. This will transform the **current selection** back
into code.

.. ipython::

    In [26]: red = RedBaron("a = 1")

    In [27]: red.dumps()

    In [28]: red[0].target.dumps()

.fst(), transform the redbaron tree into baron FST
--------------------------------------------------

To transform a RedBaron tree into Baron Full Syntax Tree, just use the
:file:`.fst()` method. This will transform the **current selection** into FST.

.. ipython::

    In [28]: red = RedBaron("a = 1")

    In [29]: red.fst()

    In [30]: red[0].target.fst()

While I don't see a lot of occasions where you might need this, this will
allows you to better understand how Baron and RedBaron are working.

.copy()
-------

If you want to copy a RedBaron node you can use the :file:`.copy()` method this
way:

.. ipython::

    In [45]: red = RedBaron("a = b")

    In [52]: red[0].target.copy()


Querying
========

As you have seen in the previous section, you can navigate into RedBaron tree
only using attribute access and index access on list of nodes with the use of
the :file:`.help()` method to know what you can do. However, RedBaron offers
way more powerful and convenient tools to do that.

.find()
-------

To retrieve a single node, you can use the :file:`.find()` method by passing it
the name of node you want to get, this way:

.. ipython::

    In [31]: red = RedBaron("a = 1")

    In [35]: red.find('NameNode').help()

This will recursively travel the tree and return the first node of that type.

You can also specify attributes of the node that you want to match:

.. ipython::

    In [36]: red = RedBaron("a = b")

    In [37]: red.find('NameNode').help()

    In [38]: red.find('NameNode', value='b').help()

If you don't want a recursive approach but only on the first level on the current node or node list, you can pass :file:`recursive=False` to :file:`.find()`.

Like BeautifulSoup, RedBaron provides a shorthand to :file:`.find()`, you can
write the name of the target as an attribute of the node and this will do a :file:`.find()` in the same fashion:

.. ipython::

    In [39]: red = RedBaron("a = b")

    In [40]: red.find('NameNode')

    In [41]: red.NameNode

Writing :file:`StuffNode` every time is a bit boring, so you can alternatively
use :file:`stuff` (or 'Stuff', it's not case sensitive) or :file:`stuff_` for
when :file:`stuff` is a reserver keyword of the python language (examples:
:file:`if`, :file:`with`, :file:`while`...).

.. ipython::

    In [39]: red = RedBaron("a = b")

    In [40]: red.NameNode

    In [41]: red.name

    In [42]: red.name_

.find_all()
-----------

:file:`.find_all()` is extremely similar to :file:`.find()` except it return a
node list contains all the matching queries instead on a single one. Like in
BeautifulSoup, :file:`__call__` is aliased to :file:`find_all` (meaning that if
you try to *call* the node this way :file:`node(some_arguments)` this will call
:file:`.find_all()` with the arguments).

.. ipython::

    In [45]: red = RedBaron("a = b")

    In [46]: red.find_all("NameNode")

    In [47]: red.find_all("name")

    In [48]: red.findAll("name")

    In [49]: red.findAll("name", value="b")

    In [50]: red("name", value="b")

:file:`.find_all()` also supports the option :file:`recursive=False`.


Modifying
=========

This is obviously one of the main usage of what you'll want to do with
RedBaron. Thankfully, RedBaron provides ways to help you do that.

Obvious boring and annoying way to do that
------------------------------------------

This is the way of doing things that you'll probably never want to have to do.
You can construct by hand new RedBaron nodes and attach them to existing node's
attributes. This is very boring to do since you need to construct everything by
hand and that RedBaron node except Baron FST as first argument, but knowing how
to do this might proves itself useful in some situation to bypass RedBaron
limitations. Warning: it's very easy to break things doing this, absolutely no
protection mechanisms are in place.

Example:

.. ipython::

    In [54]: from redbaron import RedBaron, NameNode

    In [55]: red = RedBaron("a = 1")

    In [56]: red[0].value

    In [57]: red[0].value = NameNode({"type": "name", "value": "stuff"})

    In [58]: red

Taking advantage of __setattr__
-------------------------------

While paying the price of magic, RedBaron exploit the power of overloading
__setattr__ to allow you to write things like:

.. ipython::

    In [64]: from redbaron import RedBaron

    In [65]: red = RedBaron("a = 1")

    In [66]: red[0].value = "(1 + 3) * 4"

    In [67]: red[0]

Yep, if you pass assign a string to a node attribute, RedBaron will
automatically parse it with RedBaron then assign the result at the place of the
previous node.

Here is an IPython session illustrating all the possibilities (be sure to have
read the "node structures" in basics to understand what is happening):

.. ipython::

    In [70]: from redbaron import RedBaron

    In [71]: red = RedBaron("a = b")

Data attribute, no parsing
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython::

    In [72]: red.name.help()

    In [73]: red.name.value = "something_else"

    In [74]: red

Node attribute with a string: parsing with RedBaron
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython::

    In [75]: red[0].help()

    In [76]: red[0].value = "42 * pouet"

    In [77]: red

Node attribute with FST data: transformation into RedBaron objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython::

    In [79]: red[0].value = {"type": "name", "value": "pouet"}

    In [80]: red

List attribute with a string: parsing with RedBaron
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython::

    In [81]: red = RedBaron("[1, 2, 3]")

    In [82]: red[0].help()

    In [83]: red[0].value = "caramba"

    In [84]: red

    In [85]: red[0].value = "4, 5, 6"

    In [86]: red

List node attribute with FST: transformation into RedBaron objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython::

    In [87]: red[0].value = {"type": "name", "value": "pouet"}

    In [88]: red


    In [89]: red[0].value = [{"type": "name", "value": "pouet"}]

    In [90]: red

List node attribute with mixed content: parsing/transformation depending of the context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython::

    In [103]: red[0].value = [{"type": "name", "value": "pouet"}, {"type": "comma", "first_formatting": [], "second_formatting": []}, "pouet ,", NameNode({"type": "name", "value": "plop"})]

    In [104]: red

Limitations
-----------

As of today, this magical parsing on string has a **big** limitation: it is
expecting something parsable by Baron which only parse a **valid python
program**. That means that string passed in a __setattr__ case have to be an
entire valid python program that the command :file:`python` can execute. This
mean that you wouldn't have been able to write something like this in the
previous example:

.. ipython::

    In [105]: red[0].value = ["a", ", ", "b"]

As you can guess :file:`","` is not a valid python program.

This will be fixed in the future but this require quite a lot of work to be
done correctly and other things are more urgent.
