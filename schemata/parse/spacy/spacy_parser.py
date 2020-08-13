import spacy

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
    return result

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
            spans.append((min(desc)-1,max(desc)))
    return spans
          

class SpacyParser:
    def __init__(self):
        self.parser = spacy.load("en_core_web_lg")

    def __call__(self, sent):
        return self.get_spans(sent)
        
    def get_spans(self, sent):
        doc = self.parser(sentence=sent)
        heads = get_tree_dict(doc)
        tree = head_to_tree(heads)
        non_singletons = get_spans(tree)
        singletons = [(n, n+1) for n in range(len(heads))]
        return set(non_singletons) | set(singletons)

#DEMO
text = "The dog eats good food ."
nlp = spacy.load("en_core_web_lg")
doc = nlp(text)
heads = get_tree_dict(doc)
tree = head_to_tree(heads)
non_singletons = get_spans(tree)
print(non_singletons)
singletons = [(n, n+1) for n in range(len(heads))]
print(set(non_singletons) | set(singletons))
