Introduction
============

[![Build Status](https://travis-ci.org/Psycojoker/redbaron.svg?branch=master)](https://travis-ci.org/Psycojoker/redbaron) [![Latest Version](https://pypip.in/version/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Supported Python versions](https://pypip.in/py_versions/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Development Status](https://pypip.in/status/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Wheel Status](https://pypip.in/wheel/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![Download format](https://pypip.in/format/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/) [![License](https://pypip.in/license/redbaron/badge.svg)](https://pypi.python.org/pypi/redbaron/)

RedBaron is a query library for the [Baron](https://github.com/Psycojoker/baron) Full Syntax Tree (FST). But what is
Baron? Baron is a syntax tree, like an
[AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) for the Python
language that hold the following rule:
<code>syntax_tree_to_code(code_to_syntax_tree(code)) == code</code>. The
Baron FST is in form of JSON-serializable Python (list and dict) which is very
low level and not extremely funny to work with (a bit like bytecode), RedBaron
is an abstraction on top of that to ease the exploration and
modification of this FST.

Ok, but why this can be useful? The (hard) bet made by Baron is to induce a
paradigm change in which writing code that explore or modify code (like
(custom) refactoring code, refactoring browser, tooling, autoformatting…)
is now a realistic task for most of the developers. Having a FST for Python
means that the task of modifying source code just shift from parsing then
modifying a string to modifying a meaningful tree. For a longer explanation
[read this](https://redbaron.readthedocs.org/en/latest/why.html).

**For now, RedBaron is in its early stages of development, it is quite stable
but it is probably not the most shiny experience yet.** Feedback is very welcome.

Installation
============

    pip install redbaron

Links
=====

* [Documentation](https://redbaron.readthedocs.org)
* [Baron](https://github.com/Psycojoker/baron)
* IRC chat: [irc.freenode.net#baron](https://webchat.freenode.net/?channels=%23baron)
