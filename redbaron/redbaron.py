import baron
from UserList import UserList


class RedBaron(UserList):
    def __init__(self, source_code):
        self.data = baron.parse(source_code)
