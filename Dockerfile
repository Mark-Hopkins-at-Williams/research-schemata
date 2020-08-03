FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install tensorflow==1.15.0
RUN pip install supar
ENTRYPOINT ["python", "/app/schemata/parse/supar/run_parser.py"]
CMD ["data/pp1.asc"]
