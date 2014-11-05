.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

    from redbaron import RedBaron


Modifying
=========

Principle
---------

When it comes to modifying the tree, the normal classical way would tell you to
use the RedBaron nodes constructors, like this:

.. ipython::

    In [54]: from redbaron import RedBaron, NameNode

    In [55]: red = RedBaron("a = 1")

    In [56]: red[0].value

    In [57]: red[0].value = NameNode({'first_formatting': [{'type': 'space', 'value': ' '}], 'value': '+', 'second_formatting': [{'type': 'space', 'value': ' '}], 'second': {'section': 'number', 'type': 'int', 'value': '1'}, 'type': 'binary_operator', 'first': {'section': 'number', 'type': 'int', 'value': '1'}})

    In [58]: red

As you can see, this is totally impracticable. So, to solve this problem,
RedBaron adopt a simple logic: you already know how to code in python, so, just
send python code in form of a string, RedBaron will takes care or parsing and
injecting it into its tree. This give an extremely simple and intuitive API:

.. ipython::

    In [55]: red = RedBaron("a = 1")

    In [56]: red[0].value

    In [57]: red[0].value = "1 + 1"

    In [58]: red

The details on how you can modify **every** nodes can be found here: :doc:`nodes_reference`.

Code block modifications
------------------------

The modification of python code block (like the body of a function or a while
loop) is also possible this way. RedBaron will takes care for you or formatting
you input the right way (adding surrounding blank lines and settings the
correct indentation for the every line).

Example:

.. ipython:: python

    red = RedBaron("while True: pass")
    red[0].value = "plop"
    red
    red[0].value = "                        this_will_be_correctly_indented"
    red

You have the full list of cases handled on this page: :doc:`nodes_reference`.

Details
-------

As you might have already noticed, you can set attributes of a node with a
string or a RedBaron node. This is also possible by directly passing FST.

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
a :file:`fst node`, an instance of a node or a node list.

The same is done for :file:`.on_attribute`.

Next
~~~~

To learn how to work with list of things in RedBaron read :doc:`proxy_list`.
