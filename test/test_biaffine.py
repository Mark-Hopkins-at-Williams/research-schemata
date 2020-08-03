import unittest

from schemata.parse.biaffine.biaffine import BiaffineParser

class TestBiaffine(unittest.TestCase):
    
    def test_get_spans(self):        
        parser = BiaffineParser()
        spans = parser("The dog eats good food .") 
        assert spans == {(0, 1), (0, 2), (0, 6), (1, 2), (2, 3),
                         (3, 4), (3, 5), (4, 5), (5, 6)}


if __name__ == "__main__":
	unittest.main()
