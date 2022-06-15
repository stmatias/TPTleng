import ply.lex as lex
import ply.yacc as yacc



# VT = {STRING, INT, FLOAT64, BOOL, RBRACKET, LBRACKET, ARRAY}
tokens = ['TYPE','ID','STRING', 'INT', 'FLOAT64', 'BOOL', 'RBRACKET', 'LBRACKET', 'ARRAY' ]

#VN = {S, }


t_L_BRCK = r'{'
t_R_BRCK = r'}'
t_ARRAY = r'\[\]'

t_ignore = ' \t\n'

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


def p_attributes(p):
    '''
    attributes : attribute attributes 
               | empty
    '''
    if len(p) == 2: 
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_attribute(p):
    '''
    attribute : ID ID
    '''
    if p[2] not in ['string', 'float', 'int']:
        p_error(p)
        raise SyntaxError
    else:
        p[0] = ' ' + p[1] + ' ' + p[2]

def p_array(p):
    '''
    array : ARRAY
          | empty
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = ''
    
def p_error(p):
    print('SyntaxError')


parser = yacc.yacc()











parser = yacc.yacc()
