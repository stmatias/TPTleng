import random
import string 

def randomString():
    letters = string.ascii_lowercase
    vowels = "aeiou"
    return "".join(random.choice((letters, vowels)[i%2]) for i in range(random.randint(0, 10)))

def randomInt():
    return random.randint(0, 1000)

def randomBool():
    return random.choice(['true', 'false'])

def randomFloat64():
    return random.uniform(0, 10)

def randomArray(type):
    return [randomType(type) for i in range(random.randint(0, 5))]

def randomType(type):
    if type == 'int':
        return randomInt()
    if type == 'string':
        return randomString() 
    if type == 'bool':
        return randomBool() 
    if type == 'float64':
        return randomFloat64() 
    else:
        raise Exception("Tipo Invalido")