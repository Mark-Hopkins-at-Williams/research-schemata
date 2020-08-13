from stanza.server import CoreNLPClient

#IN TERMINAL:
#export CORENLP_HOME=/Users/hongly3j/reed-nlp/research-schemata/schemata/parse/stanford/stanford-corenlp-4.1.0

#example = "Chris Manning is a nice person. Chris wrote a simple sentence. He also gives oranges to people"


def head_to_tree(dicts):
    def fill_tree(one_dict, dicts):
        # fills tree with missing keys
        current = {}
        for n in range(len(dicts) + 1):
            if one_dict.get(n, None) == None:
                current[n] = []
            else:
                current[n] = one_dict[n]
        current[len(dicts)] = []  # create extra key:value pair
        return current
    
    # takes a list of dictionaries with heads and descendants and creates one dictionary with
    # heads and descendants
    tree_dict = {}
    for one_dict in dicts:
        head = one_dict["governor"]  # get  heads
        child = one_dict["dependent"]  # get descendent of head
        tree_dict[head] = tree_dict.get(head, []) + [child]

    # fill tree with missing key/value pairs
    tree_dict = fill_tree(tree_dict, dicts)
    return tree_dict

def descendents(tree, i):
    # takes a dictionary and an index i and returns all descendents of the key at i
    if tree[i] == []:
        return [i]
    else:
        desc = [i]
        for c in tree[i]:
            desc += (descendents(tree, c))
        return desc

def get_spans(tree):
    # takes a dictionary and returns a list of lists representing
    # constituents
    spans = []
    for i in tree:
        desc = descendents(tree, i)
        # we ignore one-word constituents
        if len(desc) > 1 and len(desc) < len(tree):
            spans.append((min(desc) - 1, max(desc)))
    return spans

class StanfordParser:
    def __call__(self, sent):
        return self.get_spans(sent)

    def get_spans(self, sent):
        with CoreNLPClient() as client:
            ann = client.annotate(sent, annotators='parse', output_format='json')
        dependencies_list = ann['sentences'][0]['basicDependencies']
        tree = head_to_tree(dependencies_list)
        non_singletons = get_spans(tree)
        singletons = [(n, n + 1) for n in range(len(dependencies_list))]
        return set(non_singletons) | set(singletons)


#DEMO OF STANFORD PARSER
text = "I saw the dog with dark fur ."
with CoreNLPClient() as client:
    ann = client.annotate(text, annotators='parse', output_format='json')

dependencies_list = ann['sentences'][0]['basicDependencies']
#print(dependencies_list)  # see dictionary input

tree = head_to_tree(dependencies_list)
print(tree)

spans = get_spans(tree)
print(spans)
