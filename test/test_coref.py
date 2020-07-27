import unittest

from schemata.thirdparty.e2e_coref.demo_schema import they_or_them , pairs_to_list
from schemata.thirdparty.e2e_coref.demo_schema import coref, spans_from_coref

import schemata.thirdparty.e2e_coref.coref_model as cm
from schemata.thirdparty.e2e_coref import util



class TestEvaluate(unittest.TestCase):
    def setUp(self):
        config = util.initialize_from_env('final')
        self.model = cm.CorefModel(config)
    
    def test_coref(self):
        predictions = coref(self.model, [["i think therefore i am".split()], 
                                         ["they think therefore they were".split()]])
        assert len(predictions) == 2
        assert predictions[0] == {'clusters': [],
                                  'doc_key': 'nw',
                                  'sentences': [['i', 'think', 'therefore', 'i', 'am']],
                                  'speakers': [['spk1', 'spk1', 'spk1', 'spk1', 'spk1']],
                                  'predicted_clusters': [((0, 0), (3, 3))]}
        assert predictions[1] == {'clusters': [],
                                  'doc_key': 'nw',
                                  'sentences': [['they', 'think', 'therefore', 'they', 'were']],
                                  'speakers': [['spk1', 'spk1', 'spk1', 'spk1', 'spk1']],
                                  'predicted_clusters': [((0, 0), (4, 4))]}
                
    
    def test_coref2(self):
        predictions = coref(self.model, [["i think therefore i am".split()]])
        assert len(predictions) == 1
        assert predictions[0] == {'clusters': [],
                                  'doc_key': 'nw',
                                  'sentences': [['i', 'think', 'therefore', 'i', 'am']],
                                  'speakers': [['spk1', 'spk1', 'spk1', 'spk1', 'spk1']],
                                  'predicted_clusters': [((0, 0), (3, 3))]}
    
    def test_pairs_to_list(self):
        result = pairs_to_list("thirdparty/e2e_coref/schema.txt")
        assert ('eat', 'spoiled') in result
        
    def test_spans_from_coref(self):
        predictions = coref(self.model, [["i think therefore i am".split()], 
                                         ["they think therefore they were".split()]])
        clusters = spans_from_coref(coref(self.model, predictions))
        assert clusters[0] == {(0, 0), (3, 3)}
        assert clusters[1] == {(0, 0), (4, 4)}
        
    def test_they_or_them(self):
        clusters = they_or_them(self.model, [('eat', 'spoiled'),('like', 'disappointed')])
        subjects = clusters["they"]
        objects = clusters["them"]
        assert subjects == [('like', 'disappointed')]
        assert objects == [('eat', 'spoiled')] 
        
if __name__ == "__main__":
	unittest.main()
