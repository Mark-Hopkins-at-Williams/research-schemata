from supar import Parser
import sys
from schemata.parse.util import ConstituencyParserWrapper
from schemata.parse.util import DependencyParserWrapper

class SuPar(ConstituencyParserWrapper):
    def __init__(self, model = "crf-con-en"):
        super().__init__(Parser.load(model))

    def _run_base_parser(self, sent):
        dataset = self.base_parser.predict([sent.split()], verbose=False)
        tree = dataset.trees[0]
        return tree

class SuParDependency(DependencyParserWrapper):
    def __init__(self):
        super().__init__()
        self.parser = Parser.load("crf2o-dep-en")

    def __call__(self, sent):
        return self.get_spans(sent)
        
    def get_spans(self, sent):
        parse = self.parser.predict([sent.split()], prob=True, verbose=False)
        heads = parse.arcs[0]
        tree = DependencyParserWrapper.head_to_tree(heads)
        non_singletons = DependencyParserWrapper.compute_spans(tree)
        singletons = [(n,n+1) for n in range(len(heads))]
        return set(non_singletons) | set(singletons)

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
