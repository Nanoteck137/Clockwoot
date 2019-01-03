from parser import MyLexer, MyParser
from collections import deque
from vm import VM, Bytecode


def run():
    bytecode = Bytecode()

    lexer = MyLexer()
    parser = MyParser(bytecode)

    code = '''
    var x = 1 - 2 - 3;
    var y = 1 + 2 + 3 + x;
    '''

    result = parser.parse(lexer.tokenize(code))

    bytecode.dumpinstructions()

    vm = VM(bytecode)
    vm.run()

    print("stack:", vm.stack)
    print("storage:", vm.storage)


if __name__ == "__main__":
    run()
