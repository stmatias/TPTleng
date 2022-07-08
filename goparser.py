import ply.yacc as yacc
from tlexer import *

from expressions import *

# PLY empieza con la primera produccion que se encuentra, ya que no definimos start

def p_s(p):
        '''s : struct '''
        p[1].sanitize()
        p[0] = indent(p[1].json())

def p_struct(p):
    '''struct : TYPE ID STRUCT L_BRCK lines R_BRCK struct 
        | empty
        '''    
    if len(p) == 2:
        # Todos los structs deben tener id en minimuscula
        p[0] = StructNode(id='EMPTY_STRUCT',empty=True, lineno = p.lineno(0)) # ''
    else:
        p[0] = StructNode(id=p[2],lines = p[5],nextStruct=p[7], lineno = p.lineno(0))    

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
    exp : struct_anidado 
        | tipo 
        | array
        | struct_sinDefinir
    '''
    p[0] = p[1]

def p_struct_sinDefinir(p):
    '''struct_sinDefinir : ID'''
    p[0] = StructNodeSinDefinir(p[1],lineno = p.lineno(0))

def p_struct_anidado(p):
    '''struct_anidado : STRUCT L_BRCK lines R_BRCK'''
    p[0] = StructAnidadoNode(id=p[-1],lines=p[3],lineno = p.lineno(0))

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
    if p[1] in ['string','int','float64','bool']:
        p[0] = ArrayExpression(p[1])
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
    # print(str)
    # Agregar error todos los identificadores deben comenzar por una letra min´uscula.
    # Levantar excepciones sin no 
    out = parser.parse(str, tracking=True)
    return out
