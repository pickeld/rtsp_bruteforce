from config import Config
from utils import PasswordGenerator

if __name__ == '__main__':
    configs = Config()
    if configs.generate_paswords:
        pass_gen = PasswordGenerator()
        pass_gen.password_gen_orch()
    # brute_forcer = RTSPBruteForce(config=configs)
    # brute_forcer.brute_force_rtsp()
