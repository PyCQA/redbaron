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

.next .previous .next_recursive .previous_recursive .next_generator() .previous_generator()
-------------------------------------------------------------------------------------------

In a similar fashion, nodes have a :file:`.next` and :file:`.previous`
attributes that point to the next or previous node if the node is located in a
node list. They are set at :file:`None` if there is not adjacent node or if the
node is not in a node list. A node list will never have a :file:`.next` or
:file:`.previous` node, so those attributes will always be set at :file:`None`.

Nodes also have a :file:`.next_generator()` and :file:`.previous_generator()`
if you want to iterate on the neighbours of the node.

Nodes have also a :file:`.next_recursive` and
:file:`.previous_recursive` attribute. It is similar to the non
recursive function but differ in the fact that, when using
:file:`.next_recursive` on a node at the end of the list, it points to
the first adjacent node that exist in the parent hierarchy.

.. ipython::

    In [42]: red = RedBaron("[1, 2, 3]; a = 1")
    In [42]: red.help()

    In [42]: list = red[0]

    In [42]: print(list.next)
    In [42]: print(list.previous)

    In [42]: list.help()
    In [42]: print(list.value[0])
    In [42]: print(list.value[0].next)
    In [42]: print(list.value[0].next_recursive)
    In [42]: print(list.value[0].previous)
    In [42]: print(list.value[0].previous_recursive)
    In [42]: print(list.value[2])
    In [42]: print(list.value[2].next)
    In [42]: print(list.value[2].next_recursive)
    In [42]: print(list.value[2].previous)
    In [42]: print(list.value[2].previous_recursive)

    In [42]: assign = red[2]

    In [42]: assign.help()
    In [42]: print(assign.target.next)
    In [42]: print(assign.target.previous)

    In [42]: list.value[2].help(deep=1)
    In [42]: print([x for x list.value[2].next_generator()])
    In [42]: print([x for x list.value[2].previous_generator()])
    In [42]: list.value.help(deep=0)
    In [42]: print([x for x list.value.next_generator()])
    In [42]: print([x for x list.value.previous_generator()])
    In [42]: print([x for x assign.target.next_generator()])
    In [42]: print([x for x assign.target.previous_generator()])

.next_intuitive/.previous_intuitive
-----------------------------------

Due to its tree nature, navigating in the FST might not behave as the user
expect it. For example: doing a :file:`.next` on a :file:`TryNode` will not
return the first :file:`ExceptNode` (or :file:`FinallyNode`) but will return
the node after the try-excepts-else-finally node because it is a full node in
itself in the FST.

See for yourself:

.. ipython:: python

    red = RedBaron("try:\n    pass\nexcept:\n    pass\nafter")
    red.try_
    red.try_.next
    red.help()

To solve this issue :file:`.next_intuitive` and :file:`.previous_intuitive`
have been introduced:

.. ipython:: python

    red
    red.try_.next_intuitive
    red.try_.next_intuitive.next_intuitive

This also applies to :file:`IfNode`, :file:`ElifNode`, :file:`ElseNode`,
:file:`ForNode` and :file:`WhileNode` (both of the last one can have an else
statement). This also works coming from nodes outsides of those previous nodes.

For :file:`IfNode`, :file:`ElifNode` and :file:`ElseNode` **inside** an
:file:`IfelseblockNode`:

.. ipython:: python

    red = RedBaron("before\nif a:\n    pass\nelif b:\n    pass\nelse:\n    pass\nafter")
    red
    red[1].help()
    red[1]
    red.if_.next
    red.if_.next_intuitive
    red.if_.next_intuitive.next_intuitive
    red.if_.next_intuitive.next_intuitive.next_intuitive
    red.if_.next_intuitive.next_intuitive.next_intuitive.next_intuitive

.. warning::

    There is a subtlety: :file:`IfelseblockNode` is **unaffected** by this
    behavior: you have to use :file:`next_intuitive` or
    :file:`previous_intuitive` on :file:`IfNode`, :file:`ElifNode` and
    :file:`ElseNode` **inside** IfelseblockNode.

    But, if you do a :file:`next_intuitive` or :file:`previous_intuitive` or a
    node around :file:`IfelseblockNode` it will jump to the first or last node
    **inside** the :file:`IfelseblockNode`.

    See this example

