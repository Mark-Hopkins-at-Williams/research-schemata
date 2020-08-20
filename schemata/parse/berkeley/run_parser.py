#!/usr/bin/env python3

import nltk
import benepar
import sys

nltk.download('punkt')
benepar.download('benepar_en2')

from schemata.parse.evaluate import evaluate, AttachmentSchema
from schemata.parse.berkeley.berkeley import BerkeleyParser

if __name__ == '__main__':
    file = sys.argv[1]
    schemas = AttachmentSchema.from_plaintext_file(file)
    print(evaluate(schemas, BerkeleyParser()))
