import paho.mqtt.client as mqtt
import redis
import logging
logging.basicConfig(level=logging.INFO)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")


def on_message(client, userdata, msg):
    r.set(msg.topic, msg.payload)
    logging.info(msg.topic + " " + str(msg.payload))

logging.info("listener started")
r = redis.Redis(host="redis")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mosquitto", 1883, 60)
client.username_pw_set(username="mosquitto", password="mosquitto")

client.loop_forever()
