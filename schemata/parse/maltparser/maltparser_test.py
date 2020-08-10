import nltk
from nltk.parse.malt import MaltParser
mp = MaltParser('maltparser-1.9.2', 'engmalt.linear-1.7.mco')
tree = mp.parse_one('I shot an elephant in my pajamas .'.split()).tree()

txt = "A ceasefire for east Ukraine has been agreed during talks in Minsk ."
graph = mp.parse_one(txt.split()).tree
print(graph)
