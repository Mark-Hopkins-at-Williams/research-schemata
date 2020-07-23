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

def make_predictions(text, model):
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
      oneCluster = [" ".join(words[m[0]:m[1]+1]) for m in cluster]
      results.append(oneCluster)
    return results
    
def createSchema(verb, adj):
    return "they did not " + verb + " them because they were " + adj

if __name__ == "__main__":
  config = util.initialize_from_env()
  model = cm.CorefModel(config)
  with tf.Session() as session:
    model.restore(session)
    resultDict = {}
    fileName = input("Document text: ") # Take in text files w/ format verb, adj (i.e. eat spoiled)
    for line in open(fileName, 'r'): # Read file line by line and get predictions
        oneLine = line.strip().split()
        verb, adj = tuple(oneLine)
        sentence = createSchema(verb, adj) # Create string of full sentence for prediction
        predictions = format_predictions(make_predictions(sentence, model)) #returns list of list
        if "them" in predictions[0]:
            resultDict["them"] = resultDict.get("them", []) + [(verb, adj)]
        else:
            resultDict["they"] = resultDict.get("they", []) + [(verb, adj)]
    print("Subject Coreference: " + str(resultDict["they"]))
    print("Object Coreference: " + str(resultDict["them"]))
