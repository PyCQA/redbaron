.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

    from redbaron import RedBaron


Proxy List
==========

Problem
-------

For a python developer, the list :file:`[1, 2, 3]` has 3 members, which
is true in the python world, but in the "source code modification"
world, this list has 5 elements because you have to count the 2 commas.
Indeed each comma needs to be taken into account separately because they
can have a different formatting.

This makes things quite annoying to deal with because you have to think
about the formatting too! For example, if you want to append an item to
a list, you need to take care of a lot of details:

* if the list is empty you don't have to put a comma
* otherwise yes
* but wait, what happens if there is a trailing comma?
* also, what to do if the list is declared in an indented way (with :file:`"\\n    "` after every comma for example)?
* etc...

And that's only for a comma separated list of things: you also have the
same formatting details to care about for dot separated lists
(e.g. :file:`a.b.c().d[plop]`) and endl separated lists (a python code block,
or you whole source file).

You don't want to have to deal with this.

Solution
--------

To avoid you to deal with all this boring low level details, RedBaron
implements "proxy lists". This abstraction gives you the impression that the
list of things you are dealing with behave the same way than in the python
world while taking care of all the low level formatting details.

The "proxy lists" has the same API than a python list so they should be
really intuitive to use.

For example:

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red[0].value.append("42")
    red
    del red[0].value[2]
    red

There are, for now, 4 kind of proxy lists:

* :file:`CommaProxyList` which handles comma separated lists
* :file:`DotProxyList` which handles :file:`atomtrailers` (those kind of constructions: :file:`a.b[plop].c()`)
* :file:`LineProxyList` which handles lines of code (like the body of a function or the
  whole source code)
* :file:`DecoratorLineProxyList` which handles lists of decorators (they are nearly the
  same as :file:`LineProxyList`)

**Be aware that the proxy list are set on the attribute that is a list, not
on the node holding the list. See the 'value' attribute access in the
examples below.**

Usage
-----

As said, proxy lists have the exact same API than python lists (at the exception
that they don't implement the :file:`sort` and :file:`reverse` methods).
Every method accepts as input the same inputs that you can use to modify a node
in RedBaron. This means that you can pass a string containing source code,
an FST or a RedBaron node.

Here is a session demonstrating every method of a proxy list:

.. ipython:: python

    red = RedBaron("[1, 2, 3]")

Please refer to `python list documentation
<https://docs.python.org/2/tutorial/datastructures.html>`_ if you want to
know the exact behavior or those methods (or `send a patch
<https://github.com/PyCQA/redbaron>`_ to improve this documentation).

append
~~~~~~

.. ipython:: python

    red
    red[0].value.append("plop")
    red
    red[0].value

insert
~~~~~~

.. ipython:: python

    red
    red[0].value.insert(1, "42")
    red
    red[0].value

extend
~~~~~~

.. ipython:: python

    red
    red[0].value.extend(["pif", "paf", "pouf"])
    red
    red[0].value

pop
~~~

.. ipython:: python

    red
    red[0].value.pop()
    red
    red[0].value
    red[0].value.pop(3)
    red
    red[0].value

__getitem__
~~~~~~~~~~~

.. ipython:: python

    red
    red[0].value
    red[0].value[2]

__setitem__
~~~~~~~~~~~

.. ipython:: python

    red
    red[0].value[2] = "1 + 1"
    red
    red[0].value

remove
~~~~~~

.. ipython:: python

    red
    red[0].value.remove(red[0].value[2])
    red
    red[0].value

index
~~~~~

.. ipython:: python

    red
    red[0].value
    red[0].value.index(red[0].value[2])

count
~~~~~

.. ipython:: python

    red
    red[0].value
    red[0].value.count(red[0].value[2])

len
~~~

.. ipython:: python

    red
    red[0].value
    len(red[0].value)

__delitem__
~~~~~~~~~~~

.. ipython:: python

    red
    del red[0].value[2]
    red
    red[0].value

in
~~

.. ipython:: python

    red
    red[0].value[2] in red[0].value

__iter__
~~~~~~~~

.. ipython:: python

    red
    for i in red[0].value:
        print(i.dumps())

__getslice__
~~~~~~~~~~~~

.. ipython:: python

    red
    red[0].value
    red[0].value[2:4]

__setslice__
~~~~~~~~~~~~

.. ipython:: python

    red
    red[0].value[2:4] = ["1 + 1", "a", "b", "c"]
    red
    red[0].value

__delslice__
~~~~~~~~~~~~

.. ipython:: python

    red
    red[0].value[2:5]
    del red[0].value[2:5]
    red
    red[0].value

Access the unproxified node list
--------------------------------

The unproxified node list is stored under the attribute :file:`node_list` of
the proxy list. **Be aware that, for now, the proxy won't detect if you
directly modify the unproxified node list, this will cause bugs if you modify
the unproxified list then use the proxy list directly**. So, for now, only use
one or the other.

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red[0].value.node_list
    red[0].value

Omitting ".value"
-----------------

For convenience, and because this is a super common typo error, if a node has a
proxy list on its :file:`.value` attribute, you can omit to access it and the
method access will be automatically redirect to it.

This means that the 2 next lines are equivalent:

.. ipython:: python

    red[0]
    red[0].value.append("plop")
    red[0].append("plop")

CommaProxyList
--------------

CommaProxyList is the most generic and most obvious proxy list, all the examples
above are made using it.

It is used everywhere where values are separated by commas.

DotProxyList
------------

DotProxyList is nearly as generic as the CommaProxyList. The specific case of a
DotProxyList is that it is intelligent enough to not add a "." before a "call"
(:file:`(a, b=c, *d, **e)`) or a "getitem" (:file:`[foobar]`).

.. ipython:: python

    red = RedBaron("a.b(c).d[e]")
    red[0].value
    red[0].extend(["[stuff]", "f", "(g, h)"])
    red[0]
    red[0].value

It is used everywhere where values are separated by ".".

You can see a complete example with a DotProxyList, like for the CommaProxyList,
here: :doc:`dotproxylist`.

LineProxyList
-------------

LineProxyList is used to handle lines of code, it takes care to place the
correct endl node between and to set the correct indentation and not to break
the indentation of the next block (if there is one).

One particularity of LineProxyList is that it shows you explicitly the empty
line (while other proxy lists never show you formatting). This is done because
you'll often want to be able to manage those blank lines because you want to
put some space in your code or separate group of lines.

.. ipython:: python

    red = RedBaron("while 42:\n    stuff\n    other_stuff\n\n    there_is_an_empty_line_before_me")
    red
    red[0].value
    red[0].append("plouf")
    red
    red[0].value

You can see a complete example with a LineProxyList, like for the CommaProxyList,
here: :doc:`lineproxylist`.

DecoratorLineProxyList
----------------------

A DecoratorLineProxyList is exactly the same as a LineProxyList except it has
a small modification to indent decorators correctly. Just think of it as
a simple LineProxyList and everything will be fine.

*Don't forget to add the :file:`@` when you add a new decorator (omitting it
will raise an exception)*.

Example:

.. ipython:: python

    red = RedBaron("@plop\ndef stuff():\n    pass\n")
    red
    red[0].decorators.append("@plouf")
    red[0].decorators
    red

Next
~~~~

To learn about various helpers and features in RedBaron, read :doc:`other`.
Be sure to check the :file:`.replace()` method on that page as it can be very useful.
