import ply.yacc as yacc
from tlexer import *

from expressions import *

start = 'sSanitazadora'

structs_conocidas = {}
structs_no_conocidas = {}

# no haya interseccion entre conocidas y no conocidas. 
# y que no agregamos una dos veces dict[key] = value, revisar que key no pertenece antes de agregar a conocidas

def p_sSanitizadora(p):
        '''sSanitazadora : s '''
        #p[1].revisarDependenciasCirculares()        
        #p[1] es un NodoStruct
        p[0] = p[1].json() # sanitizar(p[1])


def p_s(p):
    '''s : TYPE ID STRUCT L_BRCK lines R_BRCK s 
        | empty
        '''    
    
    if len(p) == 2:
        p[0] = StructNode(empty=True) # ''
    else:
        lines = p[5]
        nextStruct = p[7]
        p[0] = StructNode([lines,nextStruct])    


def p_lines(p):
    '''
    lines : ID exp lines
      | empty
    '''
    if len(p) == 2:
        p[0] = LinesNode(empty=True)
    else:
        p[0] = LinesNode(p[1],[p[2], p[3]])


def p_exp(p):
    '''
    exp : s_anidado 
        | tipo 
        | array
        | s_sinDefinir
    '''
    p[0] = p[1]


def p_s_sinDefinir(p):
    '''s_sinDefinir : ID'''
    if p[1] in structs_conocidas.keys():
        raise Exception('Error de dependencias circulares')
    structs_no_conocidas[p[1]] = p[1]
    p[0] = p[1]


def p_s_anidado(p):
    '''s_anidado : STRUCT L_BRCK lines R_BRCK'''
    lb = p[2]
    rb = p[4]
    lines = p[3]
    p[0] = lb + '\n' + lines + '\n' + rb 

def p_tipo(p):
    '''
    tipo : STRING
        | INT 
        | FLOAT64 
        | BOOL 
    '''
    p[0] = BasicExpression(p[1])


def p_array(p):
    '''
    array : ARRAY array1
    '''
    p[0] = p[2]

def p_array1(p):
    '''
    array1 : STRING
        | INT 
        | FLOAT64 
        | BOOL 
        | array
    '''
    if p[1]=='string' or p[1]=='int'or p[1]=='float64'or p[1]=='bool':
        p[0] = ARRAY(p[1])
    else: 
        p[1].increaseNesting()
        p[0] = p[1]
    

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
    # Agregar error todos los identificadores deben comenzar por una letra min´uscula.
    # Dependencias definidas (por ejemplo cuando re uso un struct)
    # Levantar excepciones sin no 
    out = parser.parse(str)
    return out