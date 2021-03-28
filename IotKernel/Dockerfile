FROM python:3.9-alpine
WORKDIR kernel
COPY . IotKernel
RUN pip3 install -r IotKernel/requirements.txt
CMD uvicorn IotKernel.api.server:app --host 0.0.0.0 --port 80 --reload