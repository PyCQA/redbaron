import sys
from baron.utils import python_version, string_instance


if python_version == 3:
    from collections import UserList
else:
    from UserList import UserList
