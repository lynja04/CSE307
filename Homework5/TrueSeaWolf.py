# ------------------------- #
# James Lynn, ID: 108708026 #
# CSE 307                   #
#                           #
# TrueSeaWolf.py            #
# An expression evaluator.  #
# ------------------------- #

tokens = [
    'REAL', 'INTEGER', 'STRING', 'LBRACKET', 'RBRACKET', 'COMMA',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'NOTEQUALS', 'MODULUS', 'EXPONENT', 'FLOORDIVISION',
    'GREATERTHAN', 'LESSTHAN', 'LPAREN', 'RPAREN', 'GREATERTHANEQUAL', 'LESSTHANEQUAL',
    'AND', 'OR', 'IN', 'NOT', 'NAME', 'SEMI', 'LBRACE', 'RBRACE', 'PRINT', 'IF', 'ELSE', 'WHILE', 'EQUAL'
]

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_FLOORDIVISION = r'\\'
t_MODULUS = r'%'
t_EXPONENT = r'\*\*'
t_EQUALS = r'=='
t_EQUAL = r'\='
t_NOTEQUALS = r'<>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_GREATERTHAN = r'>'
t_LESSTHAN = r'<'
t_GREATERTHANEQUAL = r'>='
t_LESSTHANEQUAL = r'<='
t_AND = r'and'
t_OR = r'or'
t_IN = r'in'
t_NOT = r'not'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMI = r';'
t_NAME = r'[a-zA-Z][a-zA-Z0-9_]*'


def t_REAL(t):
    r'\d*\.\d*'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_PRINT(t):
    r'print'
    return t


def t_IF(t):
    r'if'
    return t


def t_ELSE(t):
    r'else'
    return t


def t_WHILE(t):
    r'while'
    return t


def t_STRING(t):
    r'"([^\\"]*|\\.)*"'
    t.value = str(t.value[1:-1])
    return t

# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()


class Expression:
    pass


class BinaryExpression(Expression):
    def __init__(self, leftNode, operator, rightNode):
        self.leftNode = leftNode
        self.operator = operator
        self.rightNode = rightNode

    def evaluate(self):
        leftEvaluate = self.leftNode.evaluate()
        rightEvaluate = self.rightNode.evaluate()
        if self.operator == '+':
            if typesMatch(leftEvaluate, rightEvaluate):
                return leftEvaluate + rightEvaluate
        elif self.operator == '-':
            return leftEvaluate - rightEvaluate
        elif self.operator == '*':
            return leftEvaluate * rightEvaluate
        elif self.operator == '/':
            if rightEvaluate != 0:
                return leftEvaluate / rightEvaluate
            else:
                return "SEMANTIC ERROR"
        elif self.operator == '//':
            if rightEvaluate != 0:
                return leftEvaluate // rightEvaluate
            else:
                return "SEMANTIC ERROR"
        elif self.operator == '%':
            if rightEvaluate != 0:
                return leftEvaluate % rightEvaluate
            else:
                return "SEMANTIC ERROR"
        elif self.operator == '**':
            return leftEvaluate ** rightEvaluate
        elif self.operator == '==':
            if leftEvaluate == rightEvaluate:
                return 1
            else:
                return 0
        elif self.operator == '<':
            if leftEvaluate < rightEvaluate:
                return 1
            else:
                return 0
        elif self.operator == '>':
            if leftEvaluate > rightEvaluate:
                return 1
            else:
                return 0
        elif self.operator == '<=':
            if leftEvaluate < rightEvaluate:
                return 1
            elif leftEvaluate == rightEvaluate:
                return 1
            else:
                return 0
        elif self.operator == '>=':
            if leftEvaluate > rightEvaluate:
                return 1
            elif leftEvaluate == rightEvaluate:
                return 1
            else:
                return 0
        elif self.operator == '<>':
            if leftEvaluate != rightEvaluate:
                return 1
            else:
                return 0
        elif self.operator == 'and':
            if leftEvaluate == 1 or leftEvaluate > 0:
                if rightEvaluate == 1:
                    return 1
                elif rightEvaluate > 0:
                    return 1
                else:
                    return 0
        elif self.operator == 'or':
            if leftEvaluate == 1:
                return 1
            elif rightEvaluate == 1:
                return 1
            elif rightEvaluate > 0 or leftEvaluate > 0:
                return 1
            else:
                return 0
        elif self.operator == 'in':
            if leftEvaluate in rightEvaluate:
                return 1
            else:
                return 0


