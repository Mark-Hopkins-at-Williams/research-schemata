import os
import sys

def run_one_file(file, parser, run_file="run_parser.py"):
    # run test on one file
    print("------------ " + parser + " running " + file + " ------------")
    os.system("python " + run_file + " ../../../data/" + file)
    
def run_schema(root, parser, run_file="run_parser.py"):
    # run all tests for one parser
    files = ["julieschema.txt", "myschema.txt", "pp1.asc"]
    new_path = os.path.join(root, "schemata/parse", parser)
    os.chdir(new_path)
    for file in files:
        run_one_file(file, parser, run_file)
        
def run_parsers():
    # run tests for all parsers
    root = os.getcwd()
    parsers = ["berkeley", "biaffine", "bllip", "maltparser", "spacy", "stanford", "supar", "supar_dep"]
    
    for parser in parsers:
        run_schema(root, parser, run_file="run_parser.py")
        if parser == "supar":
            run_schema(root, parser, "run_dep_parser.py")
    os.chdir(root)

if __name__ == '__main__':
    root = os.getcwd()
    # run tests for specific parser
    if len(sys.argv) == 2:
        parser = sys.argv[1]
        if parser == "supar_dep":
            run_schema(root, parser, "run_dep_parser.py")
        else:
            run_schema(root, parser)
            
    # run tests for specific parser and file
    elif len(sys.argv) > 2:
        parser = sys.argv[1]
        file = sys.argv[2]
        if parser == "supar_dep":
            # checking for special case supar_dep
            new_path = os.path.join(root, "schemata/parse", "supar")
            os.chdir(new_path)
            run_one_file(file, parser, "run_dep_parser.py")
        else:
            new_path = os.path.join(root, "schemata/parse", parser)
            os.chdir(new_path)
            run_one_file(file, parser)
    
    # run tests for all parsers
    else:
        run_parsers()
    os.chdir(root)
