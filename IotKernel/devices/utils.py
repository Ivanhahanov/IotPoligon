from . import all_devices


def check_device(module, device, command):
    if not all_devices.get(module):
        return f"Module '{module}' doesn't exist"
    if not all_devices[module]['devices'].get(device):
        return f"Device '{device}' doesn't exist"
    if command not in all_devices[module]['devices'][device].get('available_commands'):
        return f"Device '{device}' doesn't support command {command}"
    return True
