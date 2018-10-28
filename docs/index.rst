Welcome to RedBaron's documentation!
====================================

Introduction
------------

RedBaron is a python library and tool powerful enough to be used into IPython
solely that intent to make the process of **writing code that modify source
code** as easy and as simple as possible. That include writing custom
refactoring, generic refactoring, tools, IDE or directly modifying you source
code into IPython with a higher and more powerful abstraction than the
advanced texts modification tools that you find in advanced text editors and
IDE.

RedBaron guaranteed you that **it will only modify your code where you ask him
to**. To achieve this, it is based on `Baron <https://github.com/PyCQA/baron>`_
a lossless `AST <https://en.wikipedia.org/wiki/Abstract_syntax_tree>`_ for
Python  that guarantees the operation :file:`fst_to_code(code_to_fst(source_code)) == source_code`.

RedBaron API and feel is heavily inspired by BeautifulSoup. It tries to be
simple and intuitive and that once you've get the basics principles, you are
good without reading the doc for 80% of your operations.

A note about the examples
-------------------------

This documentation is full of example for nearly everything. But in fact, those
aren't really "example": those are real life code that are executed at the
compilation time of this documentation, this guaranteed the example you see to
work exactly the same way for you.

Funny side effect: this make it possible to "break" this documentation.

Code
----

https://github.com/PyCQA/redbaron

Installation
------------

::

    pip install redbaron[pygments]

Or if you don't want to have syntax highlight in your shell or don't need it:

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

Simple API: give string, get string back.

.. ipython:: python

    from redbaron import RedBaron

    red = RedBaron("some_value = 42")
    red.dumps()  # get code back

Though to be used in IPython directly:

.. ipython:: python

    red  # direct feedback like BeautifulSoup, "0" here is the index of the node in our source code
    red.help()  # helper function that describe nodes content so you don't have to read the doc


Easy nodes modifications, you already know how to code in python, so pass
python code (in a string) on the attribute you want to modify (wonder what
:file:`.value` is? look at the output of :file:`.help()` in the previous
example):

.. ipython:: python

    red[0].value = "1 + 4"
    red

Easy queries, just like in BeautifulSoup:

.. ipython:: python

    red.find("int", value=4)
    red.find_all("int")  # can also be written red("int") like in BeautifulSoup

Queries can be very powerful, you can test each attributes with value/lambda/regex/special syntax for regex/globs.

Now let's pretend that we are editing a django settings.py (notice that we are
extending our source code using the same API than the one of a python list
since we are in a list of lines):

.. ipython:: python

    red.extend(["\n", "INSTALLED_APPLICATIONS = (\n    'django',\n)"])  # here "\n" is to had a blank line
    red

And let's install another django application! (again: same API than a python list)

.. ipython:: python

    red.find("assignment", target=lambda x: x.dumps() == "INSTALLED_APPLICATIONS").value.append("'another_app'")
    red

Notice that the formatting of the tuple has been detected and respected when
adding the new django application.

And let's see the result of our work:

.. ipython:: python

    print(red.dumps())

Financial support
-----------------

Baron and RedBaron are a very advanced piece of engineering that requires a lot
of time of concentration to work on. Until the end of 2018, the development
has been a full volunteer work mostly done by [Bram](https://github.com/psycojoker),
but now, to reach the next level and bring those projects to the stability and
quality you expect, we need your support.

You can join our contributors and sponsors on our transparent
[OpenCollective](https://opencollective.com/redbaron), every contribution will
count and will be mainly used to work on the projects stability and quality but
also on continuing, on the side, the R&D side of those projects.

Our supporters
~~~~~~~~~~~~~~

.. image:: https://opencollective.com/redbaron/tiers/i-like-this,-keep-going!/badge.svg?label=I like this, keep going!&color=brightgreen
.. image:: https://opencollective.com/redbaron/tiers/it-looks-cool!/badge.svg?label=It looks cool!&color=brightgreen
.. image:: https://opencollective.com/redbaron/tiers/oh-god,-that-saved-me-so-much-time!/badge.svg?label=Oh god, that saved me so much time!&color=brightgreen

\

.. image:: https://opencollective.com/redbaron/tiers/i-like-this,-keep-going!.svg?avatarHeight=36&width=600

Become our first sponsor!

.. image:: https://opencollective.com/redbaron/tiers/long-term-sponsor.svg?avatarHeight=36&width=600

Table of content
----------------

.. TODO add a tutorial

.. toctree::
   :maxdepth: 2

   tuto
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
