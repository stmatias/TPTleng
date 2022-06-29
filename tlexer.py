import ply.lex as lex

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

# Si se coloca arriba el lexer lo toma como un ID a los tipos 
def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = 'ID'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()