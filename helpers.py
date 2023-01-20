import itertools
import os
from pathlib import Path

from config import Config


def generator_worker(i, config=Config()):
    bulker = []
    for item in itertools.product(config.characters + config.digits + config.symbols, repeat=i):
        password = "".join(item)
        print(password)
        # if password == '28d@':
        #     return True
        if len(bulker) >= config.bulker_len:
            save_passwords_file(bulker, config, i)
            bulker = []
        bulker.append(password)


def save_passwords_file(bulker, config, i):
    output_file = Path(os.path.join(config.filepath, f'passwords_{i}.txt'))
    output_file.parent.mkdir(exist_ok=True, parents=True)
    with open(output_file, 'a') as f:
        for s in bulker:
            f.write(f'{s}\n')
