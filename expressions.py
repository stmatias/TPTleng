from random import randint
from randomData import randomArray, randomString, randomFloat64, randomInt, randomBool

class Node:
    def __init__(self,type,children=None,leaf=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf
    
    def getDependencies(self):
        map = {}
        if self.leaf:
            map[self.type] = self.leaf
        else:      
            for child in self.children:
                if child.isLeaf():
                    map[child.type] = child.leaf
                else:
                    map[child.type] = child.getDependencies()
        return map 

    def isLeaf(self):
        return self.leaf != None

    def constructJsonFromAST():
        map = self.map
        '{} '

""" class Root(Node):
    def __init__(self,children):
        self.type = 'Root'
        self.children = children
        self.map = {}   

    def checkDependencies(self):
        for child in self.children:
            if child.type == "ID":
                self.map[child.value()] = child.getID()
            else:
                self.map[child.type()] = child.getDependencies()
        return self.map

class IDNode(Node):
    def __init__(self, leaf=None):
        self.type = "ID"
        self.leaf = leaf
    
    def value(self):
        return self.leaf """

class BasicTypeExpression(Node):
    def __init__(self, children=None,leaf=None):
        self.type = "tipo"
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf
        self.type = type 	

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
    