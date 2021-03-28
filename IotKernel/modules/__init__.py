from IotKernel.devices import all_devices


class ExternalModules:
    def __init__(self, module):
        self.module_name = module.get('name')
        del module["name"]
        self.module = module
        self.devices = module.get("devices")

    def add_module(self):
        if self.check_module() is True:
            all_devices[self.module_name] = self.module
            return True
        return False

    def check_module(self):
        if not self.module_name:
            return "Module must have a name"
        if not self.devices:
            return "Module must have devices"
        if not self.module.get("description"):
            return "Module must have description"
        if not self.module.get("protocol"):
            return "Module must have protocol"
        return True
