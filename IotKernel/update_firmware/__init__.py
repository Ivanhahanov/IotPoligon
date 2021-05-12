from .update import serve, FLASH
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import subprocess
import os
import yaml


class ESPOptions:
    def __init__(self, code_name, esp_ip, board):
        self.code_name = code_name
        self.esp_ip = esp_ip
        self.host_ip = "0.0.0.0"
        self.esp_port = 8266
        self.host_port = 8266
        self.auth = ""
        # self.image = f"/kernel/IotKernel/update_firmware/bin/{code_name}.bin"
        self.command = FLASH
        self.board = board
        self.path = Path('/kernel/IotKernel/update_firmware')
        self.image = self.path.joinpath('bin', f'{code_name}.bin')

    def update(self):
        return serve(self.esp_ip,
                     self.host_ip,
                     self.esp_port,
                     self.host_port,
                     self.auth,
                     self.image,
                     self.command)

    def check_external_libs(self):
        #  external_libs_file = os.path.join('/kernel/IotKernel/update_firmware/src', self.code_name, "external_libs.yml")
        external_libs_file = self.path.joinpath('src', self.code_name, 'external_libs.yml')
        if not external_libs_file.exists():
            raise Exception(f"Can't find {external_libs_file}")

        with open(external_libs_file) as f:
            libs = yaml.safe_load(f.read())[self.code_name]

        libs_list_command = 'arduino-cli lib list'
        result, error = self.exec_command(libs_list_command)

        # load library lines
        lines = {x.strip().split()[0]: x.strip().split()[1] for x in result.decode().split("\n")[1:] if x.strip()}

        # compare install and using libraries
        common_pairs = dict()
        for lib, version in lines.items():
            if lib in lines and version == libs.get(lib):
                common_pairs[lib] = version
        lib_names_compare = libs.items() - common_pairs.items()
        if lib_names_compare:
            raise Exception(f"Can't find name or version {', '.join([':'.join(lib) for lib in lib_names_compare])}")

    def convert_code(self):
        #  env = Environment(loader=FileSystemLoader(f'/kernel/IotKernel/update_firmware/raw_src/{self.code_name}'))
        env = Environment(loader=FileSystemLoader(self.path.joinpath('raw_src', self.code_name)))
        template = env.get_template(f'{self.code_name}.ino')
        with open(self.path.joinpath('global_values.yml'), 'r') as gv:
            data = yaml.safe_load(gv.read())
        output_render = template.render(**data)
        #  if os.path.exists(f"/kernel/IotKernel/update_firmware/src/{self.code_name}"):
        if (self.path.joinpath('src', self.code_name)).exists():
            pass
            # print("Directory already exists!")
            # print("Refactoring file...")
        else:
            #  os.mkdir(f"/kernel/IotKernel/update_firmware/src/{self.code_name}")
            (self.path.joinpath('src') / self.code_name).mkdir()

        with open(self.path.joinpath('src', self.code_name, f'{self.code_name}.ino'), 'w') as pc:
            pc.write(output_render)
        #  with open(f'/kernel/IotKernel/update_firmware/src/{self.code_name}/{self.code_name}.ino', 'w') as pc:
        #  pc.write(output_render)

        return output_render

    def build(self):
        # try:
        #     self.check_board()
        # except Exception as e:
        #     return str(e)
        arduino_build = f"arduino-cli compile -b {self.board} " \
                        f"/kernel/IotKernel/update_firmware/src/{self.code_name}/" \
                        f" --output /kernel/IotKernel/update_firmware/bin/{self.code_name}"
        result, error = self.exec_command(arduino_build)
        print("build", result.decode(), error)
        if result.decode().strip() != '':
            return True
        return error.decode()

    def check_board(self):
        check_board_command = f"arduino-cli board listall {self.board}"
        result, error = self.exec_command(check_board_command)
        if result:
            lines = result.decode().split("\n")
            lines = [x.strip() for x in lines if x.strip()]
            available_names = '\n'.join([line.split()[-1] for line in lines[1:]])
            if len(lines) < 2:
                raise Exception(f"Board {self.board} not found")
            if len(lines) > 2:
                raise Exception(f"Too many boards for '{self.board}' found:\n{available_names}")
            if lines[1].split()[-1] != self.board:
                raise Exception(f"Wrong name {self.board} available names:\n{available_names}")

    @staticmethod
    def exec_command(command):
        result = subprocess.Popen(command,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, shell=True)
        result.wait()
        return result.communicate()


if __name__ == '__main__':
    esp = ESPOptions("esp_test", "192.168.1.79", "esp8266:esp8266:nodemcuv2")
    converted_code = esp.convert_code()
    build_result = esp.build()
    esp.check_external_libs()

    if build_result is True:
        print("Build Successfully Completed")
    else:
        print(build_result)

    update_result = esp.update()
    if update_result == 0:
        print("Updade Successfully Completed")
    else:
        print("Update failed!")
