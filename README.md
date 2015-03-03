Introduction
============

[![Build Status](https://travis-ci.org/Psycojoker/redbaron.svg?branch=master)](https://travis-ci.org/Psycojoker/redbaron) [![Latest Version](https://pypip.in/version/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Supported Python versions](https://pypip.in/py_versions/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Development Status](https://pypip.in/status/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Wheel Status](https://pypip.in/wheel/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Download format](https://pypip.in/format/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![License](https://pypip.in/license/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/)

RedBaron is a python library and tool powerful enough to be used into IPython
solely that intent to make the process of **writting code that modify source
code** as easy and as simple as possible. That include writing custom
refactoring, generic refactoring, tools, IDE or directly modifying you source
code into IPython with an higher and more powerful abstraction than the
advanced texts modification tools that you find in advanced text editors and
IDE.

RedBaron guaranteed you that **it will only modify your code where you ask him
to**. To achieve this, it is based on [Baron](https://github.com/Psycojoker/baron)
a lossless [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) for
Python that guarantees the operation <code>ast_to_code(code_to_ast(source_code)) == source_code</code>.
(Baron's AST is called a FST, a Full Syntax Tree).

RedBaron API and feel is heavily inspired by BeautifulSoup. It tries to be
simple and intuitive and that once you've get the basics principles, you are
good without reading the doc for 80% of your operations.

**For now, RedBaron can be considered in alpha, the core is quite stable but it
is not battle tested yet and is still a bit rough.** Feedback is very welcome.

**Disclamer**: RedBaron (and baron) is **working** with python3 but it NOT fully parsing it yet.

Installation
============

    pip install redbaron

Running tests
=============

    pip install pytest
    py.test tests

Links
=====

**RedBaron is fully documented, be sure to check the turorial and documentation**.

* [Tutorial](https://redbaron.readthedocs.org/en/latest/tuto.html)
* [Documentation](https://redbaron.readthedocs.org)
* [Baron](https://github.com/Psycojoker/baron)
* IRC chat: [irc.freenode.net#baron](https://webchat.freenode.net/?channels=%23baron)
