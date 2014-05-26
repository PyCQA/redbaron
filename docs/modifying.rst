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

While paying the price of magic, RedBaron exploits the power of overloading
__setattr__ to allow you to write things like:

.. ipython::

    In [64]: from redbaron import RedBaron

    In [65]: red = RedBaron("a = 1")

    In [66]: red[0].value = "(1 + 3) * 4"

    In [67]: red[0]

Yep, if you assigns a string to a node attribute, RedBaron will
automatically parse it with RedBaron and put the result in the
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

Auto assignment of .parent and .on_attribute
--------------------------------------------

When you modify an attribute of a node or a node list, RedBaron will take care
of setting the :file:`.parent` value of the new attribute to the corresponding
node.

This will be done if you set the attribute value using either a :file:`string`,
a :file:`fst node` or an instance of a node or a node list.

The same is done for :file:`.on_attribute`.

Limitations
-----------

As of today, this magical parsing on string has a **big** limitation: it is
expecting something parsable by Baron which only parse a **valid python
program**. That means that a string passed in a __setattr__ case has to be an
entire valid python program that the command :file:`python` can execute. This
mean that you wouldn't have been able to write something like this in the
previous example:

.. ipython::

    In [105]: red[0].value = ["a", ", ", "b"]

As you can guess :file:`","` is not a valid python program.

This will be fixed in the future but it will require quite a lot of work to be
done correctly and other things are more urgent.

Next
====

To learn advanced modifying function in RedBaron read :doc:`modifying_helpers`.