class NameExpression(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        if self.name in names:
            return names[self.name]


class TypeExpression(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        if isinstance(self.value, Expression):
            return self.value.evaluate()
        else:
            return self.value


class IndexExpression(Expression):
    def __init__(self, base, index):
        self.base = base
        self.index = index

    def evaluate(self):
        baseEvaluated = self.base.evaluate()
        indexEvaluated = self.index.evaluate()
        if (isinstance(baseEvaluated, list) or isinstance(baseEvaluated, str)) and isinstance(indexEvaluated, int):
            if indexEvaluated < len(baseEvaluated):
                return baseEvaluated[indexEvaluated]


class Statement:
    pass


class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        evaluatedExpression = self.expression.evaluate()
        print(evaluatedExpression)


class BlockStatement(Statement):
    def __init__(self, statementlist):
        self.statementlist = statementlist

    def execute(self):
        for statement in self.statementlist:
            statement.execute()


class AssignmentStatement(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def execute(self):
        names[self.name] = self.expression.evaluate()


class IndexedAssignmentStatement(Statement):
    def __init__(self, name, index, expression):
        self.name = name
        self.index = index
        self.expression = expression

    def execute(self):
        potentialList = names[self.name]
        indexEvaluated = self.index.evaluate()
        if (isinstance(potentialList, list) or isinstance(potentialList, str)) and isinstance(indexEvaluated, int):
            names[self.name][indexEvaluated] = self.expression.evaluate()


class IfStatement(Statement):
    def __init__(self, expression, blockStatement):
        self.expression = expression
        self.blockStatement = blockStatement

    def execute(self):
        if self.expression.evaluate():
            self.blockStatement.execute()


class IfElseStatement(Statement):
    def __init__(self, expression, ifBlockStatement, elseBlockStatement):
        self.expression = expression
        self.ifBlockStatement = ifBlockStatement
        self.elseBlockStatement = elseBlockStatement

    def execute(self):
        if self.expression.evaluate():
            self.ifBlockStatement.execute()
        else:
            self.elseBlockStatement.execute()


class WhileStatement(Statement):
    def __init__(self, expression, blockStatement):
        self.expression = expression
        self.blockStatement = blockStatement

    def execute(self):
        while self.expression.evaluate():
            self.blockStatement.execute()


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'LESSTHAN', 'GREATERTHAN', 'LESSTHANEQUAL', 'GREATERTHANEQUAL', 'EQUALS', 'NOTEQUALS'),
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'FLOORDIVISION'),
    ('left', 'EXPONENT'),
    ('left', 'MODULUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)


names = {}


def p_application(p):
    'application : statement'
    p[1].execute()


def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_block_statement(p):
    'block_statement : LBRACE statement_list RBRACE'
    p[0] = BlockStatement(p[2])


def p_statement(p):
    '''statement : print_statement
                 | assignment_statement
                 | if_statement
                 | if_else_statement
                 | while_statement
                 | block_statement'''
    p[0] = p[1]


def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMI'
    p[0] = PrintStatement(p[3])


def p_if_statement(p):
    'if_statement : IF expression block_statement'
    p[0] = IfStatement(p[2], p[3])


def p_if_else_statement(p):
    'if_else_statement : IF expression block_statement ELSE block_statement'
    p[0] = IfElseStatement(p[2], p[3], p[5])


def p_while_statement(p):
    'while_statement : WHILE expression block_statement'
    p[0] = WhileStatement(p[2], p[3])


def p_assignment_statement(p):
    'assignment_statement : NAME EQUAL expression SEMI'
    p[0] = AssignmentStatement(p[1], p[3])


def p_assignment_statement_list(p):
    'assignment_statement : NAME LBRACKET expression RBRACKET EQUAL expression SEMI'
    p[0] = IndexedAssignmentStatement(p[1], p[3], p[6])


def p_expression_name(p):
    'expression : NAME'
    p[0] = NameExpression(p[1])


def typesMatch(first, second):
    if type(first) == type(second):
        return True
    elif type(first) == int and type(second) == float:
        return True
    elif type(first) == float and type(second) == int:
        return True
    else:
        return False


def p_expression_operators(p):
    '''expression : LPAREN expression RPAREN
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression FLOORDIVISION expression
                  | expression MODULUS expression
                  | expression EXPONENT expression
                  | expression GREATERTHAN expression
                  | expression LESSTHAN expression
                  | expression GREATERTHANEQUAL expression
                  | expression LESSTHANEQUAL expression
                  | expression EQUALS expression
                  | expression NOTEQUALS expression
                  | expression AND expression
                  | expression OR expression
                  | expression IN expression'''

    if p[1] == '(' and p[3] == ')':
        p[0] = p[2]
    else:
        p[0] = BinaryExpression(p[1], p[2], p[3])


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_expression_not(p):
    'expression : NOT expression'
    if p[2] == 0:
        p[0] = 1
    else:
        p[0] = 0


def p_expression_types(p):
    '''expression : INTEGER
                  | REAL
                  | STRING
                  | list_expression'''

    p[0] = TypeExpression(p[1])


def p_expression_index(p):
    'expression : index_expression'
    p[0] = p[1]


def p_expression_listExpression(p):
    'list_expression : LBRACKET innerList RBRACKET'
    p[0] = TypeExpression(p[2])


def p_expression_innerList(p):
    '''innerList : innerList COMMA expression
                 | expression'''
    if len(p) == 2:
        p[0] = [p[1].evaluate()]
    else:
        p[0] = p[1] + [p[3].evaluate()]

def p_expression_indexExpression(p):
    'index_expression : expression LBRACKET expression RBRACKET'
    p[0] = IndexExpression(p[1], p[3])

def p_error(p):
    pass

import ply.yacc as yacc
import sys
parser = yacc.yacc()
file = open(sys.argv[1], "r")
program = file.read()
parser.parse(program)
