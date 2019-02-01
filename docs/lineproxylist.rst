.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False

    from redbaron import RedBaron

LineProxyList usage examples
============================

.. ipython:: python

    red = RedBaron("def a():\n    pif\n\n    paf\n    pouf\n")

Please refer to `python list documentation
<https://docs.python.org/2/tutorial/datastructures.html>`_ if you want to
know the exact behavior or those methods (or `send a patch
<https://github.com/PyCQA/redbaron>`_ to improve this documentation).

append
~~~~~~

.. ipython:: python

    red
    red[0].value.append("")
    red[0].value.append("stuff")
    red
    red[0].value

Appending an empty string or a string containing a \n adds a new line.

insert
~~~~~~

.. ipython:: python

    red
    red[0].value.insert(1, "\n")
    red[0].value.insert(1, "print(caribou)")
    red
    red[0].value

Inserting an empty string or a string containing a \n adds a new line.

extend
~~~~~~

.. ipython:: python

    red
    red[0].value.extend(["a", "\n", "if a:\n    pass", "stuff"])
    red
    red[0].value

Extending with an empty string or a string containing a \n adds a new line.

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
    red[0].value[2] = "plop"
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
    red[0].value[2:4] = ["a", "b", "c"]
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
