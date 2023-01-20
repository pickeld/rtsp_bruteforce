class Config:
    def __init__(self):
        self.passwords_dir = '/tmp/passwords'
        self.archive_folder = 'archive'
        self.characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.digits = '0123456789'
        self.symbols = '!@#$%^&*()'
        self.length = {"start": 0, "end": 20}
        self.generate_paswords = True
        # self.generate_paswords = False
        self.bulker_len = 5_000_000
        self.rtsp_ip = '192.168.127.30'
        self.rtsp_port = 8554
        self.rtsp_username = 'admin'
        self.rtsp_password = 'admin'
        self.stream_url = 'unicast'
        self.publish_progress = False
        self.pass_gen_threads = 8
        self.brute_force = True
        self.brute_force = False
