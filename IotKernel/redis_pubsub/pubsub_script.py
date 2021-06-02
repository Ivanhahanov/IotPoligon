import time
from redis import StrictRedis
import logging
logging.basicConfig(level=logging.INFO)
redis = StrictRedis(host='redis')

pubsub = redis.pubsub()
pubsub.psubscribe('__keyspace@0__:*')

logging.info("Server started")
while True:
    message = pubsub.get_message()
    if message:
        print(message)
    else:
        time.sleep(0.01)
