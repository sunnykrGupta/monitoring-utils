FROM python:3.7-slim-stretch

WORKDIR /

# pyPI dependency file
COPY requirements.txt .

RUN pip install -r requirements.txt

# all python files inside working directory.
COPY *.py ./

# Run
ENTRYPOINT ["python3" ,"custom-kafka-exporter.py"]
