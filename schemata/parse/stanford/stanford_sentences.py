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

def get_sents(file):
    # takes a txt file and returns a string of sentences
    with open(file, 'r') as in_file:
        all_lines = in_file.readlines()
        result = ""
        for line in all_lines:
            result.append(line.strip() + " ")
    return result
        
            
class StanfordParser(DependencyParserWrapper):
    def __call__(self, file):
        sents = get_sents(file)
        return self.get_spans(sents)

    def get_spans(self, sents):
        # returns a list of spans
        with CoreNLPClient() as client:
            ann = client.annotate(sents, annotators='parse', output_format='json')
            
        result = []
        for num in range(200):
            dependencies_list = ann['sentences'][num]['basicDependencies']
            heads = get_heads(dependencies_list)
            tree = DependencyParserWrapper.head_to_tree(heads)
            non_singletons = DependencyParserWrapper.compute_spans(tree)
            singletons = [(n, n + 1) for n in range(len(dependencies_list))]
            spans = set(non_singletons) | set(singletons)
            result.append(spans)
        return result
