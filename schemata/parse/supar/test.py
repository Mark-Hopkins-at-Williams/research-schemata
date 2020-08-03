#!/usr/bin/env python3

from evaluate import *
from supar_parser import *
import sys

file = sys.argv[1]
schemas = AttachmentSchema.from_plaintext_file("data/" + file)
print(evaluate(schemas, suPar()))
