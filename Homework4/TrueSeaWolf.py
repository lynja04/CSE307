# ------------------------- #
# James Lynn, ID: 108708026 #
# CSE 307                   #
#                           #
# TrueSeaWolf.py            #
# An expression evaluator.  #
# ------------------------- #

tokens = (
    'REAL', 'INTEGER', 'STRING', 'LBRACKET', 'RBRACKET', 'COMMA',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'NOTEQUALS', 'MODULUS', 'EXPONENT', 'FLOORDIVISION',
    'GREATERTHAN', 'LESSTHAN', 'LPAREN', 'RPAREN', 'GREATERTHANEQUAL', 'LESSTHANEQUAL',
    'AND', 'OR', 'IN', 'NOT'
)

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_FLOORDIVISION = r'\\'
t_MODULUS = r'%'
t_EXPONENT = r'\*\*'
t_EQUALS = r'=='
t_NOTEQUALS = r'<>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
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
t_COMMA = ","


def t_REAL(t):
    r'\d*\.\d*'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
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


def p_statement_expr(p):
    'statement : expression'
    if type(p[1]) == str:
        p[1] = "'" + p[1] + "'"
    print(p[1])


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
    '''expression : expression PLUS expression
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

    if p[2] == '+':
        if typesMatch(p[1], p[3]):
            p[0] = p[1] + p[3]
        else:
            p[0] = "SEMANTIC ERROR"
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            p[0] = "SEMANTIC ERROR"
        else:
            p[0] = p[1] / p[3]
    elif p[2] == '\\':
        p[0] = p[1] // p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    elif p[2] == '**':
        p[0] = p[1] ** p[3]
    elif p[2] == '<':
        if p[1] < p[3]:
            p[0] = 1
        else:
            p[0] = 0
    elif p[2] == '>':
        if p[1] > p[3]:
            p[0] = 1
        else:
            p[0] = 0
    elif p[2] == '<=':
        if p[1] < p[3]:
            p[0] = 1
        elif p[1] == p[3]:
            p[0] = 1
        else:
            p[0] = 0
    elif p[2] == '>=':
        if p[1] > p[3]:
            p[0] = 1
        elif p[1] == p[3]:
            p[0] = 1
        else:
            p[0] = 0
    elif p[2] == '==':
        if p[1] == p[3]:
            p[0] = 1
        else:
            p[0] = 0
    elif p[2] == '<>':
        if p[1] == p[3]:
            p[0] = 0
        else:
            p[0] = "true"
    elif p[2] == 'and':
        if p[1] == 1 or p[1] > 0:
            if p[3] == 1:
                p[0] = 1
            elif p[3] > 0:
                p[0] = 1
            else:
                p[0] = 0
        else:
            p[0] = 0
    elif p[2] == 'or':
        if p[1] == 1:
            p[0] = 1
        elif p[3] == 1:
            p[0] = 1
        elif p[3] > 0 or p[1] > 0:
            p[0] = 1
        else:
            p[0] = 0
    elif p[2] == 'in':
        if p[1] in p[3]:
            p[0] = 1
        else:
            p[0] = 0


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_expression_not(p):
    'expression : NOT expression'
    if p[2] == 0:
        p[0] = "true"
    else:
        p[0] = "false"


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_types(p):
    '''expression : INTEGER
                  | REAL
                  | STRING
                  | LIST
                  | INDEXED_STRING
                  | INDEXED_LIST'''
    p[0] = p[1]


def p_expression_listExpression(p):
    'LIST : LBRACKET innerList RBRACKET'
    p[0] = p[2]


def p_expression_innerList(p):
    '''innerList : innerList COMMA expression
                 | expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_expression_indexed_string(p):
    'INDEXED_STRING : STRING LBRACKET expression RBRACKET'
    if p[3] > len(p[1]):
        p[0] = "SEMANTIC ERROR"
    else:
        p[0] = p[1][p[3]]


def p_expression_indexed_list(p):
    'INDEXED_LIST : LIST LBRACKET expression RBRACKET'
    if p[3] > len(p[1]):
        p[0] = "SEMANTIC ERROR"
    else:
        p[0] = p[1][p[3]]


def p_error(p):
    pass

import ply.yacc as yacc
import sys
yacc.yacc()
r = open(sys.argv[1], "r")
for line in r:
    yacc.parse(line)
