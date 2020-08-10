#!/usr/bin/env python3

from schemata.parse.evaluate import evaluate, AttachmentSchema
from schemata.parse.maltparser.maltparser import MaltParser
import sys

if __name__ == '__main__':
    file = sys.argv[1]
    schemas = AttachmentSchema.from_plaintext_file(file)
    print(evaluate(schemas, MaltParser()))
