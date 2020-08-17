
class ConstituencyParserWrapper:
    def __init__(self, base_parser):
        self.base_parser = base_parser

    def __call__(self, sent):
        return self.get_spans(sent)

    def _run_base_parser(self, sent):
        raise NotImplementedError("Cannot call ._run_base_parser on abstract class.")        

    def get_spans(self, sent):
        def get_spans_helper(treepositions, start_index):
            children = sorted([position for position in treepositions
                               if len(position) == 1])
            if len(children) == 0:
                return [(start_index, start_index+1)]
            result = []
            orig_start_index = start_index
            for child in children:
                descendants = [position[1:] for position in treepositions
                               if len(position) > 0 and position[0] == child[0]]
                child_spans = get_spans_helper(descendants, start_index)
                result += child_spans
                start_index = child_spans[0][1]
            result = [(orig_start_index, start_index)] + result
            return result
        tree = self._run_base_parser(sent)
        return set(get_spans_helper(tree.treepositions(), 0))


class DependencyParserWrapper:
    def __init__(self):
        pass

    def __call__(self, sent):
        return self.get_spans(sent)
 
    @staticmethod
    def head_to_tree(heads):
        # takes a list of dependency heads and returns each head's children as a dictionary
        children = {}
        for i in range(0,len(heads)+1):
            children[i] = []
        for j in range(0,len(heads)):
            children[heads[j]].append(j+1)
        return children   
 
    @staticmethod
    def descendents(tree,i):
        # takes a dictionary and an index i and returns all descendents of the key at i
        if tree[i] == []:
            return [i]
        else:
            desc = [i]
            for c in tree[i]:
                desc+=(DependencyParserWrapper.descendents(tree,c))
            return desc
    
    @staticmethod
    def compute_spans(tree):
        print(tree)
        # takes a dictionary and returns a list of lists representing
        # constituents
        spans = []
        for i in tree:
            desc = DependencyParserWrapper.descendents(tree,i)
            # we ignore one-word constituents
            if len(desc) > 1 and len(desc) < len(tree):
                spans.append((min(desc)-1,max(desc)))
        return spans
          
