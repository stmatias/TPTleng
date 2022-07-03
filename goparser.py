from random import randint
import ply.yacc as yacc
from tlexer import *

from randomData import randomString, randomFloat64, randomInt, randomBool
from expressions import ARRAY

start = 'sSanitazadora'

structs_conocidas = {}
structs_no_conocidas = {}

# no haya interseccion entre conocidas y no conocidas. 
# y que no agregamos una dos veces dict[key] = value, revisar que key no pertenece antes de agregar a conocidas




def reemplazarConocidas(cadena):
    for key in structs_no_conocidas.keys():
        cadena = cadena.replace(key, structs_no_conocidas[key])
    return cadena

def hayDependenciaCircular():
    return structs_conocidas.keys() & structs_no_conocidas.keys()


def revisarDependenciasCirculares():
    if hayDependenciaCircular():
        raise Exception('Error de dependencias circulares')    

def p_sSanitizadora(p):
        '''sSanitazadora : s '''
        revisarDependenciasCirculares()        
        p[0] = reemplazarConocidas(p[1])# sanitizar(p[1])

        print('Conocidas: ',structs_conocidas)
        print('No conocidas: ',structs_no_conocidas)
        """ Revisa por dependencias circulares, tipos definidos mas de una vez
        {
        "nombre": "qeoexedu",
        "edad": 535,
        "nacionalidad": pais,
        "ventas": [],
        "activo": true
        } donde pais va a estar en una estrcutura guardada y lo reemplazamos 
        """ 


def p_s(p):
    '''s : TYPE ID STRUCT L_BRCK t R_BRCK s 
        | empty
        '''    
    
    if len(p) == 2:
        p[0] = ''

# pais {nacionalidad pais}

# hijos pais : pais ERROR 

# persona {nacionalidad pais}

#pais {}

    elif p[2] in structs_no_conocidas.keys():
        lb = p[4]
        rb = p[6]
        lines = p[5]
        structs_no_conocidas[p[2]] = lb + '\n' + lines + '\n' + rb + '\n' + p[7]
        p[0]= ''
    else:
        lb = p[4]
        rb = p[6]
        lines = p[5]
        p[0] = lb + '\n' + lines + '\n' + rb + '\n' + p[7]
        if (p[2] in structs_conocidas.keys()):
            raise Exception('Error de dependencias struct redefinido')
        structs_conocidas[p[2]] = p[0]

        


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
        | s_sinDefinir
    '''
    if isinstance(p[1], ARRAY):
        p[0] = p[1].getRecursiveArray()
    else: 
        p[0] = p[1]
        # Agregamos pais a un dict, para luego en el json final reemplazar pais por el strcut de pais y ademas, 
        # cuando leamos un pais mas adelante, no lo imprimimos
        # 

def p_s_sinDefinir(p):
    '''s_sinDefinir : ID'''
    if p[1] in structs_conocidas.keys():
        raise Exception('Error de dependencias circulares')
    structs_no_conocidas[p[1]] = p[1]
    p[0] = p[1]


def p_s_anidado(p):
    '''s_anidado : STRUCT L_BRCK t R_BRCK'''
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