.. ipython:: python

    red = RedBaron("before\nif a:\n    pass\nelif b:\n    pass\nelse:\n    pass\nafter")
    red[1].ifelseblock.next_intuitive  # similar to .next
    red[1].ifelseblock.next.previous  # this is the IfelseblockNode
    red[1].ifelseblock.next.previous_intuitive  # this is the ElseNode
    red[1].ifelseblock.previous.next  # this is the IfelseblockNode
    red[1].ifelseblock.previous.next_intuitive  # this is the IfNode

For :file:`ForNode`:

.. ipython:: python

    red = RedBaron("for a in b:\n    pass\nelse:\n    pass\nafter")
    red
    red[0].help()
    red.for_
    red.for_.next
    red.for_.next_intuitive
    red.for_.next_intuitive.next_intuitive

For :file:`WhileNode`:

.. ipython:: python

    red = RedBaron("while a:\n    pass\nelse:\n    pass\nafter")
    red
    red[0].help()
    red.while_
    red.while_.next
    red.while_.next_intuitive
    red.while_.next_intuitive.next_intuitive

.root
-----

Every node have the :file:`.root` attribute (property) that returns the root
node in which this node is located:

.. ipython:: python

    red = RedBaron("def a(): return 42")
    red.int_
    assert red.int_.root is red

.. _index_on_parent:

.index_on_parent
----------------

Every node have the :file:`.index_on_parent` attribute (property) that returns the index
at which this node is store in its parent node list. If the node isn't stored
in a node list, it returns :file:`None`. If the node is stored in a proxy list
(:doc:`proxy_list`), it's the index in the proxy list that is returned. to get
the unproxified index use :ref:`index_on_parent_raw`.

.. ipython:: python

    red = RedBaron("a = [1, 2, 3]")
    red[0].value.value
    red[0].value.value[2]
    red[0].value.value[2].index_on_parent
    red[0].value
    red[0].value.index_on_parent

.. _index_on_parent_raw:

.index_on_parent_raw
--------------------

Same as :ref:`index_on_parent` except that it always return the unproxified
whether the node is stored in a proxy list or not.

.. ipython:: python

    red = RedBaron("a = [1, 2, 3]")
    red[0].value.value.node_list
    red[0].value.value.node_list[2]
    red[0].value.value.node_list[2].index_on_parent_raw

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
future into a node list proxy or something like that, I just don't have the time
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

.increase_indentation() and .decrease_indentation()
---------------------------------------------------

Those 2 methods allow you to change the indentation of a part of the tree. They
expect the number of spaces to add or to remove as first argument.

.. ipython:: python

    red = RedBaron("def a():\n    if plop:\n        pass")
    red
    red[0].value.increase_indentation(15)
    red
    red[0].value.decrease_indentation(15)
    red

.to_python()
------------

.. WARNING::

   Since RedBaron calls ast.literal_eval it can only parse the python code
   parsed by the python version you are using.

   For example if you are using a python version inferior to 3.6, `to_python`
   will crash on `100_000` because it is only supported since python 3.6

This method safely evaluate the current selected nodes. It wraps
`ast.literal_eval
<https://docs.python.org/2/library/ast.html#ast.literal_eval>`_, therefor, and
for security reasons, it only works on a subset of python: numbers, strings,
lists, dicts, tuples, boolean and :file:`None`. Of course, using this method on
a list/dict/tuple containing values that aren't listed here will raise a
:file:`ValueError`.

.. ipython:: python

    RedBaron("42")[0].value  # string
    RedBaron("42")[0].to_python()  # python int

    RedBaron("'a' 'b'")[0].dumps()
    RedBaron("'a' 'b'")[0].to_python()
    RedBaron("u'unicode string'")[0].to_python()

    RedBaron("[1, 2, 3]")[0].to_python()
    RedBaron("(1, 2, 3)")[0].to_python()
    RedBaron("{'foo': 'bar'}")[0].to_python()

    RedBaron("False")[0].to_python()
    RedBaron("True")[0].to_python()

    print(RedBaron("None")[0].to_python())

