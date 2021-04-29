import paho.mqtt.client as mqtt
import json
import redis


class MQTT:
    def __init__(self):
        self.red = redis.Redis(host="redis")
        self.client = mqtt.Client("Kernel")
        self.client.username_pw_set(username="mosquitto", password="mosquitto")
        self.client.connect("mosquitto")

    def publish(self, command, *args, payload_format=None):
        topic = '/'.join(args)
        if payload_format == "json":
            command = self.convert_command_to_json(command)
        self.client.publish(topic=topic, payload=command)

    def get_data(self, *args):
        topic = '/'.join(args)
        data = self.red.get(topic)
        return data.decode()

    @staticmethod
    def convert_command_to_json(command):
        return json.dumps({"command": command})
