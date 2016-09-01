import json
import socket
from env import *


def netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    # while True:
    #     data = s.recv(4096)
    #     if not data:
    #         break
    #     print(repr(data))
    s.close()


def log(content):
    if not LOGSTASH_HOST:
        return
    log = {'component': 'webserver',
           'webserver': content}

    try:
        netcat(LOGSTASH_HOST, LOGSTASH_PORT, json.dumps(log))
    except:
        print('failed to log')
