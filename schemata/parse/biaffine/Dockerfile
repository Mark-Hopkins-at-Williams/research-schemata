FROM allennlp/allennlp:latest
COPY . /app
WORKDIR /app
RUN pip install allennlp
RUN pip install --pre allennlp-models
ENTRYPOINT ["python", "/app/test.py"]
CMD ["pp1.asc"]
