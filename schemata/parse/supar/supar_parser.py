from supar import Parser
import sys
from schemata.parse.util import ConstituencyParserWrapper

class suPar(ConstituencyParserWrapper):
    def __init__(self, model = "crf-con-en"):
        super().__init__(Parser.load(model))

    def _run_base_parser(self, sent):
        dataset = self.base_parser.predict([sent.split()], verbose=False)
        tree = dataset.trees[0]
        return tree

if __name__ == '__main__':
    sentfile = sys.argv[1]
    outfile = sys.argv[2]
    parser = suPar()
    with open(sentfile) as reader:
        with open(outfile, 'w') as writer:
            for line in reader:
                line = line.strip()
                output = parser(line)
                writer.write(str(output))
                writer.write('\n')
