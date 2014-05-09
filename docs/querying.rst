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


