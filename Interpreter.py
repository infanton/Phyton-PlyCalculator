# --------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# --------------------------------------------------------------------

import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

######################################################################
# Scanner
tokens = ('NAME', 'NUMBER',)
literals = ['=', '+', '-', '*', '/', '(', ')']

# Tokens
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

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

################################################
# BNF
# <expr> ::- <term> ADD <expr>
#        |   <term>
# <term> ::- <factor> MULT <term>
#        |   <factor>
# <factor> ::- LPAREN <expr> RPAREN
#        |  NUM

# In all of the following productions,
# p[0] is always assigned a function that returns a float
def p_expression_add(p):
    ''' expr : term '+' expr '''
    a = p[1]; b = p[3]; p[0] = lambda : a() + b()

def p_expression_term(p):
    ''' expr : term '''
    p[0] = p[1]

def p_term_mult(p):
    ''' term : factor '*' term '''
    a= p[1]; b = p[3]; p[0] = lambda : a() * b()

def p_term_factor(p):
    ''' term : factor '''
    p[0] = p[1]

def p_factor_group(p):
    ''' factor : '(' expr ')' '''
    p[0] = p[2]

def p_factor_number(p):
    ''' factor : NUMBER '''
    a = p[1]; p[0] = lambda : a

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

######################################################################
# Driver program
while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    print(yacc.parse(s,debug=False)())
