import nltk
from nltk.parse.malt import MaltParser
mp = MaltParser('maltparser-1.9.2', 'engmalt.linear-1.7.mco')
tree = mp.parse_one('The dog eats good food .'.split()).tree()
print(tree)