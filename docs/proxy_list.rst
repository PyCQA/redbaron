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
