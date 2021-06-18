from redis import Redis
import time
import logging
logging.basicConfig(level=logging.INFO)

redis = Redis(host='redis', port=6379, db=0)
# Subscribing to events matching pattern "__key*__:*"
p = redis.pubsub()
p.psubscribe('__keyspace@0__:*')
topics = ['main/lamp', 'pacs/door']
logging.info('Starting message loop')
while True:
    message = p.get_message()
    if message:
        # logging.info(message)
        topic = message['channel'].decode().split(':')[1]
        if topic in topics:
            logging.info(f"{topic}: {redis.get(topic).decode()}")
    else:
        time.sleep(0.1)
