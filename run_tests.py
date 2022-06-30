import os, glob

from goparser import readParse
path = 'tests_grupo'
print('a')
for filename in glob.glob(os.path.join(path, '*.go')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        print(filename)
        text = ''.join(f.readlines())
        json = readParse(text)
        print(json)