#!/usr/bin/env python3

from evaluate import *
from BLLIP import *
import sys

file = sys.argv[1]
schemas = AttachmentSchema.from_plaintext_file("data/" + file)
print(evaluate(schemas, BLLIP()))
