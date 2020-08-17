from nltk.parse.malt import MaltParser as MP
import sys
from schemata.parse.util import DependencyParserWrapper

class MaltParser(DependencyParserWrapper):
    # currently this can only be run from the malt parser directory
    # TODO: make more general/easy to run
    def __init__(self, version = "maltparser-1.9.2", model = "engmalt.linear-1.7.mco"):
        super().__init__()
        self.base = MP(version, model)

    def get_spans(self, sent):
        dparse = self.base.parse_one(sent.split())
        heads = [node['head'] for _, node in sorted(dparse.nodes.items())][1:]
        tree = DependencyParserWrapper.head_to_tree(heads)
        non_singletons = DependencyParserWrapper.compute_spans(tree)
        singletons = [(n,n+1) for n in range(len(heads))]
        return set(non_singletons) | set(singletons)

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
