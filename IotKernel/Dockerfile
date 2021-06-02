FROM python:3.9
RUN wget -O /tmp/cli.tar.bz2 \
        https://downloads.arduino.cc/arduino-cli/arduino-cli-latest-linux64.tar.bz2 && \
    cd /tmp && \
    mkdir arduino && \
    bunzip2 /tmp/cli.tar.bz2 && \
    tar -xvf /tmp/cli.tar && \
    mv /tmp/arduino-cli* /usr/bin/arduino-cli
COPY update_firmware/arduino/arduino-cli.yaml /root/.arduino15/arduino-cli.yaml
RUN arduino-cli core update-index
RUN arduino-cli core install esp8266:esp8266
WORKDIR kernel
COPY . IotKernel
RUN pip3 install -r IotKernel/requirements.txt
CMD uvicorn IotKernel.api.server:app --host 0.0.0.0 --port 80 --reload