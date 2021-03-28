FROM python:3.9-alpine
WORKDIR pacs
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 pacs.py