from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from six.moves import input
import tensorflow as tf
import schemata.thirdparty.e2e_coref.coref_model as cm
from schemata.thirdparty.e2e_coref import util
import json

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
    
def create_schema(verb, adj, period):
    if period:
        return "they did not " + verb + " them because they were " + adj + " ."
    else:
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
    """Takes a list of dictionaries and extracts spans from 'predicted_clusters' """
    result = []
    for num, one_dict in enumerate(predictions):
        cluster = predictions[num]["predicted_clusters"]
        span = set(util.flatten(cluster))
        result.append(span)
    return result

def span_from_coref(prediction):
    """Takes one dictionary and extracts spans from 'predicted_clusters' """
    cluster = prediction["predicted_clusters"]
    span = set(util.flatten(cluster))
    return span


def they_or_them(model, verb_adj_pairs, period):
    resultDict = {}
    for verb, adj in verb_adj_pairs:
        sentence = create_schema(verb, adj, period) # Create string of full sentence for prediction
        toks = sentence.split()
        passage = [toks]
        passages = [passage]
        predictions = coref(model, passages)
        for prediction in predictions:
            one_span = span_from_coref(prediction)
            formatted = format_predictions(prediction)
            if len(one_span) == 3:
                resultDict["three"] = resultDict.get("three", []) + [(verb, adj)]
            elif "them" in formatted[0]:
                resultDict["them"] = resultDict.get("them", []) + [(verb, adj)]
            else:
                resultDict["they"] = resultDict.get("they", []) + [(verb, adj)]
    return resultDict

def generate_key(filename):
    """Generates a dictionary with correct 'they/them' verb, adj pairings"""
    pairs = pairs_to_list(filename)
    alternate = True
    result = {}
    for verb, adj in pairs:
        if alternate:
            result["them"] = result.get("them", []) + [(verb, adj)]
            alternate = False
        else:
            result["they"] = result.get("they", []) + [(verb, adj)]
            alternate = True
    return result

def compare(set1, set2):
    """Takes two dictionaries, extracts the verb/adj pairs, and compares the they/them buckets using sets"""
    if set1.get("three", None) != None:
        print("The first dictionary contains three spans. There are " + str(len(set1["three"])) + " pairs.")
    if set2.get("three", None) != None:
        print("The second dictionary contains three spans. There are " + str(len(set2["three"])) + " pairs.")

    object1 = set(set1["them"])
    object2 = set(set2["them"])
    subject1 = set(set1["they"])
    subject2 = set(set2["they"])
    difference1 = object1.difference(object2)
    difference2 = subject1.difference(subject2)
    print(str(len(difference1)) + " object differences: " + str(difference1))
    print(str(len(difference2)) + " subject differences: " + str(difference2))


def large_scale_pairs(verb_json, adj_json):
    with open(verb_json, 'r') as verb_file:
        verbs = json.load(verb_file)
    with open(adj_json, 'r') as adj_file:
        adjs = json.load(adj_file)

    pairs = []
    count = 0
    for verb in verbs:
        for adj in adjs:
            pairs.append((verb["infinitive"], adj["base"]))
    return pairs


if __name__ == "__main__":
    config = util.initialize_from_env('final')
    model = cm.CorefModel(config)
    pairs = pairs_to_list("schema.txt")
    predict_no_period = they_or_them(model, pairs, False)
    predict_with_period = they_or_them(model, pairs, True)
    key = generate_key("schema.txt")

    print("Differences between no period and period: ")
    compare(predict_no_period, predict_with_period)
    print("Differences between period and key: ")
    compare(predict_with_period, key)
    print("Differences between no period and key: ")
    compare(predict_no_period, key)
