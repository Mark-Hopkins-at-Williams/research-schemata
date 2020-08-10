from nltk.parse.malt import MaltParser
import sys
from schemata.parse.util import ConstituencyParserWrapper

class MaltParser(ConstituencyParserWrapper):
    def __init__(self, version = "maltparser-1.9.2", model = "engmalt.linear-1.7.mco"):
        super().__init__(MaltParser(version, model))

    def _run_base_parser(self, sent):
        tree = self.base.parse_one(sent.split()).tree()
        return tree

if __name__ == '__main__':
    sentfile = sys.argv[1]
    outfile = sys.argv[2]
    parser = MaltParser()
    with open(sentfile) as reader:
        with open(outfile, 'w') as writer:
            for line in reader:
                line = line.strip()
                output = parser(line)
                writer.write(str(output))
                writer.write('\n')
