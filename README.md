Introduction
============

[![Build Status](https://travis-ci.org/PyCQA/redbaron.svg?branch=master)](https://travis-ci.org/PyCQA/redbaron) [![Latest Version](https://img.shields.io/pypi/v/redbaron.svg)](https://pypi.python.org/pypi/redbaron/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/redbaron.svg)](https://pypi.python.org/pypi/redbaron/) [![Development Status](https://img.shields.io/pypi/status/redbaron.svg)](https://pypi.python.org/pypi/redbaron/) [![Wheel Status](https://img.shields.io/pypi/wheel/redbaron.svg)](https://pypi.python.org/pypi/redbaron/) [![Download format](https://img.shields.io/pypi/format/redbaron.svg)](https://pypi.python.org/pypi/redbaron/) [![License](https://img.shields.io/pypi/l/redbaron.svg)](https://pypi.python.org/pypi/redbaron/)
[![Backers on Open Collective](https://opencollective.com/redbaron/backers/badge.svg)](#backers) 
[![Sponsors on Open Collective](https://opencollective.com/redbaron/sponsors/badge.svg)](#sponsors) 

RedBaron is a python library and tool powerful enough to be used into IPython
solely that intent to make the process of **writing code that modify source
code** as easy and as simple as possible. That include writing custom
refactoring, generic refactoring, tools, IDE or directly modifying you source
code into IPython with a higher and more powerful abstraction than the
advanced texts modification tools that you find in advanced text editors and
IDE.

RedBaron guaranteed you that **it will only modify your code where you ask him
to**. To achieve this, it is based on [Baron](https://github.com/PyCQA/baron)
a lossless [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) for
Python that guarantees the operation <code>ast_to_code(code_to_ast(source_code)) == source_code</code>.
(Baron's AST is called an FST, a Full Syntax Tree).

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

Support
=======

RedBaron is support python python 2 and up to python 3.7 grammar.

Roadmap
=======

Current roadmap is as boring as needed:

* bug fixes
* new small features (walker pattern, maybe code generation) and performance improvement.

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

Financial support
=================

Baron and RedBaron are a very advanced piece of engineering that requires a lot
of time of concentration to work on. Until the end of 2018, the development
has been a full volunteer work mostly done by [Bram](https://github.com/psycojoker),
but now, to reach the next level and bring those projects to the stability and
quality you expect, we need your support.

You can join our contributors and sponsors on our transparent
[OpenCollective](https://opencollective.com/redbaron), every contribution will
count and will be mainly used to work on the projects stability and quality but
also on continuing, on the side, the R&D side of those projects.


## Backers

Thank you to all our backers! 🙏 [[Become a backer](https://opencollective.com/redbaron#backer)]

<a href="https://opencollective.com/redbaron#backers" target="_blank"><img src="https://opencollective.com/redbaron/backers.svg?width=890"></a>


## Sponsors

Support this project by becoming a sponsor. Your logo will show up here with a link to your website. [[Become a sponsor](https://opencollective.com/redbaron#sponsor)]

<a href="https://opencollective.com/redbaron/sponsor/0/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/redbaron/sponsor/1/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/1/avatar.svg"></a>
<a href="https://opencollective.com/redbaron/sponsor/2/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/2/avatar.svg"></a>
<a href="https://opencollective.com/redbaron/sponsor/3/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/3/avatar.svg"></a>
<a href="https://opencollective.com/redbaron/sponsor/4/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/4/avatar.svg"></a>
<a href="https://opencollective.com/redbaron/sponsor/5/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/5/avatar.svg"></a>
<a href="https://opencollective.com/redbaron/sponsor/6/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/6/avatar.svg"></a>
<a href="https://opencollective.com/redbaron/sponsor/7/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/7/avatar.svg"></a>
<a href="https://opencollective.com/redbaron/sponsor/8/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/8/avatar.svg"></a>
<a href="https://opencollective.com/redbaron/sponsor/9/website" target="_blank"><img src="https://opencollective.com/redbaron/sponsor/9/avatar.svg"></a>

## Contributors

This project exists thanks to all the people who contribute. 
<a href="https://github.com/PyCQA/redbaron/contributors"><img src="https://opencollective.com/redbaron/contributors.svg?width=890&button=false" /></a>

Code of Conduct
===============

As a member of [PyCQA](https://github.com/PyCQA), RedBaron follows its [Code of Conduct](http://meta.pycqa.org/en/latest/code-of-conduct.html).

Links
=====

**RedBaron is fully documented, be sure to check the tutorial and documentation**.

* [Tutorial](https://redbaron.readthedocs.io/en/latest/tuto.html)
* [Documentation](https://redbaron.readthedocs.io/en/latest/)
* [Baron](https://github.com/PyCQA/baron)
* IRC chat: [irc.freenode.net#baron](https://webchat.freenode.net/?channels=%23baron)
