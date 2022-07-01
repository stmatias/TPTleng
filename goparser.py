from platform import node
from random import randint
import ply.yacc as yacc
from tlexer import *

from randomData import randomString, randomFloat64, randomInt, randomBool
from expressions import ARRAY, Node, BasicTypeExpression

start = 's'

def p_s(p):
    '''s : TYPE ID STRUCT L_BRCK t R_BRCK s 
        | empty
        '''    
    if len(p) == 2:
        p[0] = p[1]
    else:
        lb = p[4]
        rb = p[6]
        id = Node("structID",leaf=p[2]) 
        lines = p[5]
        p[0] =  Node("s", [id, p[5],p[7]]) 
        print(p[0].getDependencies())
        #print(lb + '\n' + lines + '\n' + rb + '\n' + p[7])


def p_t(p):
    '''
    t : ID t1 t
      | empty
    '''
    if len(p) == 2:
        p[0] = ''
    else:
        id = Node("ID",leaf=p[1]) 
        p[0] = Node("t", [id,p[2]]) 
"""         if p[3] == '':
            p[0] = "\"" + p[1] + "\": " + p[2]
        else:
            p[0] = "\"" + p[1] + "\": " + p[2] + ",\n" + p[3] """

def p_t1(p):
    '''
    t1 : s_anidado 
        | tipo 
        | array
    '''
    if isinstance(p[1], ARRAY):
        p[0] = p[1].getRecursiveArray()
    else: 
        p[0] = Node("t1", [p[1]]) 

def p_s_anidado(p):
    's_anidado : STRUCT L_BRCK t R_BRCK'
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
    p[0] = Node("tipo", leaf=p[1])


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
    p[0] = Node("empty")

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