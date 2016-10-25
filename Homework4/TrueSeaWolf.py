# ------------------------- #
# James Lynn, ID: 108708026 #
# CSE 307                   #
#                           #
# TrueSeaWolf.py            #
# An expression evaluator.  #
# ------------------------- #

tokens = (
    'NUMBER', 'STRING', 'LIST',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'NOTEQUALS', 'MODULUS', 'EXPONENT', 'FLOORDIVISION',
    'GREATERTHAN', 'LESSTHAN', 'LPAREN', 'RPAREN', 'GREATERTHANEQUAL', 'LESSTHANEQUAL'
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


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"([^"\n]|(\\"))*"$'
    t.value = str(t.value)
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

# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
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
                  | expression NOTEQUALS expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '\\':
        p[0] = p[1] // p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    elif p[2] == '**':
        p[0] = p[1] ** p[3]
    elif p[2] == '<':
        if p[1] < p[3]:
            p[0] = "true"
        else:
            p[0] = "false"
    elif p[2] == '>':
        if p[1] > p[3]:
            p[0] = "true"
        else:
            p[0] = "false"
    elif p[2] == '<=':
        if p[1] < p[3]:
            p[0] = "true"
        elif p[1] == p[3]:
            p[0] = "true"
        else:
            p[0] = "false"
    elif p[2] == '>=':
        if p[1] > p[3]:
            p[0] = "true"
        elif p[1] == p[3]:
            p[0] = "true"
        else:
            p[0] = "false"
    elif p[2] == '==':
        if p[1] == p[3]:
            p[0] = "true"
        else:
            p[0] = "false"
    elif p[2] == '<>':
        if p[1] == p[3]:
            p[0] = "false"
        else:
            p[0] = "true"


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]


def p_error(p):
    print("Syntax error at '%s'" % p.value)


import ply.yacc as yacc
import sys

yacc.yacc()

while True:
    try:
        s = input("> ")
    except EOFError:
        break
    yacc.parse(s)
