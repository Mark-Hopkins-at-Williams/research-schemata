# Model Probing using Sentence Pair Schema

To evaluate the Berkeley parser on schema file 'pp1.asc', do the following
in the Terminal:

    pip install benepar

Then open python and download the Berkeley parser model:

    > import benepar
    > benepar.download('benepar_en2')

Then in a Python interpreter, do the following:

    schemas = AttachmentSchema.from_plaintext_file('pp1.asc')
    evaluate(schemas, BerkeleyParser())        


    