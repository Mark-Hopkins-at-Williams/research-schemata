FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install Cython==0.29.15 numpy==1.18.1 \
    pip install torch==0.4.1 pytorch-pretrained-bert==0.4.0
RUN cd EVALB; make; cd ..
ENTRYPOINT ["python", "src/main.py", "train"]
CMD ["--use-bert", "--model-path-base", "models/en_bert", "--bert-model", "bert-large-uncased", "--num-layers", "2", "--learning-rate", "0.00005", "--batch-size", "32", "--eval-batch-size", "16", "--subbatch-max-tokens", "500"]