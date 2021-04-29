FROM python:3.9-alpine
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY listener listener
WORKDIR listener
CMD python3 main.py