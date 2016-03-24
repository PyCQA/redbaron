from __future__ import absolute_import

import os
import re
import sys

from baron.utils import python_version

import redbaron


if python_version == 3:
    from io import StringIO
else:
    from StringIO import StringIO



def baron_type_to_redbaron_classname(baron_type):
    return "".join(map(lambda x: x.capitalize(), baron_type.split("_"))) + "Node"


def redbaron_classname_to_baron_type(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name.replace("Node", ""))
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def log(string, *args):
    if redbaron.DEBUG:
        sys.stdout.write("%s\n" % (string % args))


def in_a_shell():
    # the isinstance here is for building sphinx doc
    if redbaron.DEBUG or isinstance(sys.stdout, StringIO):
        return True
    try:
        if hasattr(sys.stdout, 'fileno') and os.isatty(sys.stdout.fileno()):
            return True
    except Exception:
        # someone is doing strange things with stdout (eg: bpython or ipython notebook)
        return False

    return False


def indent(block_of_text, indentation):
    """
    Helper function to indent a block of text.

    Take a block of text, an indentation string and return the indented block.
    """
    return "\n".join(map(lambda x: indentation + x, block_of_text.split("\n")))


def truncate(text, n):
    if n < 5 or len(text) <= n:
        return text

    truncated = list(text)
    truncated[-3:-1] = ['.', '.', '.']
    del truncated[n-4 : -4]
    return "".join(truncated)
