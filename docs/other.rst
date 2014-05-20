.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    from redbaron import RedBaron


Other
=====

List of other features of RedBaron.

.. _parent:

.parent
-------

Every node and node list have a :file:`.parent` attribute that points to the
parent node or node list. If the node doesn't have a parent node (for example
the node list returned when constructing a new instance using the
:file:`RedBaron` class), the :file:`parent` attribute is set at :file:`None`. A
new node or node list created using :file:`.copy()` always have its
:file:`parent` attribute set at :file:`None`.

The attribute on which the node is assigned on the parent node is store in the
:file:`on_attribute` attribute. :file:`on_attribute` is set at :file:`"root"`
if the parent is a RedBaron instance.


.. ipython:: python

    red = RedBaron("a = 1 + caramba")
    red.help()
    red.parent
    red.on_attribute
    red[0].parent
    red[0].on_attribute
    red[0].target.parent
    red[0].target.on_attribute
    red[0].value.parent
    red[0].value.on_attribute
    red[0].value.first.parent
    red[0].value.first.on_attribute

.parent_find()
--------------

A helper method that allow you to do the equivalent of the :file:`.find()`
method but in the chain of the parents of the node. This is the equivalent of
doing: :file:`while node has a parent: if node.parent match query: return
node.parent, else: node = node.parent`. It returns :file:`None` if not parent
match the query.

.. ipython:: python

    red = RedBaron("def a():\n    with b:\n        def c():\n            pass")
    red.help()
    r = red.pass_
    r
    r.parent
    r.parent_find('def')
    r.parent_find('def', name='a')
    r.parent_find('def', name='dont_exist')

.next .previous .next_generator() .previous_generator()
-------------------------------------------------------

In a similar fashion, node have a :file:`.next` and :file:`.previous`
attributes that point to the next or previous node if the node is located in a
node list. They are set at :file:`None` if their is not adjacent node or if the
node is not in a node list. A node list will never have a :file:`.next` or
:file:`.previous` node, so those attributes will always be set at :file:`None`.

Nodes also have a :file:`.next_generator()` and :file:`.previous_generator()`
if you want to iterate on the neighbours of the node.

.. ipython::

    In [42]: red = RedBaron("[1, 2, 3];a = 1")
    In [42]: red.help()

    In [42]: list = red[0]

    In [42]: print list.next
    In [42]: print list.previous

    In [42]: list.help()
    In [42]: print list.value[0]
    In [42]: print list.value[0].next
    In [42]: print list.value[0].previous
    In [42]: print list.value[2]
    In [42]: print list.value[2].next
    In [42]: print list.value[2].previous

    In [42]: assign = red[2]

    In [42]: assign.help()
    In [42]: print assign.target.next
    In [42]: print assign.target.previous

    In [42]: list.value[2].help(deep=1)
    In [42]: print [x for x list.value[2].next_generator()]
    In [42]: print [x for x list.value[2].previous_generator()]
    In [42]: list.value.help(deep=0)
    In [42]: print [x for x list.value.next_generator()]
    In [42]: print [x for x list.value.previous_generator()]
    In [42]: print [x for x assign.target.next_generator()]
    In [42]: print [x for x assign.target.previous_generator()]

.filtered()
-----------

Node list comes with a small helper function: :file:`.filtered()` that returns
a **tuple** containing the "signifiant" node (nodes that aren't comma node, dot
node, space node or endl node).

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red[0].value
    red[0].value.filtered()

Note: the fact that it's a tuple that is returned will probably evolve in the
futur into a node list proxy or something like that, I just don't have the time
to do something better right now.

.indentation
------------

Every node have the property :file:`.indentation` that will return the
indentation level of the node:

.. ipython:: python

    red = RedBaron("while a:\n    pass")
    red[0].indentation
    red[0].test.indentation
    red.pass_.indentation

    red = RedBaron("while a: pass")
    red.pass_.indentation
