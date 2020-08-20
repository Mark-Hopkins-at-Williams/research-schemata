from nltk.parse.malt import MaltParser as MP
from schemata.parse.util import DependencyParserWrapper
import sys
import os

class MaltParser(DependencyParserWrapper):
    # currently this can only be run from the malt parser directory
    # TODO: make more general/easy to run
    def __init__(self, version = "maltparser-1.9.2", model = "engmalt.linear-1.7.mco"):
        super().__init__()
        root = os.getcwd()
        version_path = os.path.join(root, "schemata", "parse", "maltparser", version )
        model_path =os.path.join(root, "schemata", "parse", "maltparser", model )
        self.base = MP(version_path, model_path)

    def get_spans(self, sent):
        dparse = self.base.parse_one(sent.split())
        heads = [node['head'] for _, node in sorted(dparse.nodes.items())][1:]
        tree = DependencyParserWrapper.head_to_tree(heads)
        non_singletons = DependencyParserWrapper.compute_spans(tree)
        singletons = [(n, n+1) for n in range(len(heads))]
        return set(non_singletons) | set(singletons)

