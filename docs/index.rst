Welcome to RedBaron's documentation!
====================================

Introduction
------------

RedBaron is a python library and tool powerful enough to be used into IPython
solely that intent to make the process of **writting code that modify source
code** as easy and as simple as possible. That include writing custom
refactoring, generic refactoring, tools, IDE or directly modifying you source
code into IPython with an higher and more powerful abstraction than the
advanced texts modification tools that you find in advanced text editors and
IDE.

RedBaron guaranteed you that **it will only modify your code where you ask him
to**. To achieve this, it is based on `Baron <https://github.com/Psycojoker/baron>`_
a lossless `AST <https://en.wikipedia.org/wiki/Abstract_syntax_tree>`_ for
Python  that guarantees the operation :file:`fst_to_code(code_to_fst(source_code)) == source_code`.

RedBaron API and feel is heavily inspired by BeautifulSoup. It tries to be
simple and intuitive and that once you've get the basics principles, you are
good without reading the doc for 80% of your operations.

Code
----

https://github.com/Psycojoker/redbaron

Installation
------------

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

.. TODO meh, example is bad, change it

.. ipython:: python

    from redbaron import RedBaron

    red = RedBaron("print 'hello world!'")
    red[0].value[0].value = "'hello from Baron!'"

    red.string.value = "'hello from Baron!'"  # alternatively, BeautifulSoup-style

    red.dumps()  # gives you the modified source code

Table of content
----------------

.. TODO add a tutorial

.. toctree::
   :maxdepth: 2

   why
   basics
   querying
   modifying
   proxy_list
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

