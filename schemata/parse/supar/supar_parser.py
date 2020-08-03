from supar import Parser
import sys

class suPar:
    def __init__(self, model = "crf-con-en"):
        self.parser = Parser.load(model)

    def __call__(self, sent):
        return self.get_spans(sent)

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
        dataset = self.parser.predict([sent.split()], verbose=False)
        tree = dataset.trees[0]
        return set(get_spans_helper(tree.treepositions(), 0))


if __name__ == '__main__':
    sentfile = sys.argv[1]
    outfile = sys.argv[2]
    parser = suPar()
    with open(sentfile) as reader:
        with open(outfile, 'w') as writer:
            for line in reader:
                line = line.strip()
                output = parser(line)
                writer.write(str(output))
                writer.write('\n')
