# Model Probing Using Sentence Pair Schema

### To locally install the schemata package:

From the top-level directory:

    pip install -e .

### To run all unit tests

From the top-level directory, run: 
    
    python3 -m unittest

### To run a particular unit test module (e.g. test/test_align.py)

From the top-level directory, run:

    python3 -m unittest test.test_berkeley
    



To evaluate the Berkeley parser on schema file 'pp1.asc', do the following
in the Terminal:

    pip install benepar

Then open python and download the Berkeley parser model:

    > import benepar
    > benepar.download('benepar_en2')

Then in a Python interpreter, do the following:

    schemas = AttachmentSchema.from_plaintext_file('pp1.asc')
    evaluate(schemas, BerkeleyParser())        


    