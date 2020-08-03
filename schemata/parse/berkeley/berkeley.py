import benepar
import sys
from schemata.parse.util import ConstituencyParserWrapper

class BerkeleyParser(ConstituencyParserWrapper):
    def __init__(self, model = "benepar_en2"):
        super().__init__(benepar.Parser(model))

    def _run_base_parser(self, sent):
        tree = self.base_parser.parse(sent)
        return tree

if __name__ == '__main__':
    sentfile = sys.argv[1]
    outfile = sys.argv[2]
    parser = BerkeleyParser()
    with open(sentfile) as reader:
        with open(outfile, 'w') as writer:
            for line in reader:
                line = line.strip()
                output = parser(line)
                writer.write(str(output))
                writer.write('\n')
        
    