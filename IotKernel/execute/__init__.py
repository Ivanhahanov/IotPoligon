from IotKernel.devices import DeviceManagement, all_devices
from IotKernel.execute.protocols.mqtt import MQTT


class Executor(DeviceManagement):
    def __init__(self, module, device, command=None):
        DeviceManagement().__init__()
        self.module = module
        self.device = device
        self.command = command
        self.protocol = self.get_device_protocol()

    def send_command(self):
        if self.check_command() is True:
            if self.protocol == "mqtt":
                mqtt = MQTT()
                mqtt.publish(self.command, self.module, self.device, payload_format="json")
            return True
        return False

    def get_answer(self):
        if self.protocol == "mqtt":
            mqtt = MQTT()
            return mqtt.get_data(self.module, self.device)

    def get_device_protocol(self):
        return all_devices[self.module].get('protocol')

    def check_command(self):
        module = all_devices[self.module]
        if not module:
            return "module not found"
        device = module["devices"].get(self.device)
        if not device:
            return "device not found"
        commands = device.get("available_commands")
        if commands:
            if self.command in commands:
                return True
            return f"device haven't command: {self.command}"
        return "device haven't commands for execute"
