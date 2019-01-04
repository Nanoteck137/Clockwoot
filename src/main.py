from parser import MyLexer, MyParser
from collections import deque
from vm import VM, Bytecode, Instruction


def run():
    bytecode = Bytecode()

    lexer = MyLexer()
    parser = MyParser(bytecode)

    code = '''
    var x = 1 - 2 - 3;
    var y = 1 + 2 + 3 + x;
    '''

    #result = parser.parse(lexer.tokenize(code))

    # Initialize the counter
    bytecode.emit(Instruction.PUSH)
    bytecode.emit(0)
    bytecode.emit(Instruction.STORE)
    bytecode.emit(0)

    # Initalize the value
    bytecode.emit(Instruction.PUSH)
    bytecode.emit(10)

    bytecode.emit(Instruction.DUP)

    # Branch if the value is 0
    bytecode.emit(Instruction.BRZ)
    bytecode.emit(12)

    # Loads the counter
    bytecode.emit(Instruction.LOAD)
    bytecode.emit(0)

    # Adds one to the counter
    bytecode.emit(Instruction.PUSH)
    bytecode.emit(1)

    bytecode.emit(Instruction.ADD)

    # Stores the counter again
    bytecode.emit(Instruction.STORE)
    bytecode.emit(0)

    # Pushes 2 on the stack
    bytecode.emit(Instruction.PUSH)
    bytecode.emit(2)

    # Subtracts 2 from the value
    bytecode.emit(Instruction.SUB)

    # Jumps back to the top
    bytecode.emit(Instruction.JMP)
    bytecode.emit(-15)

    bytecode.emit(Instruction.HALT)

    bytecode.dumpinstructions()

    vm = VM(bytecode)
    vm.run()

    print("stack:", vm.stack)
    print("storage:", vm.storage)


if __name__ == "__main__":
    run()
