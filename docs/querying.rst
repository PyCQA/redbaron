.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

    from redbaron import RedBaron


Querying
========

As you have seen in the previous section, you can navigate into RedBaron tree
only using attribute access and index access on list of nodes with the use of
the :file:`.help()` method to know what you can do. However, RedBaron offers
way more powerful and convenient tools to do that.

.find()
-------

To retrieve a single node, you can use the :file:`.find()` method by passing it
one of the identifiers listed in :file:`.help()` of node you want to get, this way:

.. ipython:: python

    red = RedBaron("a = 1")

    red.help()

    red.find('NameNode').help()
    red.find('namenode').help()  # identifiers are not case sensitive
    red.find('name')

This will recursively travel the tree and return the first node of that type.

You can also specify attributes of the node that you want to match:

.. ipython::

    In [36]: red = RedBaron("a = b")

    In [37]: red.find('name').help()

    In [38]: red.find('name', value='b').help()

If you don't want a recursive approach but only on the first level on the current node or node list, you can pass :file:`recursive=False` to :file:`.find()`.

Like BeautifulSoup, RedBaron provides a shorthand to :file:`.find()`, you can
write the name of the target as an attribute of the node and this will do a :file:`.find()` in the same fashion:

.. ipython::

    In [39]: red = RedBaron("a = b")

    In [40]: red.find('name')

    In [41]: red.name

You might have noticed that some identifiers end with a :file:`_`, those are
for the case where the identifier might be a Python reserved keyword like
:file:`if`, or :file:`while` for example.

Be aware that if you do a :file:`red.something_that_can_be_a_node_identifier`
and this is also not an attribute of a node, this will raise an
:file:`AttributeError`.

.find_all()
-----------

:file:`.find_all()` is extremely similar to :file:`.find()` except it returns a
node list containing all the matching queries instead of a single one. Like in
BeautifulSoup, :file:`__call__` is aliased to :file:`find_all` (meaning that if
you try to *call* the node this way :file:`node(some_arguments)` this will call
:file:`.find_all()` with the arguments).

.. ipython::

    In [45]: red = RedBaron("a = b")

    In [46]: red.find_all("NameNode")

    In [47]: red.find_all("name")

    In [48]: red.findAll("name")

    In [49]: red.findAll("name", value="b")

    In [50]: red("name", value="b")

:file:`.find_all()` also supports the option :file:`recursive=False`.

Advanced querying
-----------------

:file:`.find()` and :file:`.find_all()` offer more powerful comparison mean
than just equality comparison.

Callable (lambda)
~~~~~~~~~~~~~~~~~

Instead of passing a string to test properties of the identifier of a node, you
can pass a callable, like a lambda. It will receive the value as first
argument:

.. ipython:: python

    red = RedBaron("a = [1, 2, 3, 4]")
    red.find("int", value=lambda value: int(value) % 2 == 0)
    red.find_all("int", value=lambda value: int(value) % 2 == 0)
    red.find(lambda identifier: identifier == "comma")
    red.find_all(lambda identifier: identifier == "comma")

Regex
~~~~~

Instead of passing a string to test properties of a node, you can pass a
compiled regex:

.. ipython:: python

    import re
    red = RedBaron("abcd = plop + pouf")
    red.find("name", value=re.compile("^p"))
    red.find_all("name", value=re.compile("^p"))
    red.find(re.compile("^n"))
    red.find_all(re.compile("^n"))

Having to compile regex is boring, so you can use this shorthand syntax
instead (prefixing a string with "re:"):

.. ipython:: python

    red = RedBaron("abcd = plop + pouf")
    red.find("name", value="re:^p")
    red.find_all("name", value="re:^p")
    red.find("re:^n")
    red.find_all("re:^n")

Globs
~~~~~

Same than in a shell, you can use globs by prefixing the string with "g:":

.. ipython:: python

    red = RedBaron("abcd = plop + pouf")
    red.find("name", value="g:p*")
    red.find_all("name", value="g:p*")
    red.find("g:n*")
    red.find_all("g:n*")

In the background, the comparison is done using the `fnmatch
<https://docs.python.org/2/library/fnmatch.html#fnmatch.fnmatch>`_ module of
the standard lib.

List or tuple
~~~~~~~~~~~~~

You can pass a list as a shorthand to test if the tested attribute is in any of
the member of the list/tuple:

.. ipython:: python

    red = RedBaron("foo\nbar\nbaz")
    red.find("name", value=["foo", "baz"])
    red.find("name", value=("foo", "baz"))
    red("name", value=["foo", "baz"])
    red("name", value=("foo", "baz"))

.. ipython:: python

    red = RedBaron("1\nstuff\n'string'\n")
    red.find(["int", "string"])
    red(["int", "string"])

\*args and default value
~~~~~~~~~~~~~~~~~~~~~~~~

You can also pass as many callable as args (without giving it a key) as you
want, those callables will receive the node itself as first argument (and must
return a value that will be tested as a boolable):

.. ipython:: python

    red = RedBaron("a = [1, 2, 3, 4]")
    red.find("int", lambda node: int(node.value) % 2 == 0)
    red.find_all("int", lambda node: int(node.value) % 2 == 0)
    red.find("int", lambda node: int(node.value) % 2 == 0, lambda node: int(node.value) == 4)

To ease the usage of RedBaron in ipython (and in general), you can pass any of
the previous testing methods (**except the lambda**) as the **first** argument of
\*args, it will be tested against the default testing attribute which is the
"value" attribute by default. This mean that: :file:`red.find("name", "foo")`
is the equivalent of :file:`red.find("name", value="foo")`.

If the default tested attribute is different, it will be shown in
:file:`.help()`. For now, the 2 only cases where this happens is on class node
and funcdef node where the attribute is "name".

.. ipython:: python

    red = RedBaron("foo\ndef bar(): pass\nbaz\ndef badger(): pass")
    red.find("name", "baz")
    red.find("def", "bar")
    red.find("def").help()

Next
~~~~

To learn how to modify stuff in RedBaron read :doc:`modifying`.
