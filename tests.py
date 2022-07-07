import sys, os, glob, json

from goparser import readParse

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

def run_tests(with_error):
  path = 'tests'
  quantity_ok = 0
  quantity_analyzed = 0

  for filename in glob.glob(os.path.join(path, '*.go')):
      with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode

        if with_error and not 'ERROR' in filename:
          continue
        
        if not with_error and 'ERROR' in filename:
          continue

        print(filename);
        test = ''.join(f.readlines());
        myjson = readParse(test);
        # print(is_json(myjson));
        # print(myjson);

        if not filename.startswith('tests/ERROR') and not is_json(myjson):
            print('-- ERROR --\n\n');
        elif is_json(myjson) and filename.startswith('tests/ERROR'):
            print('-- ERROR --\n\n');
        else:
            quantity_ok += 1
            print('-- OK --\n\n');

        quantity_analyzed += 1

        f.close()
      
  print('Tests correctos: ' + str(quantity_ok) + ' de ' + str(quantity_analyzed))
            