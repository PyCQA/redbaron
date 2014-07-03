.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

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
node.parent, else: node = node.parent`. It returns :file:`None` if no parent
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

In a similar fashion, nodes have a :file:`.next` and :file:`.previous`
attributes that point to the next or previous node if the node is located in a
node list. They are set at :file:`None` if there is not adjacent node or if the
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
a **tuple** containing the "significant" node (nodes that aren't comma node, dot
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

Every node has the property :file:`.indentation` that will return the
indentation level of the node:

.. ipython:: python

    red = RedBaron("while a:\n    pass")
    red[0].indentation
    red[0].test.indentation
    red.pass_.indentation

    red = RedBaron("while a: pass")
    red.pass_.indentation

.path()
-------

Every node has a :file:`path()` method that will return a :file:`Path` object
to it. Every path object has a :file:`.node` attribute that point to the node
and a :file:`.to_baron_path` that returns a `Baron Path namedtuple
<https://baron.readthedocs.org/en/latest/#locate-a-node>`_.

.. ipython:: python

    red = RedBaron("while a:\n    pass")
    red.pass_
    path = red.pass_.path()

    path

    path.node
    path.to_baron_path()

Path class
----------

RedBaron provides a Path class that represent a path to a node.

.. autoclass:: redbaron.Path

.map .filter .apply
-------------------

RedBaron nodes list have 3 helper methods :file:`.map`, :file:`.filter` and :file:`.apply` quite similar to python buildins (except for apply). The main difference is that they return a node list instance instead of a python buildin list.

* :file:`.map` takes a callable (like a lambda or a function) that receive a
  node as first argument, this callable is applied on every node of the node
  list and a node list containing the return of those applies will be returned.
* :file:`.filter` works like :file:`.map` but instead of returning a node list
  of the return of the callable, it returns a node list that contains the nodes
  for which the callable returned :file:`True` (or something considered
  :file:`True` in python)
* :file:`.apply` works like :file:`.map` but instead of returning the result of
  the callable, it returns to original node.

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red('int')
    red('int').map(lambda x: x.value + 1)
    red('int').filter(lambda x: x.value % 2 == 0)

.. ipython:: python

    red = RedBaron("a()\nb()\nc(x=y)")
    red('call')
    red('call').map(lambda x: x.append_value("answer=42"))
    red('call')
    red = RedBaron("a()\nb()\nc(x=y)")
    red('call').apply(lambda x: x.append_value("answer=42"))

.replace()
----------

:file:`.replace()` is a method that allow to replace **in place** a node by
another one. Like every operation of this nature, you can pass a string, a
dict, a list of length one or a node instance.

.. ipython:: python

    red = RedBaron("a()\nb()\nc(x=y)")
    red[2].replace("1 + 2")
    red
    red[-1].replace("plop")
    red

.edit()
-------

Helper method that allow to edit the code of the current **node** into an
editor. The result is parsed and replace the code of the current node.

.. ipython:: python

    red = RedBaron("def a(): return 42")
    # should be used like this: (I can't execute this code here, obviously)
    # red.return_.edit()

By default, the editor is taken from the variable :file:`EDITOR` in the
environements variables. If this variable is not present, nano is used. You can
use a different editor this way: :file:`node.edit(editor="vim")`.
