FROM python:3.7
COPY . /app
WORKDIR /app
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
RUN curl -X GET -o "e2e-coref.tgz" \
    "https://storage.googleapis.com/reed-nlp/e2e-coref.tgz" 
RUN tar -xzvf e2e-coref.tgz
RUN rm e2e-coref.tgz
RUN bash /app/setup_all.sh
ENTRYPOINT ["python", "predict.py", "final"]
