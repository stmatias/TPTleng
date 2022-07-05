from logging import root
from random import randint
from randomData import randomArray, randomString, randomFloat64, randomInt, randomBool


class Expr:
    pass


structs_no_definidos = {}
structs_definidos = {}


class StructNode(Expr):
    def __init__(self, id, lines=None, nextStruct=None, empty=False, lineno=None):
        self.type = "struct"
        self.lines = lines
        self.nextStruct = nextStruct
        self.empty = empty
        self.id = id
        self.lineno = lineno

        if self.empty:
            assert(self.lines is None)
            assert(self.nextStruct is None)
        else:
            assert(self.lines is not None)
            assert(self.nextStruct is not None)
            structs_definidos[self.id] = self

    def sanitize(self):
        self.checkRedefinition()
        self.checkCircularDependency()

    def checkRedefinition(self):
        if not self.empty:
            knownStructs = [self.id]
            self.nextStruct.checkRedefinitionAux(knownStructs)

    def checkRedefinitionAux(self, knownStructs):
        for st in knownStructs:
            if st == self.id:
                print(
                    f'Error, otra declaracion de: {self.id} en la linea {self.lineno}')
                raise SyntaxError
        knownStructs.append(self.id)

    def checkCircularDependency(self):
        if not self.empty:
            knownStructs = [self.id]
            self.lines.checkCircularDependencyAux(knownStructs)

    def checkCircularDependencyAux(self, knownStructs):
        for st in knownStructs:
            if st == self.id:
                print(
                    f'Error, dependencia circular de: {self.id} en la linea {self.lineno}')
                raise SyntaxError
        knownStructs.append(self.id)
        if not self.empty:
            self.lines.checkCircularDependencyAux(knownStructs)

    def json(self):
        if self.empty or self.id in structs_no_definidos.keys():
            return ''
        else:
            # Solo Imprime el tipo principal, descomentar para imprimir el sig struct
            return '{' + '\n' + self.lines.json() + '\n' + '}' + '\n' #+ self.nextStruct.json()

    def jsonForce(self):
        return '{' + '\n' + self.lines.json() + '\n' + '}' + self.nextStruct.json()


class StructNodeSinDefinir(StructNode):
    def __init__(self, id, lines=None, nextStruct=None, lineno=None):
        self.lines = lines
        self.nextStruct = nextStruct
        self.id = id
        self.lineno = lineno
        self.empty = True

        assert(self.lines is None)
        assert(self.nextStruct is None)
        structs_no_definidos[self.id] = self

    def checkCircularDependencyAux(self, knownStructs):
        if self.id in structs_definidos.keys():
            structs_definidos[self.id].checkCircularDependencyAux(knownStructs)
        else:
            print(f'Error, tipo no definido para: {self.id} en la linea {self.lineno}')
            raise SyntaxError

    def json(self):
        return structs_definidos[self.id].jsonForce()


class StructAnidadoNode(StructNode):

    def __init__(self, id, lines=None, empty=False, lineno=None):
        self.lines = lines
        self.empty = empty
        self.id = id
        self.lineno = lineno

        if self.empty:
            assert(self.lines is None)
        else:
            assert(self.lines is not None)

    def json(self):
        return '{' + '\n' + self.lines.json() + '\n' + '}'

    def checkCircularDependencyAux(self, knownStructs):
        for st in knownStructs:
            if st == self.id:
                print(
                    f'Error, dependencia circular de: {self.id} en la linea {self.lineno}')
                raise SyntaxError
        if not self.empty:
            self.lines.checkCircularDependencyAux(knownStructs)


class BasicExpression(Expr):
    def __init__(self, type):
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

    def checkCircularDependencyAux(self, knownStructs):
        pass


class LinesNode(Expr):
    def __init__(self, id='', children=None, empty=False):
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

    def checkCircularDependencyAux(self, knownStructs):
        if not self.empty:
            for child in self.children:
                child.checkCircularDependencyAux(knownStructs)


class ArrayExpression(Expr):
    def __init__(self, type):
        self.type = type
        self.leaf = True
        self.nesting = 0
        self.definido = True

    def checkCircularDependencyAux(self, knownStructs):
        pass

    def jsonBoolString(self, array):
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

    def jsonListString(self, array):
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

    def auxGetArray(self, type):
        if type == 'string':
            return randomArray('string')
        elif type == 'int':
            return randomArray('int')
        elif type == 'float64':
            return randomArray('float64')
        elif type == 'bool':
            return randomArray('bool')

    def json(self):
        return self.getRecursiveArray()

    def getRecursiveArray(self):
        if self.type == 'string':
            return self.jsonListString(self.auxGetRecursiveArray())
        elif self.type == 'bool':
            return self.jsonBoolString(self.auxGetRecursiveArray())
        else:
            return str(self.auxGetRecursiveArray())

    def auxGetRecursiveArray(self):
        if self.nesting == 0:
            return self.auxGetArray(self.type)
        else:
            self.decreaseNesting()
            return [self.auxGetRecursiveArray() for i in range(randint(0, 5))]

    def decreaseNesting(self):
        self.nesting -= 1

    def increaseNesting(self):
        self.nesting += 1

    def getCounter(self):
        return self.nesting

def indent(text):
    return text