from lox.value import ValueType, Value
from rpython.rlib.objectmodel import specialize

try:
    from rpython.rlib.jit import JitDriver
except ImportError:
    class JitDriver(object):
        def __init__(self,**kw): pass
        def jit_merge_point(self,**kw): pass
        def can_enter_jit(self,**kw): pass

from lox import OpCode, Compiler
from lox.debug import disassemble_instruction, get_printable_location, format_line_number

jitdriver = JitDriver(
    greens=['ip', 'instruction', 'chunk', 'vm'],
    reds=['stack_top', 'stack'],
    get_printable_location=get_printable_location
)


class IntepretResultCode:
    """

    """

    INTERPRET_OK = 0
    INTERPRET_COMPILE_ERROR = 1
    INTERPRET_RUNTIME_ERROR = 2


IntepretResultToName = {getattr(IntepretResultCode, op): op
                        for op in dir(IntepretResultCode) if op.startswith('INTERPRET_')}


class VM(object):
    STACK_MAX_SIZE = 256

    chunk = None
    stack = None
    stack_top = 0

    # Instruction Pointer (or Program Counter)
    # points to the next instruction to be executed
    ip = 0

    def __init__(self, debug=True):
        self.debug_trace = debug
        self._reset_stack()

    def _runtime_error(self, message):
        # Print the line number
        line_number = format_line_number(self.chunk, self.ip),
        print "%s\n[line %s] in script" % (message, line_number)
        self._reset_stack()

    def _reset_stack(self):
        self._nil_value = Value(0, ValueType.NIL)
        self.stack = [self._nil_value] * self.STACK_MAX_SIZE
        self.stack_top = 0

    def _stack_push(self, value):
        assert self.stack_top < self.STACK_MAX_SIZE
        self.stack[self.stack_top] = value
        self.stack_top += 1

    def _stack_pop(self):
        assert self.stack_top >= 0
        self.stack_top -= 1
        return self.stack[self.stack_top]

    def _stack_peek(self, distance=0):
        assert self.stack_top >= 0
        assert self.stack_top - distance > 0
        return self.stack[self.stack_top - 1 - distance]

    def _run(self):
        instruction = OpCode.OP_TEST
        while True:
            jitdriver.jit_merge_point(
                ip=self.ip,
                chunk=self.chunk,
                stack=self.stack,
                stack_top=self.stack_top,
                instruction=instruction,
                vm=self
            )

            if self.debug_trace:
                self._print_stack()
                disassemble_instruction(self.chunk, self.ip)
            instruction = self._read_byte()

            if instruction == OpCode.OP_RETURN:
                print "%s" % self._stack_pop().debug_repr()
                return IntepretResultCode.INTERPRET_OK
            elif instruction == OpCode.OP_CONSTANT:
                lox_value = self._read_constant()
                self._stack_push(lox_value)
            elif instruction == OpCode.OP_NIL:
                self._stack_push(self._nil_value)
            elif instruction == OpCode.OP_TRUE:
                self._stack_push(Value(True, ValueType.BOOL))
            elif instruction == OpCode.OP_FALSE:
                self._stack_push(Value(False, ValueType.BOOL))

            elif instruction == OpCode.OP_ADD:
                self._binary_op(self._stack_add, ValueType.NUMBER)
            elif instruction == OpCode.OP_SUBTRACT:
                self._binary_op(self._stack_subtract, ValueType.NUMBER)
            elif instruction == OpCode.OP_MULTIPLY:
                self._binary_op(self._stack_multiply, ValueType.NUMBER)
            elif instruction == OpCode.OP_DIVIDE:
                self._binary_op(self._stack_divide, ValueType.NUMBER)
            elif instruction == OpCode.OP_NEGATE:
                if not self._stack_peek().is_number():
                    self._runtime_error("Operand must be a number.")
                    return IntepretResultCode.INTERPRET_RUNTIME_ERROR
                operand = self._stack_pop().value
                self._stack_push(Value(-1 * operand, ValueType.NUMBER))

    def _print_stack(self):
        print "         ",
        if self.stack_top <= 0:
            print "[]",
        else:
            for i in range(self.stack_top):
                print "[ %s ]" % self.stack[i].value,
        print

    @staticmethod
    def _stack_add(op1, op2):
        return op1 + op2

    @staticmethod
    def _stack_subtract(op1, op2):
        return op1 - op2

    @staticmethod
    def _stack_multiply(op1, op2):
        return op1 * op2

    @staticmethod
    def _stack_divide(op1, op2):
        return op1 / op2

    def interpret(self, source):
        self._reset_stack()
        compiler = Compiler(source, debugging=self.debug_trace)
        if compiler.compile():
            return self.interpret_chunk(compiler.current_chunk())
        else:
            return IntepretResultCode.INTERPRET_COMPILE_ERROR

    def interpret_chunk(self, chunk):
        if self.debug_trace:
            print "== VM TRACE =="
        self.chunk = chunk
        self.ip = 0
        try:
            result = self._run()
            return result
        except:
            return IntepretResultCode.INTERPRET_RUNTIME_ERROR

    def _read_byte(self):
        instruction = self.chunk.code[self.ip]
        self.ip += 1
        return instruction

    def _read_constant(self):
        constant_index = self._read_byte()
        # already a lox value
        return self.chunk.constants[constant_index]

    def print_value(self, constant):
        print "value: %f" % constant.value

    @specialize.arg(1)
    def _binary_op(self, operator, value_type):
        if not self._stack_peek().is_number() or not self._stack_peek(1).is_number():
            self._runtime_error("Operands must be numbers.")
            raise Exception("INTERPRET_RUNTIME_ERROR")
        op2 = self._stack_pop()
        op1 = self._stack_pop()
        raw_result = operator(op1.value, op2.value)
        lox_value = Value(raw_result, value_type)
        self._stack_push(lox_value)
