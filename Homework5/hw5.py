
import re
import sys
import math
import numbers
import ply.lex as lex
import ply.yacc as yacc
reserved = {
    #control statements & print
    'print':'PRINT',
    #Boolean operators
    'not':'NOT',
    'and':'AND',
    'or':'OR',
    'in':'IN',
    'if':'IF',
    'else' : 'ELSE',
    'while':'WHILE'
    }
tokens = [
    #Token Types
    'REAL', 'INTEGER', 'STRING',
    #Operators
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'FLRDIV', 'POWER',
    #Comparison
    'LESSTHAN', 'GREATERTHAN', 'LEQUAL', 'GEQUAL', 'EQEQ', 'NOTEQ',
    #Brackets, Braces and Parens
    'LPAREN', 'RPAREN',
    'LBRACK', 'RBRACK',
    'LBRACE', 'RBRACE',
    #Comma
    'COMMA',
    #Semicolon
    'SEMI',
    #Assignment
    'EQUALS', 'NAME'
    ] + list(reserved.values())
def t_REAL(t):
    r'-?\d*(\d\.|\.\d)\d*'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0.0
    return t
def t_INTEGER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t
def t_STRING(t):
    r'"([^\\"]*|\\.)*"'
    t.value = t.value[1:-1].replace("\\\"", "\"")
    return t
