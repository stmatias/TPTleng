from random import randint
from randomData import randomArray, randomString, randomFloat64, randomInt, randomBool

from randomData import randomString, randomFloat64, randomInt, randomBool
from expressions import *

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
    