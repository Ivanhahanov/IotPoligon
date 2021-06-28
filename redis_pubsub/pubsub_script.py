from redis import Redis
import time
import logging
import yaml
import json
import paho.mqtt.client as mqtt

# Connection to mosquitto
mqtt_client = mqtt.Client('display')
mqtt_client.connect('mosquitto', port=1883)
logging.basicConfig(level=logging.INFO)
redis = Redis(host='redis', port=6379, db=0)
with open('devices.yaml', 'r') as file:
    data = yaml.safe_load(file.read())
    for device in data.values():
        icon = redis.get(device['icon'])
        if icon:
            device['icon'] = icon.decode()
# topics = [row["topic"] for row in data.values()]
# icons = [row["icon"] for row in data.values()]
# Subscribing to events matching pattern "__key*__:*"
p = redis.pubsub()
p.psubscribe('__keyspace@0__:*')
# topics = ['main/lamp', 'pacs/door']
logging.info('Starting message loop')
while True:
    message = p.get_message()
    if message:
        # logging.info(message)
        topic = message['channel'].decode().split(':')[1]
        for values in data.values():
            if topic == values['topic']:
                # Decoding redis payload from bytes to obj
                command = json.loads(redis.get(topic).decode())['command']
                values.update({'command': redis.get(command).decode()})

        # logging.info(json.dumps(data))
        json_dump = json.dumps(data)
        logging.info(json_dump)
        # Publish json_dump to mosquitto
        if mqtt_client.publish("main/display", json_dump):
            logging.info("Message published")
        else:
            logging.info("Publishing error")
    else:
        time.sleep(0.1)
