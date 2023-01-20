import threading

from config import Config
from helpers import generator_worker


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
            t = threading.Thread(target=generator_worker, args=(i,))
            threads.append(t)
            t.start()
