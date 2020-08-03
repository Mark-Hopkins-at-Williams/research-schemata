def evaluate(schemas, parser):
    """
    To evaluate the suPar parser on the schemas in 'pp1.asc':
    
        schemas = AttachmentSchema.from_plaintext_file('pp1.asc')
        evaluate(schemas, suPar())
    
    """
    correct = 0
    total = 0
    for schema in schemas:
        total += 1
        if schema.accept(parser(' '.join(schema.hspan1.tokens)), 
                         parser(' '.join(schema.hspan2.tokens))):
            correct += 1
    return correct, total

class AttachmentSchema:
    def __init__(self, hspan1, hspan2):
        self.hspan1 = hspan1
        self.hspan2 = hspan2
        
    def accept(self, parse1_spans, parse2_spans):
        return (self.hspan1.accept(parse1_spans) and 
                self.hspan2.accept(parse2_spans))

    @staticmethod
    def from_plaintext(sent1, sent2):
        return AttachmentSchema(HighlightedSpan.from_plaintext(sent1),
                                HighlightedSpan.from_plaintext(sent2))

    @staticmethod
    def from_plaintext_file(filename):
        with open(filename) as inhandle:
            all_lines = inhandle.readlines()
        for i in range(0, len(all_lines), 2):
            schema = AttachmentSchema.from_plaintext(all_lines[i].strip(),
                                                     all_lines[i+1].strip())
            yield schema
        
        
class HighlightedSpan:
    def __init__(self, tokens, span, is_taboo):
        self.tokens = tokens
        self.span = span
        self.is_taboo = is_taboo
       
    def accept(self, spans):
        if self.is_taboo:
            return self.span not in spans
        else:
            return self.span in spans
        
    @staticmethod
    def from_plaintext(sent):
        toks = sent.split()
        if '[' in toks:
            open_bracket = '['
            close_bracket = ']'
        elif '{' in toks:
            open_bracket = '{'
            close_bracket = '}'
        else:
            raise Exception('Invalid schema: ' + sent)            
        start = toks.index(open_bracket)
        stop = toks.index(close_bracket) - 1
        toks = [tok for tok in toks if 
                tok != open_bracket and tok != close_bracket]
        return HighlightedSpan(toks, (start, stop), open_bracket == '{')
        
