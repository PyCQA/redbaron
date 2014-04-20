Introduction
============

RedBaron is query library for the Baron Full Syntax Tree (FST). But what is
Baron? Baron is a syntax tree, like an
[AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) for the python
language that hold the following rule:
<code>syntaxe_tree_to_code(code_to_syntaxe_tree(code)) == code</code>. The
Baron FST is in form of JSON-serializable python (list and dict) which is very
low level and not extremely funny to work with (a bit like bytecode), RedBaron
is an abstraction on top of top of that to ease the exploration and
modification of this FST.

Ok, but why this can be useful? The (hard) bet made by Baron is to induce a
paradigm change in which writing code that explore or modify code (like
(custom) refactoring code, refactoring browser, tooling, autoformating etc...)
is now a realistic task for most of the developers. Having a FST for python
means that the task of modifying source code just shift from parsing then
modifying a string to modifying a meaningful tree. For a longer explanation
[read this](https://redbaron.readthedocs.org/en/latest/why.html).

**For now, RedBaron is in its early stages of developpement, it is quite stable
but it is probably not the most shiny experience yet.**

Installation
============

    pip install git+https://github.com/Psycojoker/redbaron.git

Links
=====

* [Documentation](https://redbaron.readthedocs.org)
* [Baron](https://github.com/Psycojoker/baron)
