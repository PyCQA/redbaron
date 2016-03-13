# Todo

### Important

- .help() seems really slow on big piece of code (for example RedBaron("baron/grammator.py").read())("dict")[0].help() is suuuuuuuuuuuuuuuuper slow)
- raise AttributeError on node.attribute if attribute not in available nodes names
- .at() return the first item starting at line X
- .rename() (name -> value, def/class -> name)
- .replace() expect a whole valid python program. This could be fixed by look at "on_attribute" and resetting itself like that.

- generate default constructors for nodes using nodes_rendering_order
- if possible try to keep a coherent signature with possibles attributes, set correctly default attributes
- examples:
    * SpaceNode(" ")
    * CommaNode()
    * CommaNode(first_formatting=[" "]) # allow to pass strings again

- auto merging behavior for Atomtrailer: "a.b.c".value[0].replace("x.y.z") should not include one Atomtrailer in the current one but flatten both. Same for getitem.

do a check on every setitem, some doesn't works as expected and I'm expected
that none works as expected, for eg, this one fails:
    RedBaron("a(b, c=d, *e, **f)")[0].value[1].value[0] = "**dsq"

in addition of passing empty string, allow to pass None value on setattr
this needs to be done in "_convert_input_to_node_object" and it's possible
now since we have string type in nodes_rendering_order

### More intuitive .next/.previous attribute behavior

while_node.next should check for the while_node.else attribute
same for every other construction with an else: for/except/etc...
the else attribute should check for parent for next
if/elif same
how ifelseblock should behave?
trynode should also have a special behavior
document all of this!
same for .previous!

### Find/Find\_All (comparison)

Magic stuff like:
value\_\_dumps that compare the .dumps() with a string? or use lambda for that instead?

### More general stuff

* .assign, .map\_concat
* .swap, .move on a NodeList
* .cut (like .copy but with del self)
* .remove on nodelist
* method to change style of formatting in a datastructure
* .grep method that test on successive .dumps()
* auto add quotes for strings

### More refactoring like

- find\_name\_binding -> search assign, def (args && name), class, except, with, for ...
- find\_identifier -> search name + everything up there ^

### Wrappers

It should be easy to wrap statement, expressions or various structure in other
statements, like a statement with a block or an associative parenthesis or
those kind of things.

### Magic convertion on setattr

Comment: I'm not that much sure that I'll do those one, .replace already quite handle this job.

conversion from list/set/dict to comprehension version
conversion between binary_operator/boolean_operator/comparison
conversion from if/elif/else to if/elif/else (careful about the ifelseblock)
conversion from call_argument/def_argument to list_argument or dict_argument and vice versa
conversion from string chain to string
