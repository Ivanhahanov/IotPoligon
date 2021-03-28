from IotKernel.devices import DeviceManagement


class Executor:
    def __init__(self, command):
        self.module = command['module']
        self.device = command['device']
        self.command = command['command']

    def send_command(self):
        if self.check_command() is True:
            return True
        return False

    def get_answer(self):
        pass

    def check_command(self):
        module = DeviceManagement().load_devices(self.module)
        print(module)
        if not module:
            return "module not found"
        device = module.get("devices").get(self.device)
        if not device:
            return "device not found"
        commands = device.get("available_commands")
        if commands:
            if self.command in commands:
                return True
            return f"device haven't command: {self.command}"
        return "device haven't commands for execute"
