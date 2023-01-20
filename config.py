class Config:
    def __init__(self):
        self.filepath = '/tmp'
        self.filename = 'passwords.txt'
        self.characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.digits = '0123456789'
        self.symbols = '!@#$%^&*()'
        self.length = {"start": 0, "end": 20}
        self.generate_paswords = True
        self.bulker_len = 1000
        self.rtsp_ip = '192.168.127.30'
        self.rtsp_port = 8554
        self.rtsp_username = 'admin'
        self.rtsp_password = 'admin'
        self.stream_url = 'unicast'
