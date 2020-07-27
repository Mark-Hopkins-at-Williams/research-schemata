from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import schemata.thirdparty.e2e_coref.coref_model as cm
from schemata.thirdparty.e2e_coref import util

import nltk
nltk.download("punkt")

def create_schema(verb, adj):
    return "they did not " + verb + " them because they were " + adj

def coref(model, passages):
    def generate_coref_input(passage):
        speakers = []
        for sent in passage:
            speakers.append(['spk1' for x in sent])
        return {"clusters": [], "doc_key": "nw", 
                "sentences": passage, 
                "speakers": speakers}
    result = []
    with tf.Session() as session:
        model.restore(session)
        for example_num, passage in enumerate(passages):
            example = generate_coref_input(passage)
            tensorized_example = model.tensorize_example(example, is_training=False)
            feed_dict = {i:t for i,t in zip(model.input_tensors, tensorized_example)}
            _, _, _, top_span_starts, top_span_ends, top_antecedents, top_antecedent_scores = session.run(model.predictions, feed_dict=feed_dict)
            predicted_antecedents = model.get_predicted_antecedents(top_antecedents, top_antecedent_scores)
            example["predicted_clusters"], _ = model.get_predicted_clusters(top_span_starts, top_span_ends, predicted_antecedents)
            result.append(example)
    return result

def pairs_to_list(filename):
    with open(filename, "r") as f:
        pairs = [tuple(line.strip().split()) for line in f]
    return pairs

def spans_from_coref(predictions):
    result = []
    for num, one_dict in enumerate(predictions):
        cluster = predictions[num]["predicted_clusters"]
        span = set(util.flatten(cluster))
        result.append(span)
    return result

def they_or_them(model, verb_adj_pairs):
    def format_predictions(example):
        results = []
        words = util.flatten(example["sentences"])
        for cluster in example["predicted_clusters"]:
          oneCluster = [" ".join(words[m[0]:m[1]+1]) for m in cluster]
          results.append(oneCluster)
        return results
    resultDict = {}
    for verb, adj in verb_adj_pairs:
        sentence = create_schema(verb, adj) # Create string of full sentence for prediction
        toks = sentence.split()
        passage = [toks]
        passages = [passage]
        predictions = coref(model, passages)
        for prediction in predictions:
            formatted = format_predictions(prediction)
            if "them" in formatted[0]:
                resultDict["them"] = resultDict.get("them", []) + [(verb, adj)]
            else:
                resultDict["they"] = resultDict.get("they", []) + [(verb, adj)]
    return resultDict

if __name__ == "__main__":
  config = util.initialize_from_env('final')
  model = cm.CorefModel(config)
  pairs = pairs_to_list("schema.txt")
  predictions = coref(model, pairs)
  print(predictions)
