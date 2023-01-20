import base64
import itertools
import os.path
import socket
from os import error

from config import Config


class PasswordGenerator:
    def __init__(self, config):
        self.config = config
        self.characters = self.config.characters
        self.digits = self.config.digits
        self.symbols = self.config.symbols
        self.length = self.config.length

    def generate_password_dict(self):
        bulker = []
        for i in range(self.config.length['start'], self.config.length['end'] + 1):
            for item in itertools.product(self.config.characters + self.config.digits + self.config.symbols, repeat=i):
                password = "".join(item)
                print(password)
                if password == '0547755011':
                    return True
                # if len(bulker) >= self.config.bulker_len:
                #     self.save_passwords_file(bulker)
                #     bulker = []
                # bulker.append(item)

    def save_passwords_file(self, bulker):
        return

        file_path = os.path.join(self.config.filepath, self.config.filename)
        with open(file_path, 'w') as f:
            for i in bulker:
                print(i)
                # f.write(str(i))

    def get_response(self, response):
        if '200 OK' in str(response):
            return '200 OK'
        elif '401 Unauthorized' in str(response):
            return '401 Unauthorized'
        else:
            return response

    def base64encode(self, password, username):
        credentials = f'{password}:{username}'
        credentials_bytes = credentials.encode('ascii')
        base64_bytes = base64.b64encode(credentials_bytes)
        # encoded = base64.b64encode(f'{username}:{password}')
        print(str(base64_bytes))
        return base64_bytes

    def brute_force_rtsp(self):
        try:
            username = self.config.rtsp_username
            password = self.config.rtsp_password

            address = f'rtsp://{username}:{password}@{self.config.rtsp_ip}/{self.config.stream_url}'
            dest = "DESCRIBE " + address + " RTSP/1.0\r\nCSeq: 2\r\nUser-Agent: python\r\nAccept: application/sdp\r\n\r\n"
            print(address)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.config.rtsp_ip, self.config.rtsp_port))
            s.send(dest.encode())
            response = s.recv(512)

            print(self.get_response(response))
        except (ConnectionRefusedError, ConnectionResetError) as e:
            print(
                f'{e}: {self.config.rtsp_ip}:{self.config.rtsp_port} - {self.config.rtsp_username}:{self.config.rtsp_password}')
        except os.error.errno(113):
            print('s')
        except Exception as e:
            print(e)




if __name__ == '__main__':
    configs = Config()
    if configs.generate_paswords:
        generator = PasswordGenerator(config=configs)
        # generator.generate_password_dict()
        generator.brute_force_rtsp()
