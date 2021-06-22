from redis import Redis
import time
import logging
import yaml

logging.basicConfig(level=logging.INFO)

with open('devices.yaml', 'r') as file:
    data = yaml.safe_load(file.read())
data = list(data)

topics = []
for t in data:
    topics.append(t)
print(topics)
# topics = [row["topic"] for row in data]

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
            if rendered_topic in topics:
                logging.info(f'{rendered_topic} in file')
    else:
        time.sleep(0.1)
