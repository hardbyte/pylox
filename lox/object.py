from rpython.rlib.buffer import StringBuffer


class ObjType:
     STRING = 0



class Obj(object):
    """
    Base class of different dynamically allocated instances.

    """
    def __init__(self, value_type):
        self.type = value_type

    def repr(self):
        return "UNREPRESENTABLE INSTANCE"

    def is_equal(self, other):
        return False


class ObjString(Obj):

    def __init__(self, value):
        self.type = ObjType.STRING
        self.buffer = StringBuffer(value)
        self.length = len(value)

    def repr(self):
        return self.buffer.value

    def is_equal(self, other):
        if self.type != other.type:
            return False
        return self.buffer.value == other.buffer.value

