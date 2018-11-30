
class ValueType:
    BOOL = 0
    NIL = 1
    NUMBER = 2


class Value(object):
    """
    Boxing of different primitive values.

    """
    def __init__(self, value, value_type):
        self.value = value
        self.type = value_type

    def debug_repr(self):
        if self.type == ValueType.NUMBER:
            return ("%f" % self.value)[:16]
        elif self.type == ValueType.BOOL:
            return "true" if self.value else "false"
        elif self.type == ValueType.NIL:
            return "nil"
        else:
            return str(self.value)

    def __repr__(self):
        return "<Value: '%s'>" % self.value

    def is_equal(self, other):
        if self.type != other.type:
            return False
        return self.value == other.value

    def is_bool(self):
        return self.type == ValueType.BOOL

    def is_nil(self):
        return self.type == ValueType.NIL

    def is_number(self):
        return self.type == ValueType.NUMBER

    def is_falsey(self):
        if self.is_bool():
            return not self.value
        elif self.is_nil():
            return True
        else:
            return False



class ValueArray(object):
    def __init__(self):
        self.values = []

    def __getitem__(self, item):
        return self.values[item]

    def index(self, item):
        # Return the index of an item in the array
        for i, value in enumerate(self.values):
            if item.value == value.value:
                return i
        raise ValueError("Not found")

    def append(self, value):
        """

        :param value:
        :return: The index of the added constant/value
        """
        self.values.append(value)
        return len(self.values) - 1

