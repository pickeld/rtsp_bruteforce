from config import Config
from rtsp_brute_force import  RTSPBruteForce
from password_generator import PasswordGenerator

if __name__ == '__main__':
    configs = Config()
    if configs.generate_paswords:
        pass_gen = PasswordGenerator()
        pass_gen.password_gen_orch()
    if configs.brute_force:
        brute_forcer = RTSPBruteForce()
        brute_forcer.run()
