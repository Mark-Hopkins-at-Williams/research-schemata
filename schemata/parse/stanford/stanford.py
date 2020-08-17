from stanza.server import CoreNLPClient
from schemata.parse.util import DependencyParserWrapper

#IN TERMINAL:
#export CORENLP_HOME=/path/to/stanford-corenlp-4.1.0
#export CORENLP_HOME=/Users/hongly3j/reed-nlp/research-schemata/schemata/parse/stanford/stanford-corenlp-4.1.0

def get_heads(dicts):
    # takes a list of dictionaries with heads and descendants and creates one dictionary with
    # heads and descendants
    ls = sorted([(item['dependent'], item['governor']) for item in dicts])
    ls = [x[1] for x in ls]
    return ls

class StanfordParser(DependencyParserWrapper):
    def __call__(self, sent):
        return self.get_spans(sent)

    def get_spans(self, sent):
        with CoreNLPClient() as client:
            ann = client.annotate(sent, annotators='parse', output_format='json')
        dependencies_list = ann['sentences'][0]['basicDependencies']
        heads = get_heads(dependencies_list)
        tree = DependencyParserWrapper.head_to_tree(heads)
        non_singletons = DependencyParserWrapper.compute_spans(tree)
        singletons = [(n, n + 1) for n in range(len(dependencies_list))]
        return set(non_singletons) | set(singletons)
