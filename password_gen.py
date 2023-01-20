import base64
import itertools
import os.path
import socket


from config import Config

class PasswordGenerator:
    def __init__(self):
        self.config = Config()
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
        file_path = os.path.join(self.config.filepath, self.config.filename)
        with open(file_path, 'w') as f:
            for i in bulker:
                print(i)
                # f.write(str(i))
