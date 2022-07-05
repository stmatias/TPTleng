import os, glob
import json

from goparser import readParse

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

path = 'tests_grupo'

for filename in glob.glob(os.path.join(path, '*.go')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        print(filename)
        text = ''.join(f.readlines())
        myjson = readParse(text)
        print(is_json(myjson))
        if not is_json(myjson) and not filename.startswith('ERROR'):
            print(myjson)
        if is_json(myjson) and filename.startswith('ERROR'):
            print('ESPERABAMOS ERROR')