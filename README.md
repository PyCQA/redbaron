Introduction
============

[![Build Status](https://travis-ci.org/PyCQA/redbaron.svg?branch=master)](https://travis-ci.org/PyCQA/redbaron) [![Latest Version](https://pypip.in/version/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Supported Python versions](https://pypip.in/py_versions/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Development Status](https://pypip.in/status/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Wheel Status](https://pypip.in/wheel/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Download format](https://pypip.in/format/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![License](https://pypip.in/license/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/)

RedBaron is a python library and tool powerful enough to be used into IPython
solely that intent to make the process of **writing code that modify source
code** as easy and as simple as possible. That include writing custom
refactoring, generic refactoring, tools, IDE or directly modifying you source
code into IPython with an higher and more powerful abstraction than the
advanced texts modification tools that you find in advanced text editors and
IDE.

RedBaron guaranteed you that **it will only modify your code where you ask him
to**. To achieve this, it is based on [Baron](https://github.com/PyCQA/baron)
a lossless [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) for
Python that guarantees the operation <code>ast_to_code(code_to_ast(source_code)) == source_code</code>.
(Baron's AST is called a FST, a Full Syntax Tree).

RedBaron API and feel is heavily inspired by BeautifulSoup. It tries to be
simple and intuitive and that once you've get the basics principles, you are
good without reading the doc for 80% of your operations.

**For now, RedBaron can be considered in alpha, the core is quite stable but it
is not battle tested yet and is still a bit rough.** Feedback and contribution
are very welcome.

The public documented API on the other side is guaranteed to be
retro-compatible and won't break until 2.0 (if breaking is needed at that
point).
There might be the only exception that if you directly call specific nodes
constructors with FST that this API change, but this is not documented and
simply horribly unpracticable, so I'm expecting no one to do that.

**Disclamer**: RedBaron (and baron) is **working** with python3 but it NOT fully parsing it yet.

Installation
============

    pip install redbaron[pygments]

Or if you don't want to have syntax highlight in your shell or don't need it:

    pip install redbaron

Running tests
=============

    pip install pytest
    py.test tests

Community
=========

You can reach us on [irc.freenode.net#baron](https://webchat.freenode.net/?channels=%23baron) or [irc.freenode.net##python-code-quality](https://webchat.freenode.net/?channels=%23%23python-code-quality).

Code of Conduct
===============

As a member of [PyCQA](https://github.com/PyCQA), RedBaron follows its [Code of Conduct](http://meta.pycqa.org/en/latest/code-of-conduct.html).

Links
=====

**RedBaron is fully documented, be sure to check the turorial and documentation**.

* [Tutorial](https://redbaron.readthedocs.io/en/latest/tuto.html)
* [Documentation](https://redbaron.readthedocs.io/en/latest/)
* [Baron](https://github.com/PyCQA/baron)
* IRC chat: [irc.freenode.net#baron](https://webchat.freenode.net/?channels=%23baron)
