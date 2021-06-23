FROM python:3.9-alpine
WORKDIR /pubsub
RUN pip3 install -r requirements.txt
COPY requirements.txt requirements.txt
COPY pubsub_script.py pubsub_script.py
COPY devices.yaml devices.yaml
CMD ["python3", "pubsub_script.py"]