.path()
-------

Every node has a :file:`path()` method that will return a :file:`Path` object
to it. Every path object has a :file:`.node` attribute that point to the node
and a :file:`.to_baron_path` that returns a `Baron Path namedtuple
<https://baron.pycqa.org/en/latest/#locate-a-node>`_.

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

RedBaron nodes list have 3 helper methods :file:`.map`, :file:`.filter` and :file:`.apply` quite similar to python builtins (except for apply). The main difference is that they return a node list instance instead of a python buildin list.

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
    red('int').map(lambda x: x.to_python() + 1)
    red('int').filter(lambda x: x.to_python() % 2 == 0)

.. ipython:: python

    red = RedBaron("a()\nb()\nc(x=y)")
    red('call')
    # FIXME
    # red('call').map(lambda x: x.append_value("answer=42"))
    red('call')
    red = RedBaron("a()\nb()\nc(x=y)")
    # FIXME
    # red('call').apply(lambda x: x.append_value("answer=42"))

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
environment variables. If this variable is not present, nano is used. You can
use a different editor this way: :file:`node.edit(editor="vim")`.

.absolute_bounding_box
----------------------

The absolute bounding box of a node represents its top-left and
bottom-right position relative to the fst's root node. The position is
given as a tuple :file:`(line, column)` with **both starting at 1**.

.. ipython:: python

    red = RedBaron("def a(): return 42")
    red.funcdef.value.absolute_bounding_box

You can also get the bounding box of "string" nodes like the left
parenthesis in the example above by giving the attribute's name to the
:file:`get_absolute_bounding_box_of_attribute()` method:

.. ipython:: python

    red.funcdef.get_absolute_bounding_box_of_attribute('(')

This is impossible to do without giving the attribute's name as an
argument since the left parenthesis is not a redbaron Node.

.bounding_box
-------------

Every node has the :file:`bounding_box` property which holds the
top-left and bottom-right position of the node. Compared to the
:file:`absolute_bounding_box` property, it assumes the node is the
root node so the top-left position is always :file:`(1, 1)`.

.. ipython:: python

    red = RedBaron("def a(): return 42")
    red.funcdef.value.absolute_bounding_box
    red.funcdef.value.bounding_box

.find_by_position()
-------------------

You can find which node is located at a given line and column:

.. ipython:: python

    red = RedBaron("def a(): return 42")
    red.find_by_position((1, 5))
    red.find_by_position((1, 6)) # '(' is not a redbaron node

.at()
-------------------

Returns first node at specific line

.. ipython:: python

    red = RedBaron("def a():\n return 42")
    red.at(1) # Gives DefNode
    red.at(2) # Gives ReturnNode

.. _Node.from_fst:

Node.from_fst()
---------------

:file:`Node.from_fst()` is a helper class method that takes an FST node and return a
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

Similarly to :file:`Node.from_fst()`, :file:`NodeList.from_fst()` is a helper
class method that takes an FST node **list** and return a RedBaron node **list**
instance. Similarly, you probably don't need to go so low level.


.. ipython:: python

    from redbaron import NodeList
    NodeList.from_fst([{"type": "name", "value": "a"}, {'first_formatting': [], 'type': 'comma', 'second_formatting': [{'type': 'space', 'value': ' '}]}, {"type": "name", "value": "b"}])

.insert_before .insert_after
----------------------------

One thing you often wants to do is to insert things just after or before the
node you've just got via query. Those helpers are here for that:

.. ipython:: python

    red = RedBaron("foo = 42\nprint('bar')\n")
    red
    red.print_.insert_before("baz")
    red
    red.print_.insert_after("foobar")
    red

Additionally, you can give an optional argument :file:`offset` to insert more
than one line after or before:


.. ipython:: python

    red = RedBaron("foo = 42\nprint('bar')\n")
    red
    red.print_.insert_before("baz", offset=1)
    red
    red[0].insert_after("foobar", offset=1)
    red
