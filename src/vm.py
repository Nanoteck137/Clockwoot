from collections import deque, namedtuple


def insnop(vm):
    pass


def inshalt(vm):
    vm.running = False


def inspush(vm):
    vm.pushstack(vm.readpc())


def inspop(vm):
    vm.popstack()


def insload(vm):
    index = vm.readpc()
    vm.pushstack(vm.storage[index])


def insstore(vm):
    index = vm.readpc()
    vm.storage.insert(index, vm.popstack())


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


NOP = 0x00
HALT = 0x01

PUSH = 0x02
POP = 0x03

LOAD = 0x04
STORE = 0x05

ADD = 0x06
SUB = 0x07
MUL = 0x08
DIV = 0x09

InsTuple = namedtuple("InstructionTuple", ["name", "operands", "func"])

instructions = []
instructions.insert(NOP, InsTuple("nop", 0, insnop))
instructions.insert(HALT, InsTuple("halt", 0, inshalt))

instructions.insert(PUSH, InsTuple("push", 1, inspush))
instructions.insert(POP, InsTuple("pop", 1, inspop))

instructions.insert(LOAD, InsTuple("load", 1, insload))
instructions.insert(STORE, InsTuple("store", 1, insstore))

instructions.insert(ADD, InsTuple("add", 0, insadd))
instructions.insert(SUB, InsTuple("sub", 0, inssub))
instructions.insert(MUL, InsTuple("mul", 0, insmul))
instructions.insert(DIV, InsTuple("div", 0, insdiv))


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
        self.stack = deque(maxlen=10)
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
