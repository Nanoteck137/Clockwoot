from collections import deque, namedtuple
from enum import IntEnum, auto


def insnop(vm):
    pass


def inshalt(vm):
    vm.running = False


def inspush(vm):
    vm.pushstack(vm.readpc())


def inspop(vm):
    vm.popstack()


def insdup(vm):
    # TODO(patrik): Add a peek stack method on the vm
    val = vm.popstack()
    vm.pushstack(val)
    vm.pushstack(val)


def insload(vm):
    index = vm.readpc()
    vm.pushstack(vm.storage[index])


def insstore(vm):
    index = vm.readpc()
    try:
        del vm.storage[index]
    except:
        pass

    vm.storage.insert(index, vm.popstack())


def insjmp(vm):
    count = vm.readpc()
    vm.pc += count


def insbrz(vm):
    count = vm.readpc()
    val = vm.popstack()
    if val == 0:
        vm.pc += count


def insadd(vm):
    right = vm.popstack()
    left = vm.popstack()
    vm.pushstack(left + right)


def inssub(vm):
    right = vm.popstack()
    left = vm.popstack()
    vm.pushstack(left - right)


def insmul(vm):
    right = vm.popstack()
    left = vm.popstack()
    vm.pushstack(left * right)


def insdiv(vm):
    right = vm.popstack()
    left = vm.popstack()
    vm.pushstack(left / right)


class TestEnum(IntEnum):
    def _generate_next_value_(name, start, count, last_values):
        return count


class Instruction(TestEnum):
    NOP = auto()
    HALT = auto()

    PUSH = auto()
    POP = auto()
    DUP = auto()

    LOAD = auto()
    STORE = auto()

    JMP = auto()
    BRZ = auto()

    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()


InsTuple = namedtuple("InstructionTuple", ["name", "operands", "func"])

instructions = []
instructions.insert(Instruction.NOP, InsTuple("nop", 0, insnop))
instructions.insert(Instruction.HALT, InsTuple("halt", 0, inshalt))

instructions.insert(Instruction.PUSH, InsTuple("push", 1, inspush))
instructions.insert(Instruction.POP, InsTuple("pop", 0, inspop))
instructions.insert(Instruction.DUP, InsTuple("dup", 0, insdup))

instructions.insert(Instruction.LOAD, InsTuple("load", 1, insload))
instructions.insert(Instruction.STORE, InsTuple("store", 1, insstore))

instructions.insert(Instruction.JMP, InsTuple("jmp", 1, insjmp))
instructions.insert(Instruction.BRZ, InsTuple("brz", 1, insbrz))

instructions.insert(Instruction.ADD, InsTuple("add", 0, insadd))
instructions.insert(Instruction.SUB, InsTuple("sub", 0, inssub))
instructions.insert(Instruction.MUL, InsTuple("mul", 0, insmul))
instructions.insert(Instruction.DIV, InsTuple("div", 0, insdiv))


class Bytecode:
    def __init__(self):
        self.list = []

    def emit(self, value: int):
        self.list.append(value)

    def dumpinstructions(self):
        count = 0
        while count < len(self.list):
            inst = instructions[self.list[count]]

            printStr = inst.name

            for i in range(0, inst.operands):
                printStr += " " + str(self.list[count + (i + 1)])

            print(printStr)

            count += (1 + inst.operands)


class VM:
    def __init__(self, bytecode: Bytecode):
        self.bytecode = bytecode
        self.pc = 0
        self.running = True
        self.stack = deque([], maxlen=10)
        self.storage = []

    def readpc(self):
        opcode = self.bytecode.list[self.pc]
        self.pc += 1
        return opcode

    def pushstack(self, value):
        self.stack.append(value)

    def popstack(self):
        return self.stack.pop()

    def runsingle(self):
        opcode = self.readpc()

        instruction = instructions[opcode]
        instruction.func(self)

        if self.pc >= len(self.bytecode.list):
            self.running = False

    def run(self):
        while self.running:
            self.runsingle()
