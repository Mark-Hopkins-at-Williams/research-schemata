#!/usr/bin/env python3

import nltk
import benepar
import sys

nltk.download('punkt')
benepar.download('benepar_en2')

from schemata.evaluate import evaluate, AttachmentSchema
from schemata.parse.berkeley import BerkeleyParser

file = sys.argv[1]
schemas = AttachmentSchema.from_plaintext_file("data/" + file)
print(evaluate(schemas, BerkeleyParser()))
