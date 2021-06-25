from redis import Redis
import time
import logging
import yaml
import json

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

        logging.info(json.dumps(data))
        #logging.info(data)
    else:
        time.sleep(0.1)
