import spacy
from schemata.parse.util import DependencyParserWrapper

def get_tree_dict(doc):
    result = []
    for token in doc:
        if token.dep_ == "ROOT":
            result.append({"governor": 0, "dependent": token.i+1})
        children = [child for child in token.children]
        for child in children:
          one_dict = {}
          one_dict["governor"] = child.head.i + 1
          one_dict["dependent"] = child.i + 1
          result.append(one_dict)
    ls = sorted([(item['dependent'], item['governor']) for item in result])
    ls = [x[1] for x in ls]
    return ls

class SpacyParser(DependencyParserWrapper):
    def __init__(self, model = "en_core_web_lg"):
        super().__init__()
        self.parser = spacy.load(model)

    def __call__(self, sent):
        return self.get_spans(sent)
        
    def get_spans(self, sent):
        doc = self.parser(sent)
        heads = get_tree_dict(doc)
        tree = DependencyParserWrapper.head_to_tree(heads)
        non_singletons = DependencyParserWrapper.compute_spans(tree)
        singletons = [(n, n+1) for n in range(len(heads))]
        return set(non_singletons) | set(singletons)

