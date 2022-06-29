import ply.lex as lex
import ply.yacc as yacc

# s -> TYPE ID STRUCT L_BRCK t R_BRCK s | lamda.
# s_anidado -> STRUCT L_BRCK t R_BRCK.
# t -> ID t'
# t' -> s_anidado | tipo | array
# tipo -> STRING| INT |FLOAT64 | BOOL.
# array -> ARRAY array'.
# array' -> tipo | array.



# VT = {STRING, INT, FLOAT64, BOOL, RBRACKET, LBRACKET, ARRAY, STRUCT}
tokens = ['TYPE','ID','STRING', 'INT', 'FLOAT64', 'BOOL', 'R_BRCK', 'L_BRCK', 'ARRAY', 'STRUCT' ]



t_L_BRCK = r'{'
t_R_BRCK = r'}'
t_ARRAY = r'\[\]'
# ToDo: Agregar EndofLine 
t_ignore = ' \t\n'



def t_TYPE(t):
    r'type'
    t.type = 'TYPE'
    return t

def t_STRUCT(t):
    r'struct'
    t.type = 'STRUCT'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'ID'
    return t

def t_STRING(t):
    r'string'
    t.type = 'STRING'
    return t

def t_INT(t):
    r'int'
    t.type = 'INT'
    return t

def t_BOOL(t):
    r'bool'
    t.type = 'BOOL'
    return t

def t_FLOAT64(t):
    r'float64'
    t.type = 'FLOAT64'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

def p_s(p):
    '''
    s -> 
    '''

    
def p_error(p):
    print('SyntaxError')


parser = yacc.yacc()

