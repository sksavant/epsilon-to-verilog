import ply.lex as lex

tokens = ['SUMMARY','RETURN','FUNCTION','VAR','EQUALS','NUMBER','IF','ELSE','WHILE','LROUND','RROUND','LCURLY','RCURLY','ADD','MUL','DIV','SUB','MOD','LT','GT','LTE','GTE','EQEQ','NEQ']

t_ignore = ' \t\n'
def t_IF(t):
    r'if'
    return t
def t_ELSE(t):
    r'else'
    return t
def t_WHILE(t):
    r'while'
    return t
def t_FUNCTION(t):
    r'function'
    return t
def t_RETURN(t):
    r'return'
    return t

t_VAR = r'[a-zA-Z][a-zA-Z0-9_]*'
t_SUMMARY = r'\#[a-zA-Z0-9_ ][a-zA-Z0-9_ ]*\#'
t_EQUALS = r'='
t_ADD = r'\+'
t_MUL = r'\*'
t_DIV = r'/'
t_SUB = r'-'
t_MOD = r'%'
t_LT = r'<'
t_LTE = r'<='
t_GTE = r'>='
t_EQEQ = r'=='
t_NEQ = r'!='
t_GT = r'>'

t_LROUND = r'\('
t_RROUND = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'

def t_NUMBER(t):
    r'-?[0-9]+'
    t.value = int(t.value)
    return t

def t_error(t):
    print "illegal character ", t.value[0]
    t.lexer.skip(1)

lex.lex()
#lex.input("a <= b")
#while True:
    #tok = lex.token()
    #if not tok:
    #   break
    #print tok
