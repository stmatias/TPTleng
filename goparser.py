import ply.yacc as yacc
from tlexer import tokens

from randomData import randomArray, randomString, randomFloat64, randomInt, randomBool


start = 's'

def p_s(p):
    '''s : TYPE ID STRUCT L_BRCK t R_BRCK s 
        | empty
        '''    
    if len(p) == 2:
        p[0] = ''
    else:
        lb = p[4]
        rb = p[6]
        # por ahora no se como usar p[1] + p[2] + p[3]
        lines = p[5]
        p[0] = lb + '\n' + lines + '\n' + rb + '\n' #+ p[7]

def p_s_anidado(p):
    's_anidado : STRUCT L_BRCK t R_BRCK'
    pass

def p_t(p):
    '''
    t : ID t1 t
      | empty
    '''
    if len(p) == 2:
        p[0] = ''
    else:
        if p[3] == '':
            p[0] = "\"" + p[1] + "\": " + p[2]
        else:
            p[0] = "\"" + p[1] + "\": " + p[2] + ",\n" + p[3]

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
    if p[1]=='string':
        p[0] = randomString()
    elif p[1]=='int':
        p[0] = str(randomInt())
    elif p[1]=='float64':
        p[0] = str(randomFloat64())
    elif p[1]=='bool':
        p[0] = str(randomBool())
    else:
        raise Exception('Error de TIPO')


def p_array(p):
    '''
    array : ARRAY array1
    '''
    #p[0] = p[1] + p[2]
    p[0] = p[2]

def p_array1(p):
    '''
    array1 : tipo 
        | array
    '''
    if p[1]=='string':
        p[0] = randomArray('string')
    elif p[1]=='int':
        p[0] = randomArray('int')
    elif p[1]=='float64':
        p[0] = randomArray('float64')
    elif p[1]=='bool':
        p[0] = randomArray('bool')
    else: 
        p[0] = [p[1]]
    
    #p[0] = p[1]

def p_empty(p):
     'empty :'
     pass

def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")

        # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.state,
                  stack_state_str,
                  p))

parser = yacc.yacc()

def readParse(str):
    # Chequear dependencias circulares
    # Todos los identificadores deben comenzar por una letra min´uscula.
    # Dependencias definidas (por ejemplo cuando re uso un struct)
    # Levantar excepciones sin no 
    out = parser.parse(str)
    return out