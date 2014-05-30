Modifying helpers
=================

In an attempt to overcome some of the limitations describe at the end of the
previous section and in an attempt to make RedBaron mor please to use, a series
of helpers method are provided.

An example on how you can do that by hand without the helper is provided
everytime to teach you the general underlying of (Red)Baron. Expect this to be
quite low level.

.. _to_node:

to_node()
---------

:file:`to_node()` is an helper function that takes a FST node and return a
RedBaron node instance. Except if you need to go down at a low level or that
RedBaron doesn't provide the helper you need, you shouldn't use it.

.. ipython:: python

    from redbaron import to_node
    to_node({"type": "name", "value": "a"})

:file:`to_node()` takes 2 optional keywords arguments: :file:`parent` and
:file:`on_attribute` that should respectively be RedBaron node instance (the
parent node) and a string (the attribute of the parent node on which this node
is stored). See :ref:`parent` doc for a better understanding of those 2
parameters.

.. ipython:: python

    red = RedBaron("[1,]")
    new_name = to_node({"type": "name", "value": "a"}, parent=red[0], on_attribute="value")
    red[0].value.append(new_name)

.append_value()
---------------

This method allows you to append an element to the :file:`value` attribute of a
node if this is a node liste while taking care of inserting the correct
separator (if needed) for you. For example: appending a new statement to a
function body.

The way it choose the separator is simple: take the last one if the list if
it's present, otherwise, use a default one (4 spaces indentations if the
separator is an endl node).

Like every other method of RedBaron you can pass it either a string, a fst item
of a RedBaron instance.

This method is provided for:

* ListNode (put a comma)
* SetNode (put a comma)
* TupleNode (put a comma and a leading trailing comma if there is only one item)
* DictNode (put a comma) **Warning: except a key and a value parameter**
* CallNode (put a comma)
* FuncdefNode (put an endl)
* ForNode (put an endl)
* WhileNode (put an endl)
* ClassNode (put an endl)
* WithNode (put an endl)
* IfNode (put an endl)
* ElifNode (put an endl)
* ElseNode (put an endl)
* TryNode (put an endl)
* FinallyNode (put an endl)
* ExceptNode (put an endl)

.. ipython::

    In [105]: red = RedBaron("[1, 2, 3]"); red[0].append_value("42"); red

    In [105]: red = RedBaron("{1, 2, 3}"); red[0].append_value("42"); red

    In [105]: red = RedBaron("(1, 2, 3)"); red[0].append_value("42"); red

    In [105]: red = RedBaron("()"); red[0].append_value("42"); red

    In [105]: red = RedBaron('{"a": 1, "b": 2, "c": 3}'); red[0].append_value(key='"d"', value="4"); red

    In [105]: red = RedBaron("some_function(42)"); red[0].value[1].append_value("a=b"); red

    In [105]: red = RedBaron("def function(): pass"); red[0].append_value("print 'Hello World!'"); red

    In [105]: red = RedBaron("for i in b:\n    print i"); red[0].append_value("stuff(i)"); red

    In [105]: red = RedBaron("while i < 100:\n                       print i"); red[0].append_value("i += 1"); red

    In [105]: red = RedBaron("class Cats: pass"); red[0].append_value("fluffy = True"); red

    In [105]: red = RedBaron("with a: pass"); red[0].append_value("I_dont_have_any_inspiration"); red

    In [105]: red = RedBaron("if True: stuff()"); red[0].if_.append_value("print 'It\\'s True!'"); red


By hand
~~~~~~~

Not really a very funny thing to do. You have 2 strategies: add nodes by
writting FST and using :ref`to_node` (but I don't expect anyone to really have
to remember the FST from head) by hand or using :file:`.copy()` if nodes
already exist (please note that I'm not going to cover all the cases possible
you can encounter, :file:`.append_value()` does that, you can read its code if
you want to).

.. note::

    Remember that you can use :file:`.fst()` on any node to have an idea of the
    corresponding fst.

.. warning::

    You have to explicitly set :file:`.parent` and :file:`on_attribute` by hand

With FST:

.. ipython:: python

    red = RedBaron("[1, 2, 3]")

    list_node_value = red[0]
    comma = to_node({"type": "comma", "first_formatting": [], "second_formatting": [{"type": "space", "value": " "}]}, parent=list_node_value, on_attribute="value")
    new_name = to_node({"type": "name", "value": "a"}, parent=list_node_value, on_attribute="value")
    list_node_value.value.append(comma)
    list_node_value.value.append(new_name)
    list_node_value
    list_node_value.value

With :file:`.copy()`:

.. ipython:: python

    red = RedBaron("[1, 2, 3]")

    list_node_value = red[0]
    comma = red[0].value[-2].copy()
    comma.parent = list_node_value
    comma.on_attribute = "value"
    new_int = red[0].value[-1].copy()
    new_int.value = "42"
    new_int.parent = list_node_value
    new_int.on_attribute = "value"
    list_node_value.value.append(comma)
    list_node_value.value.append(new_int)
    list_node_value
    list_node_value.value

Next
~~~~

To learn some other misc details of RedBaron read :doc:`other`.
