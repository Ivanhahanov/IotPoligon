import requests
import yaml


class Module:
    def __init__(self, config_file, server_address="kernel"):
        self.config_file = config_file
        self.server_address = server_address

    def init_module(self):
        result = self.register_module()
        if not result:
            print("Cannot register module")
            exit(1)

    def register_module(self):
        with open(self.config_file, "r") as f:
            module = yaml.safe_load(f.read())

        url = f"http://{self.server_address}/modules/register"
        print(module)
        r = requests.post(url, json=module).json()
        if r.get("status"):
            return True
        print("Register module error", r)
        return False


if __name__ == '__main__':
    m = Module("pacs_devices.yml")
    m.init_module()
    print("pacs started")
