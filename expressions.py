from random import randint
from randomData import randomArray, randomString, randomFloat64, randomInt, randomBool

class Expr: 
    pass
 
class StructNode(Expr):
    def __init__(self,children=None, empty=False):
        self.type = "struct"
        self.children = children
        self.empty = empty

    def json(self):
        if self.empty:
            return ''
        else:
            lines = self.children[0]
            nextStruct= self.children[1]
            return '{' + '\n' + lines.json() + '\n' + '}' + '\n' + nextStruct.json()

class BasicExpression(Expr):
    def __init__(self,type):
        self.type = type
        self.leaf = True

    def json(self):
        return self.getSampleValue()

    def getSampleValue(self):
        if self.type == 'string':
            return randomString()
        elif self.type == 'int':
            return str(randomInt())
        elif self.type == 'float64':
            return str(randomFloat64())
        elif self.type == 'bool':
            return str(randomBool())
        else:
            raise Exception('Error de TIPO')

class LinesNode(Expr):
    def __init__(self,id='', children=None, empty=False):
        self.type = "lines"
        self.children = children
        self.id = id
        self.empty = empty

    def json(self):
        if self.empty:
            return ''
        else:
            if self.children[1].empty:
                return "\"" + self.id + "\": " + self.children[0].json()
            else:
                return "\"" + self.id + "\": " + self.children[0].json() + ",\n" + self.children[1].json()

class ARRAY():
    def __init__(self, type):
        self.type = type
        self.nesting = 0

    def jsonBoolString(self,array):
        if len(array) == 0:
            return '[]'
        if isinstance(array[0], list):
            acc = '['
            for i in range(len(array)):
                acc += self.jsonBoolString(array[i]) 
            acc += ']'
        else:
            acc = '[{}]'.format(', '.join(array))
        return acc

    def jsonListString(self,array):
        if len(array) == 0:
            return '[]'
        if isinstance(array[0], list):
            acc = '['
            for i in range(len(array)):
                acc += self.jsonListString(array[i]) 
            acc += ']'
        else:
            acc = '[%s]' % ', '.join(map(str, array))
        return acc

    def auxGetArray(self,type):
        if type=='string':
            return randomArray('string')
        elif type=='int':
            return randomArray('int')
        elif type=='float64':
            return randomArray('float64')
        elif type=='bool':
            return randomArray('bool')
    
    def getRecursiveArray(self):
        if self.type=='string':
            return self.jsonListString(self.auxGetRecursiveArray())
        elif self.type=='bool':
            return self.jsonBoolString(self.auxGetRecursiveArray())
        else:
            return str(self.auxGetRecursiveArray())

    def auxGetRecursiveArray(self):
        if self.nesting == 0:
            return self.auxGetArray(self.type) 
        else:
            self.decreaseNesting()
            return [self.auxGetRecursiveArray() for i in range(randint(0,5))]

    def decreaseNesting(self):
        self.nesting -= 1

    def increaseNesting(self):
        self.nesting += 1
    
    def getCounter(self):
        return self.nesting
    