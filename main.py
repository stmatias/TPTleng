import sys
import argparse

from goparser import readParse

# s -> TYPE ID STRUCT L_BRCK t R_BRCK s | lambda.
# s_anidado -> STRUCT L_BRCK t R_BRCK.
# t -> ID t'
# t' -> s_anidado | tipo | array
# tipo -> STRING| INT |FLOAT64 | BOOL.
# array -> ARRAY array'.
# array' -> tipo | array.

if __name__ == "__main__":

    
    msg = "Parser para structs de Go a JSON"
 
    # Initialize parser
    argparser = argparse.ArgumentParser(description = msg)
    group = argparser.add_mutually_exclusive_group()

    group.add_argument(
        '-f', '--file',
        help='Go input file',
        type=argparse.FileType('r'),
    )

    group.add_argument(
        '-t', '--text',
        help="input text to parse",
        type=str
    )

    args = argparser.parse_args()
    
    if args.file:
        text = '\n'.join(args.file.readlines())
        json = readParse(text)
    elif args.text:
        json = readParse(args.text)    
    else: 
        print("No input file or text")
        argparser.print_usage()
        sys.exit(1)

    print(json)  