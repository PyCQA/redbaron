Welcome to RedBaron's documentation!
====================================

Introduction
------------

RedBaron is an abstraction on top of `Baron <https://github.com/Psycojoker/baron>`_ to make it easy to use. It is
heavily inspired by BeautifulSoup.

Baron is a Full Syntax Tree (FST) library for Python. By opposition to an AST
which drops some syntax information in the process of its creation (like empty
lines, comments, formatting), a FST keeps everything and guarantees the
operation :file:`fst_to_code(code_to_fst(source_code)) == source_code`.

Code
----

https://github.com/Psycojoker/redbaron

Installation
------------

Not released on pypi yet.

::

    pip install redbaron

Basic usage
-----------

.. ipython:: python
    :suppress:

    import sys
    sys.path.append("..")

    import redbaron
    redbaron.ipython_behavior = False


.. ipython:: python

    from redbaron import RedBaron

    red = RedBaron("print 'hello world!'")
    red[0].value[0].value = "'hello from Baron!'"

    red.string.value = "'hello from Baron!'"  # alternatively, BeautifulSoup-style

    red.dumps()  # gives you the modified source code

Table of content
----------------

.. toctree::
   :maxdepth: 2

   why
   basics
   querying
   modifying
   modifying_helpers
   other

Reference
---------

.. toctree::
   :maxdepth: 2

   nodes_reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

