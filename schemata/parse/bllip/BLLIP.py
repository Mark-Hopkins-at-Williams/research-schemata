import bllipparser
import sys
from bllipparser import RerankingParser
from schemata.parse.util import ConstituencyParserWrapper

class BLLIP(ConstituencyParserWrapper):
    def __init__(self, model = "WSJ-PTB3"):
        super().__init__(RerankingParser.fetch_and_load(model, verbose=True))
                         
    def _run_base_parser(self, sent):
        intermediate = self.base_parser.parse(sent)
        tree = intermediate.fuse().as_nltk_tree()
        return tree


if __name__ == '__main__':
    sentfile = sys.argv[1]
    outfile = sys.argv[2]
    parser = BLLIP()
    with open(sentfile) as reader:
        with open(outfile, 'w') as writer:
            for line in reader:
                line = line.strip()
                output = parser(line)
                writer.write(str(output))
                writer.write('\n')
