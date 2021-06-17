from redis import Redis
import datetime
import time
import logging
logging.basicConfig(level=logging.INFO)

redis = Redis(host='redis', port=6379, db=0)
# Subscribing to events matching pattern "__key*__:*"
p = redis.pubsub()
p.psubscribe('__key*__:*')
logging.info('Starting message loop')
while True:
    message = p.get_message()
    if message:
        logging.info(datetime.datetime.now(), message)
    else:
        time.sleep(0.1)
