all_devices = {
    "main": {
        "description": "basic module for smart home",
        "description_ru": "Базовый модуль для эмуляции умного дома",
        "protocol": "mqtt",
        "devices": {
            "lamp": {
                "description": "table lamp",
                "protocol": "mqtt",
                "available_commands": ["on", "off"]},
            "temp": {
                "description": "table lamp",
                "protocol": "mqtt",
                "available_commands": ["get"]}
        },
    },
}


class DeviceManagement:
    def __init__(self):
        self.all_devices = all_devices

    def load_devices(self, module=None):
        if module:
            module_devices = self.all_devices.get(module)
            if module_devices:
                return {module: module_devices}
            return None
        return all_devices


class CrudDevice(DeviceManagement):
    def __init__(self, device):
        super().__init__()
        self.device_name = device.get('name')
        del device['name']
        self.device = device
        self.module = device.get('module', 'main')
        del device['module']

    def add_device(self):
        if self.check_device():
            self.all_devices[self.module]['devices'][self.device_name] = self.device
            return True
        return False

    def device_info(self):
        info = self.all_devices[self.module]['devices'][self.device_name].copy()
        device = {self.device_name: info}
        return device

    def update_device(self):
        if self.check_device():
            print(self.device)
            self.all_devices[self.module]['devices'][self.device_name].update(self.device)
            return True
        return False

    def delete_device(self):
        del self.all_devices[self.module]['devices'][self.device_name]
        return True

    def check_device(self):
        if not self.all_devices.get(self.module):
            return "Module doesn't exist"
        if self.all_devices[self.module]['devices'].get(self.device_name):
            return "Device already exists"
        return True
