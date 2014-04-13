"""
Recursivly traverse a python script to test if .indentation seems to be working everywhere
"""

from redbaron import RedBaron

red = RedBaron(open("../redbaron.py", "r").read())
# red = RedBaron(open(__file__, "r").read())

def walk(node):
    if node is None:
        return
    print [node.indentation, node]
    for i in node._dict_keys:
        walk(getattr(node, i))

    for i in node._list_keys:
        map(walk, getattr(node, i))

map(walk, red)
# print walk(red[0])
