FROM python:3.9-alpine
WORKDIR /pubsub
COPY requirements.txt requirements.txt
COPY pubsub_script.py pubsub_script.py
RUN pip3 install -r requirements.txt
CMD ["python3", "pubsub_script.py"]
