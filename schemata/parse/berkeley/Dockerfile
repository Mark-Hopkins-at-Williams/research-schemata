FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install Cython==0.29.15 numpy==1.18.1 tensorflow==1.15.0
RUN pip install benepar
ENTRYPOINT ["python", "/app/test.py"]
CMD ["pp1.asc"]
