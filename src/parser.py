from sly import Lexer, Parser
import vm


class MyLexer(Lexer):
    tokens = {IDENTIFIER, NUMBER, SEMICOLON, PLUS, MINUS,
              ASTERISK, FORWARD_SLASH, EQUALS, KEYWORD_VAR}

    KEYWORD_VAR = r'var'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'[0-9]+'
    SEMICOLON = r';'
    PLUS = r'\+'
    MINUS = r'\-'
    ASTERISK = r'\*'
    FORWARD_SLASH = r'\/'
    EQUALS = r'='

    ignore = ' \t\n'


class MyParser(Parser):
    tokens = MyLexer.tokens

    def __init__(self, bytecode: vm.Bytecode):
        self.bytecode = bytecode
        self.storageIndex = 0
        self.storageTable = {}

    @_("statements statement")
    def statements(self, p):
        pass

    @_("statement")
    def statements(self, p):
        pass

    @_("KEYWORD_VAR IDENTIFIER EQUALS expr SEMICOLON")
    def statement(self, p):
        self.storageTable[p.IDENTIFIER] = self.storageIndex
        self.bytecode.emit(vm.Instruction.STORE)
        self.bytecode.emit(self.storageIndex)
        self.storageIndex += 1

    @_("expr PLUS expr1",
       "expr MINUS expr1")
    def expr(self, p):
        if p[1] == '+':
            self.bytecode.emit(vm.Instruction.ADD)
        else:
            self.bytecode.emit(vm.Instruction.SUB)

    @_("expr1")
    def expr(self, p):
        pass

    @_("expr1 ASTERISK expr2",
       "expr1 FORWARD_SLASH expr2")
    def expr1(self, p):
        if p[1] == '*':
            self.bytecode.emit(vm.Instruction.MUL)
        else:
            self.bytecode.emit(vm.Instruction.DIV)

    @_("expr2")
    def expr1(self, p):
        pass

    @_("NUMBER")
    def expr2(self, p):
        self.bytecode.emit(vm.Instruction.PUSH)
        self.bytecode.emit(int(p[0]))

    @_("IDENTIFIER")
    def expr2(self, p):
        self.bytecode.emit(vm.Instruction.LOAD)
        self.bytecode.emit(self.storageTable[p.IDENTIFIER])
