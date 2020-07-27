from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from six.moves import input
import tensorflow as tf
import coref_model as cm
import util

import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize, word_tokenize


def create_example(text):
  raw_sentences = sent_tokenize(text)
  sentences = [word_tokenize(s) for s in raw_sentences]
  speakers = [["" for _ in sentence] for sentence in sentences]
  return {
    "doc_key": "nw",
    "clusters": [],
    "sentences": sentences,
    "speakers": speakers,
  }

def print_predictions(example):
  words = util.flatten(example["sentences"])
  for cluster in example["predicted_clusters"]:
    print(u"Predicted cluster: {}".format([" ".join(words[m[0]:m[1]+1]) for m in cluster]))

def make_predictions(text, model, session):
  example = create_example(text)
  tensorized_example = model.tensorize_example(example, is_training=False)
  feed_dict = {i:t for i,t in zip(model.input_tensors, tensorized_example)}
  _, _, _, mention_starts, mention_ends, antecedents, antecedent_scores, head_scores = session.run(model.predictions + [model.head_scores], feed_dict=feed_dict)

  predicted_antecedents = model.get_predicted_antecedents(antecedents, antecedent_scores)

  example["predicted_clusters"], _ = model.get_predicted_clusters(mention_starts, mention_ends, predicted_antecedents)
  example["top_spans"] = zip((int(i) for i in mention_starts), (int(i) for i in mention_ends))
  example["head_scores"] = head_scores.tolist()
  return example
  
# New functions
def format_predictions(example):
    results = []
    words = util.flatten(example["sentences"])
    for cluster in example["predicted_clusters"]:
      #print(cluster)
      oneCluster = [" ".join(words[m[0]:m[1]+1]) for m in cluster]
      results.append(oneCluster)
    return results
    
def create_schema(verb, adj):
    return "they did not " + verb + " them because they were " + adj

def generate_coref_input(passage):
    speakers = []
    for sent in passage:
        speakers.append(['spk1' for x in sent])
    return {"clusters": [], "doc_key": "nw", 
            "sentences": passage, 
            "speakers": speakers}

def coref(model, passages):
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
