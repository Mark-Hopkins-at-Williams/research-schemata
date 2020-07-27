import unittest

from thirdparty.e2e_coref.demo_schema import *

class TestEvaluate(unittest.TestCase):
    def setUp(self):
        config = util.initialize_from_env('final')
        model = cm.CorefModel(config)
    
    def test_coref:
        passages = [["they did not eat them because they were spoiled".split()]]
        prediction = coref(model, passages)
        assert prediction == [{'clusters': [], 'doc_key': 'nw', 'sentences': [['they', 'did', 'not', 'eat', 'them', 'because', 'they', 'were', 'spoiled']], 'speakers': [['spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1']], 'predicted_clusters': [((4, 4), (6, 6))]}]

        passages2 = [["they did not pick them because they were dirty".split()],["they did not purchase them because they were disgusted".split()]]
        prediction = coref(model, passages2)
        assert prediction == [
            {'clusters': [], 'doc_key': 'nw', 'sentences': [['they', 'did', 'not', 'dick', 'them', 'because', 'they', 'were', 'dirty']], 'speakers': [['spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1']], 'predicted_clusters': [((4, 4), (6, 6))]},
            {'clusters': [], 'doc_key': 'nw', 'sentences': [['they', 'did', 'not', 'purchase', 'them', 'because', 'they', 'were', 'disgusted']], 'speakers': [['spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1', 'spk1']], 'predicted_clusters': [((0, 0), (6, 6))]}
            ]
    
    def test_pairs_to_list(self):
        result = pairs_to_list("thirdparty/e2e_coref/schema.txt")
        assertIn(('eat', 'spoiled'), result)
        
    def test_spans_from_coref(self):
        passages = [["they did not pick them because they were dirty".split()],["they did not eat them because they were disgusted".split()]]
        clusters = spans_from_coref(coref(model, passages))
        assert span[0] == {(4, 4), (6, 6)}
        assert span[1] == {(0, 0), (6, 6)}
        
    def test_they_or_them(self):
        cluster = they_or_them(model, pairs_to_list("schema.txt"))
        subjects = cluster["they"]
        objects = cluster["them"]
        assertIn(("pick", "disgusted"), subjects)
        assertIn(("pick", "dirty"), objects)
        assertIn(("purchase", "frugal"), subjects)
        assertIn(("purchase", "unnecessary"), objects)
        
if __name__ == "__main__":
	unittest.main()
