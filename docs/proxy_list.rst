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

For a python developer, this list: :file:`[1, 2, 3]` has 3 members, which is
true in the python world, but in the "source code modification" world, this
list has 5 elements because you have to count the 2 commas.

This makes things quite annoying to deal with because you have to think about
this formatting detail to. For example: you want to append an item to a list:

* if the list is empty you don't have to put a comma
* otherwise yes
* but wait, what happens if there is a trailing comma?
* also, what to do if the list is declared in an indented way (with "\n    " after every comma for example)?
* etc...

And I'm only talking about comma separated list of things: you also have the
same things for dot separated things (:file:`a.b.c().d[plop]`) and endl
separated lists (a python code block, or you whole source file).

You don't want to have to deal with this.

Solution
--------

To avoid you to deal with all this boring low level details things, RedBaron
implements "proxy lists", an abstraction that gives you the impression that the
list of things you are dealing with behave the same way than in the python
world while taking care of all the low level formatting details.

The "proxy lists" have the same API than the python lists so they should be
really intuitive to use for you.

For example:

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red[0].value.append("42")
    red
    del red[0].value[2]
    red

There are, for now, 4 kind of proxy lists:

* :file:`CommaProxyList` which handles things separated by comma
* :file:`DotProxyList` which handles :file:`atomtrailers` (those kind of constructions: :file:`a.b[plop].c()`)
* :file:`LineProxyList` which handles lines of code (like the body of a function or you
  whole source code file)
* :file:`DecoratorLineProxyList` which handles list of decorators (they are nearly the
  same than :file:`LineProxyList`)

**Be aware that the proxy list are setted on the attribute that is a list, not
on the node holding the list, see the 'value' attribute access in the
example**.

Usage
-----

As said, proxy lists have the exact same API than python list (at the execption
that they don't implement the :file:`sort` and the :file:`reverse` method).
Every method accept as input the same inputs that you can use to modify a node
in ReadBaron. This means that you can pass: a string containing source code,
FST or RedBaron node.

Here is a session demonstrating every method of a proxy list:

.. ipython:: python

    red = RedBaron("[1, 2, 3]")

Please refer to `python list documentation
<https://docs.python.org/2/tutorial/datastructures.html>`_ a if you want to
know the exact behavior or those methods (or `send a patch
<https://github.com/Psycojoker/redbaron>`_ to improve this documentation).

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
        print i.dumps()

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
or the other.

.. ipython:: python

    red = RedBaron("[1, 2, 3]")
    red[0].value.node_list
    red[0].value
