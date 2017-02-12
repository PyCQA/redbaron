Why is this important?
======================

The usage of an FST might not be obvious at first sight so let's consider a
series of problems to illustrate it. Let's say that you want to write a program that will:

* rename a variable in a source file... without clashing with things that are not a variable (example: stuff inside a string)
* inline a function/method
* extract a function/method from a series of line of code
* split a class into several classes
* split a file into several modules
* convert your whole code base from one ORM to another
* do custom refactoring operation not implemented by IDE/rope
* implement the class browser of smalltalk for python (the whole one where you can edit the code of the methods, not just showing code)

It is very likely that you will end up with the awkward feeling of writing
clumsy weak code that is very likely to break because you didn't thought about
all the annoying special cases and the formatting keeps bothering you. You may
end up playing with `ast.py <http://docs.python.org/2/library/ast.html>`_ until
you realize that it removes too much information to be suitable for those
situations. You will probably ditch this task as simple too complicated and
really not worth the effort. You are missing a good abstraction that will take
care of all of the code structure and formatting for you so you can concentrate
on your task.

The FST tries to be this abstraction. With it you can now work on a tree which
represents your code with its formatting. Moreover, since it is the exact
representation of your code, modifying it and converting it back to a string
will give you back your code only modified where you have modified the tree.

Said in another way, what I'm trying to achieve with Baron is a paradigm change in
which writing code that will modify code is now a realistic task that is worth
the price (I'm not saying a simple task, but a realistic task, it's still a
complex task).

Other usages
------------

Having an FST (or at least a good abstraction build on it) also makes it easier
to do code generation and code analysis while those two operations are already
quite feasible (using `ast.py <http://docs.python.org/2/library/ast.html>`_ and 
a templating engine for example).

Next
~~~~

To start playing with RedBaron read :doc:`basics`.
