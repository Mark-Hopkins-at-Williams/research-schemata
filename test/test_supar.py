import unittest

from schemata.parse.supar.supar_parser import SuPar

class TestSupar(unittest.TestCase):
    
    def test_parser(self):        
        parser = SuPar()
        spans = parser("Short cuts make long delays .")    
        assert spans == {(0, 1), (0, 2), (0, 6), (1, 2), (2, 3),
                         (2, 5), (3, 4), (3, 5), (4, 5), (5, 6)}


if __name__ == "__main__":
	unittest.main()
