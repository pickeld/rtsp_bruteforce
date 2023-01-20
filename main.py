from config import Config
from utils import PasswordGenerator, RTSPBruteForce

if __name__ == '__main__':
    configs = Config()
    if configs.generate_paswords:
        pass_gen = PasswordGenerator()
        pass_gen.password_gen_orch()
    brute_forcer = RTSPBruteForce()
    brute_forcer.run()
