from allennlp.predictors.predictor import Predictor

def head_to_tree(heads):
    # takes a list of dependency heads and returns each head's children as a dictionary
    children = {}
    for i in range(0,len(heads)+1):
        children[i] = []
    for j in range(0,len(heads)):
        children[heads[j]].append(j+1)
    return children
            
def descendents(tree,i):
    # takes a dictionary and an index i and returns all descendents of the key at i
    if tree[i] == []:
        return [i]
    else:
        desc = [i]
        for c in tree[i]:
            desc+=(descendents(tree,c))
        return desc
    
def get_spans(tree):
    # takes a dictionary and returns a list of lists representing
    # constituents
    spans = []
    for i in tree:
        desc = descendents(tree,i)
        # we ignore one-word constituents
        if len(desc) > 1 and len(desc) < len(tree):
            spans.append([min(desc)-1,max(desc)])
    return spans
          

class BiaffineParser:
    def __init__(self):
        self.parser = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/biaffine-dependency-parser-ptb-2020.04.06.tar.gz")

    def __call__(self, sent):
        return self.get_spans(sent)
        
    def get_spans(self, sent):
        json_parse = self.parser.predict(sentence=sent)
        heads = json_parse['predicted_heads']
        return heads # This gives the head word of each token.
        # TODO: convert these heads into a list of the constituent spans.
        # see test_biaffine.py to look at an example input/output.
