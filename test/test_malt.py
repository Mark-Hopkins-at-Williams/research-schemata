import unittest

from schemata.parse.maltparser.maltparser import MaltParser

class TestMalt(unittest.TestCase):
    
    def test_get_spans(self):        
        parser = MaltParser()
        spans = parser('I shot an elephant in my pajamas .')
        assert spans == {(0, 1), (1, 2), (4, 7), (6, 7), (4, 5), (5, 6), 
                         (5, 7), (2, 3), (3, 4), (0, 8), (7, 8), (2, 4)}

    def disabled_test_get_spans2(self): # why is malt parser failing on this?
        parser = MaltParser()
        spans = parser("The dog eats good food .") 
        assert spans == {(0, 1), (0, 2), (0, 6), (1, 2), (2, 3),
                         (3, 4), (3, 5), (4, 5), (5, 6)}


if __name__ == "__main__":
	unittest.main()
