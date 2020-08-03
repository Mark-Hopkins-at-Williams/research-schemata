#!/usr/bin/env python3
import sys

from evaluate import *
from biaffine import *

file = sys.argv[1]
schemas = AttachmentSchema.from_plaintext_file("data/" + file)
print(evaluate(schemas, BiaffineParser()))
