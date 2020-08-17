from supar import Parser
from schemata.parse.util import DependencyParserWrapper

class suParDependency(DependencyParserWrapper):
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
