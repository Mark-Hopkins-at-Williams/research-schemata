
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
