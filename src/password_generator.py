import itertools
import os
from multiprocessing import Process
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