def t_NAME(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_MODULO      = r'%'
t_FLRDIV      = r'//'
t_POWER       = r'\*\*'
t_LESSTHAN    = r'<'
t_GREATERTHAN = r'>'
t_LEQUAL      = r'<='
t_GEQUAL      = r'>='
t_EQEQ        = r'=='
t_NOTEQ       = r'<>'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACK      = r'\['
t_RBRACK      = r'\]'
t_LBRACE      = r'{'
t_RBRACE      = r'}'
t_COMMA       = r','
t_SEMI        = r';'
t_EQUALS      = r'='
def t_error(t):
    print("SYNTAX ERROR '%s'" % t.value.strip())
    t.lexer.skip(len(t.value))
# Ignored characters
t_ignore = " \t"
lexer = lex.lex()
#############################################
## HELPER FUNCTIONS
#############################################
def handleSemanticError(p, parser, message):
    print("SEMANTIC ERROR: %s" % message.strip())
    if not p:
        return
    parser.errok()
def invalidTypesError(p, parser, operator):
    handleSemanticError(p, parser, "Invalid type on operator '%s'" % operator)
def invalidNameError(p, parser, name):
    handleSemanticError(p, parser, "Invalid name '%s'" % name)
def typesMatch(x,y):
    return (type(x) is type(y)) or (isinstance(x, numbers.Number) and isinstance(y, numbers.Number))
#############################################
##
## ABSTRACT SYNTAX TREE
##
#############################################
#############################################
## Expressions
#############################################
class Expression:
    #dummy parent class just for abstract syntax
    pass
class BinaryExpression(Expression):
    def __init__(self, left, op, right, p):
        self.left = left
        self.right = right
        self.op = op
        self.p = p
    def evaluate(self):
        leftEval = self.left.evaluate()
        rightEval = self.right.evaluate()
        if self.op == '+':
            if typesMatch(leftEval,rightEval):
                return leftEval + rightEval
            else:
                invalidTypesError(self.p, parser, self.op)
        elif self.op == 'in' and isinstance(rightEval, list) or isinstance(rightEval, str):
            return 1 if leftEval in rightEval else 0
        elif isinstance(leftEval, numbers.Number) and isinstance(rightEval, numbers.Number):
            if self.op == '-' :
                return leftEval - rightEval
            elif self.op == '*' :
                return leftEval * rightEval
            elif self.op == '/' :
                if rightEval != 0:
                    return leftEval / rightEval
                else:
                    handleSemanticError(p, parser, "Divide by zero")
            elif self.op == '%' :
                if rightEval != 0:
                    return leftEval % rightEval
                else:
                    handleSemanticError(p, parser, "Divide by zero")
            elif self.op == '//' :
                if rightEval != 0:
                    return leftEval // rightEval
                else:
                    handleSemanticError(p, parser, "Divide by zero")
            elif self.op == '**' :
                return leftEval ** rightEval
            elif self.op == '==' :
                return 1 if leftEval == rightEval else 0
            elif self.op == '<>' :
                return 1 if leftEval != rightEval else 0
            elif self.op == '<' :
                return 1 if leftEval < rightEval else 0
            elif self.op == '>' :
                return 1 if leftEval > rightEval else 0
            elif self.op == '<=' :
                return 1 if leftEval <= rightEval else 0
            elif self.op == '>=' :
                return 1 if leftEval >= rightEval else 0
            elif self.op == 'and' :
                return 1 if leftEval and rightEval else 0
            elif self.op == 'or' :
                return 1 if leftEval or rightEval else 0
            else:
                invalidTypesError(self.p, parser, self.op)
        else:
            invalidTypesError(self.p, parser, self.op)
class UnaryExpression(Expression):
    def __init__(self, op, right, p, left = None):
        self.left = left
        self.right = right
        self.op = op
    def evaluate(self):
        if isinstance(self.right, numbers.Number):
            return 1 if self.right == 0 else 0
        else:
            invalidTypesError(self.p, parser, self.op)
class TypeExpression(Expression):
    def __init__(self, value):
        self.value = value
    def evaluate(self):
        if isinstance(self.value, Expression):
            return self.value.evaluate()
        else:
            return self.value
class NameExpression(Expression):
    def __init__(self, name, p):
        self.name = name
        self.p = p
    def evaluate(self):
        if self.name in names:
            return names[self.name]
        else:
            invalidNameError(self.p, parser, self.name);
class IndexExpression(Expression):
    def __init__(self, base, index,p):
        self.base = base
        self.index = index
        self.p = p
    def evaluate(self):
        baseEval = self.base.evaluate()
        indexEval = self.index.evaluate()
        if (isinstance(baseEval, list) or isinstance(baseEval, str)) and isinstance(indexEval, int):
            if indexEval < len(baseEval):
                return baseEval[indexEval]
            else:
                handleSemanticError(self.p, parser, "Index out of bounds error.  List: {}, Index: {}".format(baseEval, indexEval))
        else:
            invalidTypesError(self.p, parser, '[')
#############################################
## Statements
#############################################
class Statement:
    #dummy parent class just for abstract syntax
    pass
class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression
    def execute(self):
        evaluated = self.expression.evaluate()
        if evaluated != None:
            print(evaluated)
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
        indexEval = self.index.evaluate()
        if (isinstance(potentialList, list) or isinstance(potentialList, str)) and isinstance(indexEval, int):
            names[self.name][indexEval] = self.expression.evaluate()
class BlockStatement(Statement):
    def __init__(self, statementList):
        self.statementList = statementList
    def execute(self):
        for statement in self.statementList:
            statement.execute()
class IfStatement(Statement):
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block
    def execute(self):
        if(self.expression.evaluate()):
            self.block.execute()
class IfElseStatement(Statement):
    def __init__(self, expression, ifBlock, elseBlock):
        self.expression = expression
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock
    def execute(self):
        if(self.expression.evaluate()):
            self.ifBlock.execute()
        else:
            self.elseBlock.execute()
class WhileStatement(Statement):
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block
    def execute(self):
        while(self.expression.evaluate()):
            self.block.execute()
#############################################
##
## PARSER
##
#############################################
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('right','NOT'),
    ('left','LESSTHAN','GREATERTHAN','LEQUAL','GEQUAL','EQEQ','NOTEQ'),
    ('left','IN'),
    ('left','PLUS','MINUS'),
    ('left','FLRDIV'),
    ('left','POWER'),
    ('left','MODULO'),
    ('left','TIMES','DIVIDE'),
    )
names = { }
def p_program(p):
    '''program : statement'''
    p[1].execute()
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 2:
            p[0] = [p[1]]
    else:
            p[0] = p[1] + [p[2]]
def p_block_statement(p):
    '''block_statement : LBRACE statement_list RBRACE'''
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
    '''print_statement : PRINT LPAREN expression RPAREN SEMI'''
    p[0] = PrintStatement(p[3])
