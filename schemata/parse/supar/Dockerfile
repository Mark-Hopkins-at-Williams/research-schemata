FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install tensorflow==1.15.0
RUN pip install supar
ENTRYPOINT ["python", "/app/test.py"]
CMD ["pp1.asc"]
