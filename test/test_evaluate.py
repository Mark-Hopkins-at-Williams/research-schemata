import unittest

from schemata.parse.evaluate import HighlightedSpan, AttachmentSchema

class TestEvaluate(unittest.TestCase):

    def test_from_plaintext(self):
        hspan = HighlightedSpan.from_plaintext('He found [ the top to the jar ] .')
        assert hspan.tokens == ['He', 'found', 'the', 'top', 'to', 
                                'the', 'jar', '.'] 
        assert hspan.span == (2,7)
        assert not hspan.is_taboo
        hspan = HighlightedSpan.from_plaintext('He was asked { to go by his wife } .')
        assert hspan.tokens == ['He', 'was', 'asked', 'to', 'go', 'by', 
                                'his', 'wife', '.'] 
        assert hspan.span == (3,8)
        assert hspan.is_taboo

    def test_accept(self):
        hspan = HighlightedSpan.from_plaintext('He found [ the top to the jar ] .')
        assert hspan.accept({(2,3), (2,7)})
        assert not hspan.accept({(2,3), (2,6)})
        hspan = HighlightedSpan.from_plaintext('He fastened { the top to the jar } .')
        assert not hspan.accept({(2,3), (2,7)})
        assert hspan.accept({(2,3), (2,6)})

    def test_from_plaintext_file(self):
        schemas = AttachmentSchema.from_plaintext_file('data/pp1.asc')
        schema = next(schemas)
        assert not schema.accept({(2,3), (2,7)}, ({(2,3), (2,7)}))
        assert not schema.accept({(2,3), (3,12)}, ({(2,3), (3,12)}))
        assert schema.accept({(2,3), (3,11)}, ({(2,3), (3,12)}))
        schema = next(schemas)
        assert not schema.accept({(2,3), (2,7)}, ({(2,3), (2,7)}))
        assert not schema.accept({(2,3), (3,9)}, ({(2,3), (3,19)}))
        assert schema.accept({(2,3), (3,10)}, ({(2,3), (3,10)}))
        assert not schema.accept({(2,3), (3,10)}, ({(2,3), (3,9)}))

if __name__ == "__main__":
	unittest.main()
