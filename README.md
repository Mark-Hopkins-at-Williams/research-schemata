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
 
### To evaluate a parser using attachment schema
 
To evaluate the Berkeley parser on schema file 'pp1.asc', do the following
in the Terminal:

    pip install benepar

Then open python and download the Berkeley parser model:

    > import benepar
    > benepar.download('benepar_en2')

Then in a Python interpreter, do the following:


    from schemata.parse.evaluate import * 
    from schemata.parse.berkeley import *
    schemas = AttachmentSchema.from_plaintext_file('data/pp1.asc')
    evaluate(schemas, BerkeleyParser())        


### To use Spacy parser

Download the models:

    python -m spacy download en_core_web_sm
    
    
### To install/use Stanford parser

From Terminal:

    pip install stanza

In a Python interpreter:

    >>> import stanza
    >>> stanza.install_corenlp()
    

    
## Dockerizing the thirdparty components

### To Dockerize e2e-coref (Kenton Lee)

From the top-level directory:

    cd thirdparty/e2e-coref
    docker build --tag e2e:1.0 . 
    
Then to run the Docker image:

    docker run -v $PWD:/home/docker/data -m 16G e2e:1.0 in.json /home/docker/data/out.json
    





    