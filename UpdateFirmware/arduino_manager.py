import json
import subprocess


class ArduinoManage:

    def install_new_lib(self, library_name):
        install_lib_command = f"./arduino-cli lib install {library_name}"
        result, error = self.execute_command(install_lib_command)

    def update_lib(self, library_name):
        pass

    def install_board(self, fqbn):
        install_board_command = f"./arduino-cli core install {fqbn}"
        result, error = self.execute_command(install_board_command)
        print(result)

    def search_lib(self, library_name):
        search_lib = f"./arduino-cli lib search {library_name}"
        result = self.execute_command(search_lib)
        available_libraries = [lib['name']for lib in result['libraries']]
        print(available_libraries)

    def search_board(self, fqbn):
        search_board = f"./arduino-cli core search {fqbn}"
        result = self.execute_command(search_board)
        available_boards = result[0]["Boards"]
        fqbn_list = [line["fqbn"] for line in available_boards]
        print(fqbn_list)

    def uninstall_lib(self, library_name):
        search_lib = f"./arduino-cli core search {library_name}"
        result = self.execute_command(search_lib)
        print(result)

    @staticmethod
    def execute_command(command):
        result = subprocess.Popen(f"{command} --format json", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  shell=True)
        answer, error = result.communicate()
        return json.loads(answer)


if __name__ == '__main__':
    install = ArduinoManage()
    install.search_lib("Adafruit NeoPixel")
    install.search_board("esp8266")