def p_print_statement_error(p):
    '''print_statement : PRINT LPAREN error RPAREN SEMI'''
    p[0] = PrintStatement(TypeExpression("SYNTAX ERROR at line {}: '{}'".format(p[3].lineno, p[3].value)))
def p_while_statement(p):
    '''while_statement : WHILE expression block_statement'''
    p[0] = WhileStatement(p[2], p[3])
def p_while_statement_error(p):
    '''while_statement : WHILE error block_statement'''
    p[0] = PrintStatement(TypeExpression("SYNTAX ERROR at line {}: '{}'".format(p[2].lineno, p[2].value)))
def p_if_statement(p):
    '''if_statement : IF expression block_statement'''
    p[0] = IfStatement(p[2], p[3])
def p_if_statement_error(p):
    '''if_statement : IF error block_statement'''
    p[0] = PrintStatement(TypeExpression("SYNTAX ERROR at line {}: '{}'".format(p[2].lineno, p[2].value)))
def p_if_else_statement(p):
    '''if_else_statement : IF expression block_statement ELSE block_statement'''
    p[0] = IfElseStatement(p[2], p[3], p[5])
def p_if_else_statement_error(p):
    '''if_else_statement : IF error block_statement ELSE block_statement'''
    p[0] = PrintStatement(TypeExpression("SYNTAX ERROR at line {}: '{}'".format(p[2].lineno, p[2].value)))
def p_assignment_statement(p):
    '''assignment_statement : NAME EQUALS expression SEMI'''
    p[0] = AssignmentStatement(p[1],p[3])
def p_assignment_statement_list(p):
    '''assignment_statement : NAME LBRACK expression RBRACK EQUALS expression SEMI'''
    p[0] = IndexedAssignmentStatement(p[1],p[3],p[6])
def p_assignment_statement_error(p):
    '''assignment_statement : NAME EQUALS error SEMI'''
    p[0] = PrintStatement(TypeExpression("SYNTAX ERROR at line {}: '{}'".format(p[3].lineno, p[3].value)))
def p_expression(p):
    '''expression : LPAREN expression RPAREN
                  | expression PLUS        expression
                  | expression MINUS       expression
                  | expression TIMES       expression
                  | expression DIVIDE      expression
                  | expression FLRDIV      expression
                  | expression POWER       expression
                  | expression MODULO      expression
                  | expression IN          expression
                  | expression EQEQ        expression
                  | expression NOTEQ       expression
                  | expression LESSTHAN    expression
                  | expression GREATERTHAN expression
                  | expression LEQUAL      expression
                  | expression GEQUAL      expression
                  | expression AND         expression
                  | expression OR          expression '''
    if p[1] == '(' and p[3] == ')':
        p[0] = p[2]
    else:
        p[0] = BinaryExpression(p[1],p[2],p[3],p)
def p_unary_expression(p):
    '''expression : NOT expression'''
    p[0] = UnaryExpression(p[1],p[2],p);
def p_expression_types(p):
    '''expression : STRING
                  | REAL
                  | INTEGER
                  | list_expression'''
    p[0] = TypeExpression(p[1])
def p_expression_index(p):
    '''expression : index_expression'''
    p[0] = p[1]
def p_expression_name(p):
    '''expression : NAME'''
    p[0] = NameExpression(p[1], p)
def p_list_expression(p):
    '''list_expression : LBRACK inner_list RBRACK'''
    p[0] = TypeExpression(p[2])
def p_inner_list(p):
    '''inner_list : inner_list COMMA expression
                  | expression'''
    if len(p) == 2:
        p[0] = [p[1].evaluate()]
    else:
        p[0] = p[1] + [p[3].evaluate()]
def p_index_expression(p):
    '''index_expression : expression LBRACK expression RBRACK'''
    p[0] = IndexExpression(p[1],p[3],p)
def p_error(p):
    pass
import ply.yacc as yacc
parser = yacc.yacc()
while True:
    try:
        s = input('> ')
    except EOFError:
        break
    parser.parse(s)