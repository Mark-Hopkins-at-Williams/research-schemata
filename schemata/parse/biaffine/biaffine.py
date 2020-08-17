from allennlp.predictors.predictor import Predictor
from schemata.parse.util import DependencyParserWrapper

class BiaffineParser(DependencyParserWrapper):
    def __init__(self):
        super().__init__()
        self.parser = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/biaffine-dependency-parser-ptb-2020.04.06.tar.gz")
        
    def get_spans(self, sent):
        json_parse = self.parser.predict(sentence=sent)
        heads = json_parse['predicted_heads']
        tree = DependencyParserWrapper.head_to_tree(heads)
        non_singletons = DependencyParserWrapper.compute_spans(tree)
        singletons = [(n,n+1) for n in range(len(heads))]
        return set(non_singletons) | set(singletons)
