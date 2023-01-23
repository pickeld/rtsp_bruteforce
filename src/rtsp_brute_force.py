import concurrent.futures
import os
import re

from config import Config
from src.helpers import create_conn


class RTSPBruteForce:
    def __init__(self):
        self.config = Config()
        self.characters = self.config.characters
        self.digits = self.config.digits
        self.symbols = self.config.symbols
        self.length = self.config.length
        self.active_tasks = []

    def get_pass_files(self):
        passwords = os.listdir(self.config.passwords_dir)
        return passwords

    def brute_force(self, bulks):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.workers) as executor:
            tasks = {executor.submit(create_conn, bulk): bulk for bulk in bulks}
            for _task in concurrent.futures.as_completed(tasks):
                task = tasks[_task]
                data = _task.result()
                if data != "None" or None:
                    print(data)
                    executor.shutdown()

    def bulker(self, passwords):
        bulks = []
        bulk = []
        for password in passwords:
            bulk.append(password)
            if len(bulk) >= self.config.bf_bulker_limit:
                bulks.append(bulk)
                bulk = []
        return bulks

    def run(self):
        files = self.get_pass_files()
        files.sort(key=lambda f: int(re.sub('\D', '', f)))
        for filename in files:
            file_path = os.path.join(self.config.passwords_dir, filename)
            with open(file_path, 'r') as f:
                passwords = f.read().splitlines()
            bulks = self.bulker(passwords=passwords)
            self.brute_force(bulks=bulks)
