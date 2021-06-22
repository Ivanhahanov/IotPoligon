from redis import Redis
import time
import logging
import yaml
import json

logging.basicConfig(level=logging.INFO)

with open('devices.yaml', 'r') as file:
    data = yaml.safe_load(file.read())

topics = [row["topic"] for row in data.values()]

redis = Redis(host='redis', port=6379, db=0)
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
        if topic in topics:
            logging.info(f"{topic}: {redis.get(topic).decode()}")
            rendered_topic = topic
            logging.info(rendered_topic)
            if rendered_topic in topics:
                command_dump = redis.get(topic).decode()
                topic_dump = json.dumps(rendered_topic)
                logging.info([topic_dump, command_dump])
    else:
        time.sleep(0.1)
