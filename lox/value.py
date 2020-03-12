from lox.object import Obj, ObjType


class ValueType:
    BOOL = 0
    NIL = 1
    NUMBER = 2
    OBJ = 3


class Value(object):
    """
    Boxing of different primitive values.
    See object.py for dynamic objects such as strings.
    """

    def __init__(self, value, value_type):
        if value_type == ValueType.BOOL:
            PrimitiveBoolValue.__init__(self, value)
        elif value_type == ValueType.NIL:
            PrimitiveNilValue.__init__(self)
        elif value_type == ValueType.NUMBER:
            PrimitiveNumberValue.__init__(self, value)
        elif value_type == ValueType.OBJ:
            assert isinstance(value, Obj)
            PrimitiveObjValue.__init__(self, value)

    def repr(self):
        if self.is_number():
            return ("%f" % self.value)[:16]
        elif self.is_bool():
            return "true" if self.value else "false"
        elif self.is_nil():
            return "nil"
        else:
            return str(self.value)

    def __repr__(self):
        return "<Value: '%s'>" % self.value

    def is_bool(self):
        return self.type == ValueType.BOOL

    def is_nil(self):
        return self.type == ValueType.NIL

    def is_number(self):
        return self.type == ValueType.NUMBER

    def is_obj(self):
        return self.type == ValueType.OBJ

    def is_string(self):
        return self.type == ValueType.OBJ and self.obj.type == ObjType.STRING

    def is_falsey(self):
        if self.is_bool():
            return not self.value
        elif self.is_nil():
            return True
        else:
            return False

    def is_equal(self, other):
        if self.type != other.type:
            return False
        if self.is_nil():
            return True
        else:
            return self.value == other.value


class PrimitiveNumberValue(Value):
    """
    Only used for primitive values.
    """

    def __init__(self, value, type=ValueType.NUMBER):
        self.type = type
        self.value = value


class PrimitiveBoolValue(Value):
    """
    Only used for primitive Boolean values
    """

    def __init__(self, value, type=ValueType.BOOL):
        self.type = type
        self.value = value


class PrimitiveNilValue(Value):
    """
    Only used for primitive values.
    """

    def __init__(self, value=None, type=ValueType.NIL):
        self.type = type


class PrimitiveObjValue(Value):
    """
    Only used for primitive values.
    """

    def __init__(self, value, type=ValueType.OBJ):
        self.type = type
        self.obj = value

    def is_equal(self, other):
        if self.type != other.type:
            return False
        assert isinstance(self.obj, Obj)
        assert isinstance(other.obj, Obj)

        return self.obj.is_equal(other.obj)

    def repr(self):
        return self.obj.repr()


class ValueArray(object):
    def __init__(self):
        self.values = []

    def __getitem__(self, item):
        return self.values[item]

    def index(self, item):
        # Return the index of an item in the array
        for i, value in enumerate(self.values):
            if item.is_equal(value):
                return i
        raise ValueError("Not found")

    def append(self, value):
        """

        :param value:
        :return: The index of the added constant/value
        """
        self.values.append(value)
        return len(self.values) - 1

