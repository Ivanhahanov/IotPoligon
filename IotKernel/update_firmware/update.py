from __future__ import print_function
from jinja2 import Environment, FileSystemLoader
import subprocess
import socket
import sys
import os
import hashlib
import random
import logging
import yaml

FLASH = 0
SPIFFS = 100
AUTH = 200
PROGRESS = False


def update_progress(progress):
    if PROGRESS:
        bar_length = 60  # Modify this to change the length of the progress bar
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done...\r\n"
        block = int(round(bar_length * progress))
        text = "\rUploading: [{0}] {1}% {2}".format("=" * block + " " * (bar_length - block), int(progress * 100),
                                                    status)
        sys.stderr.write(text)
        sys.stderr.flush()
    else:
        sys.stderr.write('')
        sys.stderr.flush()


def serve(remote_addr, local_addr, remote_port, local_port, password, filename, command=FLASH):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (local_addr, local_port)
    logging.info('Starting on %s:%s', str(server_address[0]), str(server_address[1]))
    try:
        sock.bind(server_address)
        sock.listen(1)
    except Exception:
        logging.error("Listen Failed")
        return 1

    # Check whether Signed Update is used.
    if os.path.isfile(filename + '.signed'):
        filename = filename + '.signed'
        file_check_msg = 'Detected Signed Update. %s will be uploaded instead.' % filename
        sys.stderr.write(file_check_msg + '\n')
        sys.stderr.flush()
        logging.info(file_check_msg)

    content_size = os.path.getsize(filename)
    f = open(filename, 'rb')
    file_md5 = hashlib.md5(f.read()).hexdigest()
    f.close()
    logging.info('Upload size: %d', content_size)
    message = '%d %d %d %s\n' % (command, local_port, content_size, file_md5)

    # Wait for a connection
    logging.info('Sending invitation to: %s', remote_addr)
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    remote_address = (remote_addr, int(remote_port))
    sock2.sendto(message.encode(), remote_address)
    sock2.settimeout(10)
    try:
        data = sock2.recv(128).decode()
    except Exception:
        logging.error('No Answer')
        sock2.close()
        return 1
    if data != "OK":
        if data.startswith('AUTH'):
            nonce = data.split()[1]
            cnonce_text = '%s%u%s%s' % (filename, content_size, file_md5, remote_addr)
            cnonce = hashlib.md5(cnonce_text.encode()).hexdigest()
            passmd5 = hashlib.md5(password.encode()).hexdigest()
            result_text = '%s:%s:%s' % (passmd5, nonce, cnonce)
            result = hashlib.md5(result_text.encode()).hexdigest()
            sys.stderr.write('Authenticating...')
            sys.stderr.flush()
            message = '%d %s %s\n' % (AUTH, cnonce, result)
            sock2.sendto(message.encode(), remote_address)
            sock2.settimeout(10)
            try:
                data = sock2.recv(32).decode()
            except Exception:
                sys.stderr.write('FAIL\n')
                logging.error('No Answer to our Authentication')
                sock2.close()
                return 1
            if data != "OK":
                sys.stderr.write('FAIL\n')
                logging.error('%s', data)
                sock2.close()
                sys.exit(1)
            sys.stderr.write('OK\n')
        else:
            logging.error('Bad Answer: %s', data)
            sock2.close()
            return 1
    sock2.close()

    logging.info('Waiting for device...')
    try:
        sock.settimeout(10)
        connection, client_address = sock.accept()
        sock.settimeout(None)
        connection.settimeout(None)
    except Exception:
        logging.error('No response from device')
        sock.close()
        return 1

    try:
        f = open(filename, "rb")
        if PROGRESS:
            update_progress(0)
        else:
            sys.stderr.write('Uploading')
            sys.stderr.flush()
        offset = 0
        while True:
            chunk = f.read(1460)
            if not chunk:
                break
            offset += len(chunk)
            update_progress(offset / float(content_size))
            connection.settimeout(10)
            try:
                connection.sendall(chunk)
                if connection.recv(32).decode().find('O') >= 0:
                    pass
            except Exception:
                sys.stderr.write('\n')
                logging.error('Error Uploading')
                connection.close()
                f.close()
                sock.close()
                return 1

        sys.stderr.write('\n')
        logging.info('Waiting for result...')
        # libraries/ArduinoOTA/ArduinoOTA.cpp L311 L320
        # only sends digits or 'OK'. We must not not close
        # the connection before receiving the 'O' of 'OK'
        try:
            connection.settimeout(60)
            received_ok = False
            received_error = False
            while not (received_ok or received_error):
                reply = connection.recv(64).decode()
                # Look for either the "E" in ERROR or the "O" in OK response
                # Check for "E" first, since both strings contain "O"
                if reply.find('E') >= 0:
                    sys.stderr.write('\n')
                    logging.error('%s', reply)
                    received_error = True
                elif reply.find('O') >= 0:
                    logging.info('Result: OK')
                    received_ok = True
            connection.close()
            f.close()
            sock.close()
            if received_ok:
                return 0
            return 1
        except Exception:
            logging.error('No Result!')
            connection.close()
            f.close()
            sock.close()
            return 1

    finally:
        connection.close()
        f.close()


class ESPOptions:
    def __init__(self, code_name, esp_ip, board):
        self.code_name = code_name
        self.esp_ip = esp_ip
        self.host_ip = "0.0.0.0"
        self.esp_port = 8266
        self.host_port = random.randint(10000, 60000)
        self.auth = ""
        self.image = f"bin/{code_name}/{code_name}.ino.bin"
        self.command = FLASH
        self.board = board

    def update(self):
        return serve(self.esp_ip,
                     self.host_ip,
                     self.esp_port,
                     self.host_port,
                     self.auth,
                     self.image,
                     self.command)

    def check_external_libs(self):
        external_libs_file = os.path.join('src', self.code_name, "external_libs.yml")
        if not os.path.isfile(external_libs_file):
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
        env = Environment(loader=FileSystemLoader(f'raw_src/{self.code_name}'))
        template = env.get_template(f'{self.code_name}.ino')
        with open('global_values.yml', 'r') as gv:
            data = yaml.safe_load(gv.read())
        output_render = template.render(**data)
        if os.path.exists(f"./src/{self.code_name}"):
            pass
            # print("Directory already exists!")
            # print("Refactoring file...")
        else:
            os.mkdir(f"./src/{self.code_name}")
        with open(f'src/{self.code_name}/{self.code_name}.ino', 'w') as pc:
            pc.write(output_render)

        return output_render

    def build(self):
        try:
            self.check_board()
        except Exception as e:
            return e
        arduino_build = f"arduino-cli compile -b {self.board} " \
                        f"./src/{self.code_name}/ " \
                        f"--output-dir bin/{self.code_name} "
        result, error = self.exec_command(arduino_build)
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
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
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
    esp.update()
    # ota = subprocess.Popen("./espota.py -i 192.168.1.79 -p 8266 -f bin/esp_test/esp_test.ino.bin", shell=True)
    # output, error = ota.communicate()
    # print(output)
