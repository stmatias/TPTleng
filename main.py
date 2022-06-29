import sys
import ply.lex as lex
import ply.yacc as yacc

import sys

# s -> TYPE ID STRUCT L_BRCK t R_BRCK s | lambda.
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

def p_empty(p):
     'empty :'
     pass

def p_s(p):
    '''s : TYPE ID STRUCT L_BRCK t R_BRCK s 
        | empty
        ''' 
    if len(p) == 0:
        p[0] = []
    else:
        p[0] = () 

def p_s_anidado(p):
    's_anidado : STRUCT L_BRCK t R_BRCK'
    pass

def p_t(p):
    '''
    t : ID t1
    '''
    p[0] = p[1] + p[2]

def p_t1(p):
    '''
    t1 : s_anidado 
        | tipo 
        | array
    '''
    p[0] = p[1]

def p_tipo(p):
    '''
    tipo : STRING
        | INT 
        | FLOAT64 
        | BOOL 
    '''
    p[0] = p[1]

def p_array(p):
    '''
    array : ARRAY array1
    '''
    p[0] = p[1] + p[2]

def p_array1(p):
    '''
    array1 : tipo 
        | array
    '''
    p[0] = p[1]


def p_error(p):
    print('SyntaxError')

parser = yacc.yacc()

def readParse(str):
    out = parser.parse(str)
    print(out)
    #return out

if __name__ == "__main__":
    if(len(sys.argv)>1):
        readParse(sys.argv[1])