.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

    from redbaron import RedBaron


Modifying helpers
=================

.. _Node.from_fst:

Node.from_fst()
---------------

:file:`Node.from_fst()` is an helper class method that takes a FST node and return a
RedBaron node instance. Except if you need to go down at a low level or that
RedBaron doesn't provide the helper you need, you shouldn't use it.

.. ipython:: python

    from redbaron import Node
    Node.from_fst({"type": "name", "value": "a"})

:file:`Node.from_fst()` takes 2 optional keywords arguments: :file:`parent` and
:file:`on_attribute` that should respectively be RedBaron node instance (the
parent node) and a string (the attribute of the parent node on which this node
is stored). See :ref:`parent` doc for a better understanding of those 2
parameters.

.. ipython:: python

    red = RedBaron("[1,]")
    new_name = Node.from_fst({"type": "name", "value": "a"}, parent=red[0], on_attribute="value")
    red[0].value.append(new_name)

NodeList.from_fst()
-------------------

Similarly to :file:`Node.from_fst()`, :file:`NodeList.from_fst()` is an helper
class method that takes a FST node **list** and return a RedBaron node **list**
instance. Similarly, you probably don't need to go so low level.


.. ipython:: python

    from redbaron import NodeList
    NodeList.from_fst([{"type": "name", "value": "a"}, {'first_formatting': [], 'type': 'comma', 'second_formatting': [{'type': 'space', 'value': ' '}]}, {"type": "name", "value": "b"}])

Next
~~~~

To learn some other misc details of RedBaron read :doc:`other`.
