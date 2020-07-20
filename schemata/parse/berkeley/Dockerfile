FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod +x /app/setup_all.sh && /app/setup_all.sh
ENTRYPOINT ["python", "demo.py", "final"]
